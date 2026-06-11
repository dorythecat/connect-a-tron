import os, subprocess
from enum import Enum

import interfaces.awg.awg as awg

# See https://www.eevblog.com/forum/testgear/feeltech-fy3224s-24mhz-2-channel-dds-aw-function-signal-generator/msg708434/?topicseen#msg708434 for more information on commands for this AWG

class WaveType(Enum):
    SINE  = 0  # Sinusoidal
    SQUR  = 1  # Square
    TRGL  = 2  # Triangle
    STW   = 3  # Sawtooth
    NSTW  = 4  # Inverted sawtooth
    DC    = 5  # Offset value determines the DC voltage
    PRE1  = 6  # Lorentz pulse
    PRE2  = 7  # Multitonal
    PRE3  = 8  # Periodic random noise
    PRE4  = 9  # Electrocardiogram
    PRE5  = 10 # Trapezoidal
    PRE6  = 11 # Sinc (sin(x)/x)
    PRE7  = 12 # Pulse
    PRE8  = 13 # Gaussian white noise
    PRE9  = 14 # Amplitude Modulated (AM)
    PRE10 = 15 # Frequency Modulated (FM)
    ARB1  = 16 # Arbitrary waveform 1
    ARB2  = 17 # Arbitrary waveform 2
    ARB3  = 18 # Arbitrary waveform 3
    ARB4  = 19 # Arbitrary waveform 4

class FY3200S(awg.AWG):
    def __init__(self, port: str = "/dev/ttyUSB0") -> None:
        super().__init__(port)

    @property
    def id(self) -> str:
        return self._get_str("a")

    def set_waveform(self, channel: int = 1, freq: float = 1000, amp: float = 1, offset: float = 0, duty: float = 50, typ: WaveType = WaveType.SINE, phase: int = 0) -> None:
        """
        Sets the waveform for the arbitrary waveform generator to produce.

        :param channel: Channel of the generator to set. (1 or 2)
        :param freq: Frequency of the desired wave, in Hertzs. (0.01 <= freq <= 20000000) (0 will turn the generator off)
        :param amp: Amplitude of the desired wave, in Volts. (0.01 <= amp <= 20) (0 will turn the generator off)
        :param offset: Offset of the desired wave, in Volts. (abs(offset) <= 10)
        :param duty: Duty cycle of the desired wave, in percentage. (0.1 <= duty <= 99.9)
        :oaram typ: Type of the desired wave.
        :param phase: Phase offset of the desired wave. (0 <= phase <= 359)

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        if channel not in [1, 2]:
            raise AttributeError("Invalid channel provided!")
        if freq != 0 and not 0.01 <= freq <= 20000000:
            raise AttributeError("Invalid frequency value provided!")
        if amp != 0 and not 0.01 <= amp <= 20:
            raise AttributeError("Invalid amplitude value provided!")
        if abs(offset) > 10:
            raise AttributeError("Invalid offset value provided!")
        if not 0.1 <= duty <= 99.9:
            raise AttributeError("Invalid duty cycle value provided!")
        if not 0 <= phase <= 359:
            raise AttributeError("Invalid phase value provided!")

        chan = "b" if channel == 1 else "d" # Channel select letter
        self._send(f'{chan}f{int(freq * 100)}') # AWG expects frequency in cHz, NOT Hz
        self._send(f'{chan}a{amp}')
        self._send(f'{chan}o{offset}')
        self._send(f'{chan}d{duty}')
        self._send(f'{chan}w{typ.value}')
        self._send(f'{chan}p{phase}')
