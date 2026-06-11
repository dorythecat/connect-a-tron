class AWG:
    def __init__(self, port: str) -> None:
        self._port: str = port

        self._conn = open(port, "r+b", buffering=0) # Open serial communication as a file

    def __del__(self) -> None:
        return self._conn.close() # Close the connection properly once we're done

    @property
    def port(self) -> str:
        return self._port

    @property
    def id(self) -> str:
        return "Generic AWG"

    def set_waveform(self, channel: int, freq: float, amp: float, offset: float, duty: int) -> None:
        raise NotImplementedError
