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

    def measure_set(self, nplc: float = 10, typ: dmm.MType = dmm.MType.DC_VOLT, samples: int = 1, mov: bool = False, digits: int = 7, threshold: int = 10, bandwidth: int = 30) -> None:
        """
        Configures the DMM to use the given settings for all following single measurements.

        :param nplc: Number of powerline cycles to sample (0.01 to 10)
        :param typ: Type of measurement to make
        :param samples: How many raw measurements to average for each queried measurement
        :param filt: Wether to use a moving filter, uses repeat filter if false (See "Filter types" on the Keithley 2000 for more information)
        :param digits: How many digits of precision to display (only affects front panel view, not returned value)
        :param threshold: Threshold for continuity, in Ohms
        :param bandwidth: Bandwidth for AC measurements, in Hertz
        :raises AttributeError: If nplc, samples, digits, threshold, or bandwidth are out of range
        """
        if not 0.01 <= nplc <= 10:
            raise AttributeError("NPLC out of range!")
        if not 1 <= samples <= 100:
            raise AttributeError("Samples out of range!")
        if not 4 <= digits <= 7:
            raise AttributeError("Digits out of range!")
        if not 1 <= threshold <= 1000:
            raise AttributeError("Threshold out of range!")
        if not 3 <= bandwidth <= 300000:
            raise AttributeError("Bandwidth out of range")
        super().measure_set(nplc, typ, samples)

        self._ser.write(b'*RST\n*CLS\n') # Reset everything
        func = ["VOLT:DC", "VOLT:AC", "CURR:DC", "CURR:AC", "RES", "FRES", "TEMP", "PER", "FREQ", "DIOD", "CONT"][typ.value - 1]
        self._ser.write(f':SENS:FUNC "{func}"\n'.encode()) # Set the desired function
        if typ.value < 7: # These settings can't be set for Temperature (the manual begs to differ, but it gives a -113 "Undefined header" error), Frequency, Period, Diode, and Continuity measurements
            if typ.value in [2, 4]:
                self._ser.write(f':SENS:{func}:DET:BAND {bandwidth}\n'.encode())
            else:
                self._ser.write(f':SENS:{func}:NPLC {nplc}\n'.encode()) # Set NPLC (Not applicable to AC measurements, even though the documentation says otherwise, we'll get a -221 "Settings conflict" error)

            self._ser.write(f':SENS:{func}:AVER:COUN {samples}\n'.encode()) # Set number of samples the filter will take
            self._ser.write(f':SENS:{func}:AVER:TCON {"MOV" if mov else "REP"}\n'.encode()) # Set the apropiate type of filter to be used
            self._ser.write(f':SENS:{func}:AVER:STAT {int(samples > 1)}\n'.encode()) # Turn on averaging filter only if samples > 1
        if typ.value < 10: # Can't be set for Diode and Continuity measurements
            self._ser.write(f':SENS:{func}:DIG {digits}\n'.encode()) # Set digits
        elif typ.value == 11: # Set this only for continuity measurements only
            self._ser.write(f':SENS:{func}:THR {threshold}\n'.encode()) # Set continuity threshold

    def measure_get(self) -> float:
        """
        Measures raw data, with the settings provided, and returns a single sample.

        For averaging multiple samples, see measure_avg.

        A measurement will take, at least, delay_time seconds.

        :return: One raw measurement
        """
        self._ser.write(b':READ?\n') # Ask for reading back
        return float(self._ser.readline().decode()) # Return parsed output
