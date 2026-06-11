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

    @property
    def port(self) -> str:
        return self._port

    @property
    def id(self) -> str:
        return "Generic AWG"

    def set_waveform(self, channel: int, freq: float, amp: float, offset: float, duty: int) -> None:
        raise NotImplementedError
