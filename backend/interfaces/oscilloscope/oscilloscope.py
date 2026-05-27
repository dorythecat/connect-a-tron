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
        return True

    @keypad_lock.setter
    def keypad_lock(self, value: bool) -> None:
        pass

    def frequency(self, channel: int = 1) -> float:
        return 0

    def period(self, channel: int = 1) -> float:
        return 0

    def rms(self, channel: int = 1) -> float:
        return 0

    def ppk(self, channel: int = 1) -> float:
        return 0

    def get_waveform(self, points: int, mode: str, samples: int) -> list[float]:
        pass

    def set_waveform(self, freq: float, amp: float, offset: float, typ: str, duty: int) -> None:
        pass

