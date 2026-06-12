import subprocess

class AWG:
    def __init__(self, port: str) -> None:
        self._port: str = port

    # Helper functions to communicate with the device
    def _send(self, command: str) -> None:
        subprocess.Popen(f'echo "{command}" > {self._port}', shell=True).wait()

    def _get_str(self, command: str) -> str:
        self._send(command)
        return subprocess.check_output(f'cat {self._port}', shell=True, text=True)

    def _get_float(self, command: str) -> float:
        return float(self._get_str(command))

    @property
    def port(self) -> str:
        return self._port

    @property
    def id(self) -> str:
        return "Generic AWG"

    def set_waveform(self, channel: int, freq: float, amp: float, offset: float, duty: int) -> None:
        raise NotImplementedError

    def set_fsweep(self, channel: int, start: float, stop: float, time: float, typ: int) -> None:
        raise NotImplementedError

    def start_fsweep(self, channel: int) -> None:
        raise NotImplementedError

    def stop_fsweep(self, channel: int) -> None:
        raise NotImplementedError

    def set_asweep(self, channel: int, start: float, stop: float, time: float, typ: int) -> None:
        raise NotImplementedError

    def start_asweep(self, channel: int) -> None:
        raise NotImplementedError

    def stop_asweep(self, channel: int) -> None:
        raise NotImplementedError
