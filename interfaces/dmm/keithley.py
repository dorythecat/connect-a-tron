import serial
import time

import interfaces.dmm.dmm as dmm

class Keithley2000(dmm.DMM):
    def __init__(self, port: str = "/dev/ttyUSB0", baud_rate: int = 9600) -> None:
        """
        :param port: The serial port where the DMM is connected
        :param baud_rate: The baud rate to use to communicate with the DMM
        :param plf: The powerline frequency, in Hertzs (defaults to 50)
        :raises AttributeError: If baud_rate not supported
        """
        if baud_rate not in [300, 600, 1200, 2400, 4800, 9600, 19200]:
            raise AttributeError("Baud Rate not supported!")

        super().__init__(port, baud_rate)

        self._ser.write(b':SYST:BEEP:STAT 0\n') # Disable beeper by default

        # Get current powerline frequency
        self._ser.write(b':SYST:LFR?\n')
        self._plf = int(self._ser.readline().decode())

    @property
    def id(self) -> str:
        self._ser.write(b'*IDN?\n') # Query the ID
        return self._ser.readline().decode()[:-3] # Output the decoded ID, with the trailing newline removed

    @property
    def beeper(self) -> bool:
        self._ser.write(b':SYST:BEEP:STAT?\n')
        return bool(int(self._ser.readline().decode()))

    @beeper.setter
    def beeper(self, value: bool = True) -> None:
        self._ser.write(f':SYST:BEEP:STAT {int(value)}\n'.encode())

    @property
    def display(self) -> bool:
        self._ser.write(b':DISP:ENAB?\n')
        return bool(int(self._ser.readline().decode()))

    @display.setter
    def display(self, value: bool = True) -> bool:
        self._ser.write(f':DISP:ENAB {int(value)}\n'.encode())

    @property
    def text(self) -> str:
        self._ser.write(b':DISP:TEXT:DATA?\n')
        return self._ser.readline().decode()[1:-2] # Remove special characters

    @text.setter
    def text(self, value: str = "") -> None:
        if value == "":
            self._ser.write(b':DISP:TEXT:STAT 0\n')
            return
        self._ser.write(b':DISP:TEXT:STAT 1\n')
        self._ser.write(f':DISP:TEXT:DATA "{value[:12]}"\n'.encode())
        while len(value) > 12:
            time.sleep(0.5) # TODO: This should be a setting? idrk, also probably adding a "loop" feature?
            value = value[1:]
            self._ser.write(f':DISP:TEXT:DATA "{value[:12]}"\n'.encode())

    @property
    def input(self) -> bool:
        self._ser.write(b':SYST:FRSW?\n')
        return bool(int(self._ser.readline().decode()))

    @property
    def autozero(self) -> bool:
        self._ser.write(b':SYST:AZER:STAT?\n')
        return bool(int(self._ser.readline().decode()))

    @autozero.setter
    def autozero(self, value: bool) -> None:
        self._ser.write(f':SYST:AZER:STAT {int(value)}\n'.encode())

    @property
    def key_press(self) -> int:
        self._ser.write(b':SYST:KEY?\n')
        return int(self._ser.readline().decode())

    @key_press.setter
    def key_press(self, value: int) -> None:
        if value < 1 or value > 31:
            raise AttributeError("Invalid key number provided!")
        self._ser.write(f':SYST:KEY {value}\n'.encode())

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

        self._ser.write(b'*RST\n*CLS\n:INIT:CONT OFF\n:ABORT\n') # Reset everything
        func = ["VOLT:DC", "VOLT:AC", "CURR:DC", "CURR:AC", "RES", "FRES", "PER", "FREQ", "TEMP", "DIOD", "CONT"][typ.value - 1]
        self._ser.write(f':SENS:FUNC "{func}"\n'.encode()) # Set the desired function
        if typ.value < 7: # Set NPLC for the functions that need it
            self._ser.write(f':SENS:{func}:NPLC {nplc}\n'.encode())

    def measure_get(self) -> float:
        """
        Measures raw data, with the settings provided, and returns a single sample.

        For averaging multiple samples, see measure_avg.

        A measurement will take, at least, delay_time seconds.

        :return: One raw measurement
        """
        self._ser.write(b':READ?\n') # Ask for reading back
        return float(self._ser.readline().decode()) # Return parsed output

    def measure_avg(self, n: int = 2) -> float:
        # TODO: Make this work with the internal avergaing of the Keithley 2000
        """
        Measures raw data, with the settings provided, n times, and averages them.

        For n = 1, preferably use measure_get.

        A measurement will take, at least, n * delay_time seconds.

        :param n: How many samples to take
        :return: One averaged measurement
        """
        self._ser.write(f':SAMP:COUN {n}\n'.encode()) # Set sample count
        self._ser.write(b':READ?\n') # Query samples
        s: float = 0
        for a in self._ser.readline().decode().split(','):
            s += float(a)
        self._ser.write(b':SAMP:COUN 1\n') # Return sample count to normal
        return s / n # Return the average
