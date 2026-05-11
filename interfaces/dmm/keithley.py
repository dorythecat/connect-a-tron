import serial
import time

import interfaces.dmm.dmm as dmm

class Keithley2000(dmm.DMM):
    def __init__(self, port: str = "/dev/ttyUSB0", baud_rate: int = 9600, plf: int = 50) -> None:
        """
        :param port: The serial port where the DMM is connected
        :param baud_rate: The baud rate to use to communicate with the DMM
        :param plf: The powerline frequency, in Hertzs (defaults to 50)
        :raises AttributeError: If baud_rate not supported
        """
        if baud_rate not in [300, 600, 1200, 2400, 4800, 9600, 19200]:
            raise AttributeError("Baud Rate not supported!")

        super().__init__(port, baud_rate, plf)

    @property
    def id(self) -> str:
        self._ser.write(b'*RST\n*IDN?\n') # Reset everything and query the ID
        return self._ser.readline().decode() # Output the decoded ID

    def measure_set(self, nplc: float = 10, typ: dmm.MType = dmm.MType.DC_VOLT) -> None:
        """
        Configures the DMM to use the given settings for all following single measurements.

        :param nplc: Number of powerline cycles to sample (0.01 to 10)
        :param typ: Type of measurement to make
        :raises AttributeError: If nplc is out of range 
        """
        if nplc < 0.01 or nplc > 10:
            raise AttributeError("NPLC out of range!")
        super().measure_set(nplc, typ)

        self._ser.write(b'*RST\n') # Reset everything
        func = ["VOLT:DC", "VOLT:AC", "CURR:DC", "CURR:AC", "RES", "FRES", "PER", "FREQ", "TEMP", "DIOD", "CONT"][typ.value - 1]
        self._ser.write(f':SENS:FUNC "{func}\n'.encode()) # Set the desired function
        if typ.value < 7: # Set NPLC for the functions that need it
            self._ser.write(f'SENS:{func}:NPLC {nplc}\n'.encode())

    def measure_raw(self) -> float:
        """
        Measures raw data, with the settings provided, and returns a single sample.

        For averaging multiple samples, see measure_avg.

        :return: One raw measurement
        """
        self._ser.write(b':INIT\n') # Query measurement
        time.sleep(self._delay_time) # WAit for measurement to be available
        self._ser.write(b':SENS:DATA?\n') # Ask for reading back
        return float(self._ser.readline().decode()) # Return parsed output

    def measure_avg(self, n: int = 2) -> float:
        """
        Measures raw data, with the settings provided, n times, and averages them.

        For n = 1, preferably use measure_raw.

        :param n: How many samples to take
        :return: One averaged measurement
        """
        self._ser.write(b':INIT:CONT ON\n') # Start continuous measurement
        i: int = 0
        avg: float = 0
        while i != n:
            time.sleep(self._delay_time) # Wait for measurement to be available
            self._ser.write(b':SENS:DATA?\n') # Ask for reading back
            avg += float(self._ser.readline().decode()) # Add the new value to the total
        self._ser.write(b':INIT:CONT OFF\n') # Stop continuous measurement
        return avg / n # Return the average

    def continuous_set(self, nplc: float = 10, typ: dmm.MType = dmm.MType.DC_VOLT) -> None:
        """
        Configures the DMM to take continuous measurements with the settings provided.

        :param nplc: Number of powerline cycles to sample (0.01 to 10)
        :param type: Type of measurement to make
        :raises AttributeError: If nplc is out of range
        """
        if nplc < 0.01 or nplc > 10:
            raise AttributeError("NPLC out of range!")
        super().continuous_set(nplc, typ)

        self._ser.write(b'*RST\n') # Reset everything
        func = ["VOLT:DC", "VOLT:AC", "CURR:DC", "CURR:AC", "RES", "FRES", "PER", "FREQ", "TEMP", "DIOD", "CONT"][typ.value - 1]
        self._ser.write(f':SENS:FUNC "{func}"\n'.encode()) # Set the desired function
        if typ.value < 7: # Set NPLC for the functions that need it
            self._ser.write(f':SENS:{func}:NPLC {nplc}\n'.encode())
        self._ser.write(b':INIT:CONT ON\n') # Start continuous data collection

    def continuous_get(self) -> float:
        """
        Gets a measurement from continuous mode.

        Remember that a new measurement is only guaranteed after delay_time seconds have passed from the previous measurement.

        :return: one measurement
        """
        self._ser.write(b':SENS:DATA?\n')
        return float(self._ser.readline().decode())
