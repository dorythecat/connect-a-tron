import serial
from enum import Enum

class MType(Enum):
    DC_VOLT = 1
    AC_VOLT = 2
    DC_CURR = 3
    AC_CURR = 4
    RES     = 5
    FRES    = 6
    PERIOD  = 7
    FREQ    = 8
    TEMP    = 9
    DIODE   = 10
    CONT    = 11

class DMM:
    def __init__(self, port: str, baud_rate: int) -> None:
        # Given settings
        self._port: str = port
        self._baud_rate: int = baud_rate

        # Generated settings, or given settings through other functions
        self._plf: int = 50
        self._nplc: float = 10
        self._typ: MType = MType.DC_VOLT
        self._delay_time: float = self.nplc / self.plf

        # Connect through serial
        self._ser = serial.Serial(self.port, self.baud_rate)

    @property
    def port(self) -> str:
        return self._port

    @property
    def baud_rate(self) -> int:
        return self._baud_rate

    @property
    def plf(self) -> int:
        return self._plf

    @property
    def nplc(self) -> float:
        return self._nplc

    @property
    def typ(self) -> MType:
        return self._type

    @property
    def delay_time(self) -> float:
        return self._delay_time

    @property
    def id(self) -> str: # This should be overriden by child classes, always
        return "Generic DMM"

    @property
    def beeper(self) -> bool:
        return True

    @beeper.setter
    def beeper(self, value: bool) -> None:
        pass

    @property
    def display(self) -> bool:
        return True

    @display.setter
    def display(self, value: bool) -> None:
        pass

    @property
    def text(self) -> str:
        return ""

    @text.setter
    def text(self, value: str) -> None:
        pass

    @property
    def input(self) -> bool: # True means front, False means back
        return True

    @property
    def autozero(self) -> bool:
        return True

    @autozero.setter
    def autozero(self, value: bool) -> None:
        pass

    @property
    def key_press(self) -> int:
        return -1

    @key_press.setter
    def key_press(self, value: int) -> None:
        pass

    def measure_set(self, nplc: float, typ: MType) -> None:
        self._nplc = nplc
        self._typ = typ
        self._delay_time = self.nplc / self.plf

    def measure_get(self) -> float:
        pass

    def measure_avg(self, n: int = 2) -> float:
        pass

    def continuous_set(self, nplc: float, typ: MType) -> None:
        self._nplc = nplc
        self._typ = typ
        self._delay_time = self.nplc / self.plf

    def continuous_get(self) -> float:
        pass
