class Oscilloscope:
    def __init__(self, port: str) -> None:
        self._port: str = port

        self._conn = open(port, "r+b", buffering=0) # We open the serial communication as a file

    def __del__(self) -> None:
        self._conn.close() # Close the file properly once we're done

    @property
    def port(self) -> str:
        return self._port

    @property
    def keypad_lock(self) -> bool:
        raise True # Default value, since most oscilloscopes will have their keypad locked by default

    @keypad_lock.setter
    def keypad_lock(self, value: bool) -> None:
        raise NotImplementedError

    def frequency(self, channel: int) -> float:
        raise NotImplementedError

    def period(self, channel: int) -> float:
        raise NotImplementedError

    def rms(self, channel: int) -> float:
        raise NotImplementedError

    def ppk(self, channel: int) -> float:
        raise NotImplementedError

    def time_conf(self, scale: float, offset: float) -> None:
        raise NotImplementedError

    def channel_conf(self, channel: int, on: bool, scale: float, offset: float, probe: int, invert: bool, coupling: str) -> None:
        raise NotImplementedError

    def get_waveform(self, points: int, mode: str, samples: int) -> list[float]:
        raise NotImplementedError

    def set_waveform(self, freq: float, amp: float, offset: float, typ: str, duty: int) -> None:
        raise NotImplementedError

