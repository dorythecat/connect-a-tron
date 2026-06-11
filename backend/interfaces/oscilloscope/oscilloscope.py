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
    def id(self) -> str:
        return "Generic Oscilloscope"

    @property
    def keypad_lock(self) -> bool:
        raise True # Default value, since most oscilloscopes will have their keypad locked by default

    @keypad_lock.setter
    def keypad_lock(self, value: bool) -> None:
        raise NotImplementedError

    @property
    def trigger_status(self) -> bool: # True if triggered, False otherwise
        return False # Default value, so we don't falsely claim it has been triggered

    def frequency(self, channel: int) -> float:
        raise NotImplementedError

    def period(self, channel: int) -> float:
        raise NotImplementedError

    def rms(self, channel: int) -> float:
        raise NotImplementedError

    def ppk(self, channel: int) -> float:
        raise NotImplementedError

    def force_trigger(self) -> None:
        raise NotImplementedError

    def time_conf(self, scale: float, offset: float) -> None:
        raise NotImplementedError

    def channel_conf(self, channel: int, on: bool, scale: float, offset: float, probe: int, invert: bool, coupling: str) -> None:
        raise NotImplementedError

    # Various trigger modes, not all of them need to be supported by a child class, though it DOES need to at least support edge triggering aqnd the general configuration function
    def trigger_conf_general(self, mode: str, holdoff: float) -> None:
        raise NotImplementedError

    def trigger_conf_edge(self, source: int, level: float, slope: str) -> None:
        raise NotImplementedError

    def trigger_conf_pulse(self, source: int, level: float, polarity: bool, width: float, when: str) -> None:
        raise NotImplementedError

    def trigger_conf_slope(self, source: int, upper_level: float, lower_level: float, polarity: bool, width: float, when: str) -> None:
        raise NotImplementedError

    def trigger_conf_interval(self, source: int, level: float, slope: str, time: float, when: str) -> None:
        raise NotImplementedError

    def trigger_conf_underthrow(self, source: int, upper_level: float, lower_level: float, polarity: bool, time: float, when: str) -> None:
        raise NotImplementedError

    def trigger_conf_timeout(self, source: int, level: float, polarity: bool, width: float) -> None:
        raise NotImplementedError

    def trigger_conf_window(self, source: int, upper_level: float, lower_level: float) -> None:
        raise NotImplementedError

    def trigger_conf_pattern(self, pattern: str, levels: str) -> None:
        raise NotImplementedError

    def trigger_conf_video(self, source: int, level: float, polarity: bool, standard: str, mode: str, line: int) -> None:
        raise NotImplementedError

    def trigger_conf_uart(self, source: int, level: float, width: int, baud_rate: int, parity: str, data: int, condition: str) -> None:
        raise NotImplementedError

    def trigger_conf_spi(self, source_sda: int, source_scl: int, level_sda: float, level_scl: float, clock_edge: bool, width: int, data: int, mask: int) -> None:
        raise NotImplementedError

    def trigger_conf_i2c(self, source_sda: int, source_scl: int, level_sda: float, level_scl: float, address: int, data: int, data_index: int, condition: str) -> None:
        raise NotImplementedError

    def trigger_conf_can(self, source: int, level: float, baud_rate: int, idle: bool, identifier: int, data_len: int, data: int, data_index: int, condition: str) -> None:
        raise NotImplementedError

    def trigger_conf_lin(self, source: int, level: float, baud_rate: int, idle: bool, identifier: int, data: int, condition: str) -> None:
        raise NotImplementedError

    def get_waveform(self, points: int, mode: str, samples: int) -> list[float]:
        raise NotImplementedError

    def set_waveform(self, freq: float, amp: float, offset: float, typ: str, duty: int) -> None:
        raise NotImplementedError

