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
    def __init__(self, port: str = "/dev/ttyUSB0", baud_rate: int = 9600, plf: int = 50) -> None:
        # Given settings
        self._port: str = port
        self._baud_rate: int = baud_rate
        self._plf: int = plf

        # Generated settings, or given settings through other functions
        self._nplc: float = 10
        self._typ: MType = MType.DC_VOLT
        self._delay_time: float = 1.5 * self.nplc / self.plf

        # Connect through serial
        self._ser = serial.Serial(self.port, self.baud_rate, timeout=3)

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

    def measure_set(self, nplc: float, typ: MType) -> None:
        self._nplc = nplc
        self._typ = typ
        self._delay_time = 1.5 * self.nplc / self.plf

    def measure_raw(self) -> float:
        pass

    def measure_avg(self, n: int = 2) -> float:
        pass

    def continuous_set(self, nplc: float, typ: MType) -> None:
        self._nplc = nplc
        self._typ = typ
        self._delay_time = 1.5 * self.nplc / self.plf

    def continuous_get(self) -> float:
        pass
