import backend.interfaces.oscilloscope.oscilloscope as oscilloscope

class DSO2D15(oscilloscope.Oscilloscope):
    def __init__(self, port: str = "/dev/usbtmc0") -> None:
        super().__init__(port)

    def __del__(self) -> None:
        super().__del__()

    def frequency(self, channel: int = 1) -> float:
        """
        Get the frequency of the waveform currently being read by the oscilloscope on the specified channel.

        :param channel: The channel to read data from. (1 or 2)

        :returns: Frequency of the waveform, in Hz.
        :raises AttributeError: If the provided channel is not valid.
        """
        if channel not in [1, 2]:
            raise AttributeError("Invalid channel provided!")

        self._conn.write(f':MEAS:CHAN{channel}:ITEM? FREQ\n'.encode())
        return float(self._conn.read(64).decode())

    def period(self, channel: int = 1) -> float:
        """
        Get the period of the waveform currently being read by the oscilloscope on the specified channel.

        :param channel: The channel to read data from. (1 or 2)

        :returns: Period of the waveform, in s.
        :raises AttributeError: If the provided channel is not valid.
        """
        if channel not in [1, 2]:
            raise AttributeError("Invalid channel provided!")

        self._conn.write(f':MEAS:CHAN{channel}:ITEM? PERIOD\n'.encode())
        return float(self._conn.read(32))

    def rms(self, channel: int = 1) -> float:
        """
        Get the RMS voltage of the waveform currently being read by the oscilloscope on the specified channel.

        :param channel: The channel to read data from. (1 or 2)

        :returns: RMS voltage of the waveform, in Hz.
        :raises AttributeError: If the provided channel is not valid.
        """
        if channel not in [1, 2]:
            raise AttributeError("Invalid channel provided!")

        self._conn.write(f':MEAS:CHAN{channel}:ITEM? RMS\n'.encode())
        return float(self._conn.read(32))

    def ppk(self, channel: int = 1) -> float:
        """
        Get the RMS voltage of the waveform currently being read by the oscilloscope on the specified channel.

        :param channel: The channel to read data from. (1 or 2)

        :returns: RMS voltage of the waveform, in Hz.
        :raises AttributeError: If the provided channel is not valid.
        """
        if channel not in [1, 2]:
            raise AttributeError("Invalid channel provided!")

        self._conn.write(f':MEAS:CHAN{channel}:ITEM? VPP\n'.encode())
        return float(self._conn.read(32))

    def get_waveform(self, points: int = 4000, mode: str = "HRES", samples: int = 4) -> list[float]:
        """
        Measures the waveform data from the oscilloscope, ensuring the format is correct and automactically handling all header data and integrity checks.

        :param points: Number of points to sample. (4000, 40000, 400000, 4000000, or 8000000)
        :param mode: The acquisition method for samples. ("NORM", "AVER", "PEAK", "HRES")
        :param samples: Number of samples to take in AVER mode. (4, 8, 16, 32, 64, 128)

        :return: A list of floats containing the parsed waveform data from channel one. Currently we don't support the second channel.
        :raises AttributeError: If the provided values are invalid.
        :raises RuntimeError: If the readout fails for any reason, including corrupted data or malformed responses.
        """
        if points not in [4000, 40000, 400000, 4000000, 8000000]:
            raise AttributeError("Provided points value is invalid!")
        if mode not in ["NORM", "AVER", "PEAK", "HRES"]:
            raise AttributeError("Provided mode value is invalid!")
        if samples not in [4, 8, 16, 32, 64, 128]:
            raise AttributeError("Provided samples value is invalid!")

        self._conn.write(b':CHAN1:DISP 1\n') # Make sure channel 1 is enabled (we don't care about the status of channel 2)
        self._conn.write(f':ACQ:POIN {points}\n'.encode()) # Set number of points to sample
        self._conn.write(f':ACQ:TYPE {mode}\n'.encode()) # Set the acquisition mode
        self._conn.write(f':ACQ:COUN {samples}\n'.encode()) # Set the number of samples to average in AVER mode

        self._conn.write(b':WAV:DATA:ALL?\n') # Query header
        data = self._conn.read(128)
        if data[:2] != b'#9':
            raise RuntimeError("Response header is corrupted or invalid!")
        offset = float(data[31:35])
        voltage = float(data[47:53])
        counter = points
        out = []
        while counter > 0:
            self._conn.write(b':WAV:DATA:ALL?\n') # Query actual data
            data = self._conn.read(4096)
            if data[:2] != b'#9':
                raise RuntimeError("Response header is corrupted or invalid!")
            for i in range(29, len(data)):
                val = int(data[i])
                val = val if val <= 127 else val - 256 # Handle negative numbers
                out.append((val - offset) * voltage)
            counter -= 4096
        return out

    def set_waveform(self, freq: float = 1000, amp: float = 1, offset: float = 0, typ: str = "SINE", duty: int = 50, mod: str = "NONE", mod_typ: str = "SINE", mod_freq: int = 1000, mod_depth: int = 100) -> None:
        """
        Sets the waveform for the arbitrary waveform generator to produce.

        :param freq: Frequency of the desired wave, in hertz. (0.1 <= freq <= 25000000) (0 will turn the generator off)
        :param amp: Amplitude of the desired wave, in volts. (0.01 <= amp <= 7) (0 will turn the generator off)
        :param offset: Offset of the desired wave, in volts. (-3 <= offset <= 3)
        :param typ: Type of the desired wave. ("SINE", "SQUA", "RAMP", "EXP", "NOIS", "DC", "ARB1", "ARB2", "ARB3", "ARB4")
        :param duty: Duty cycle of the desired wave, in percentage (0 <= duty <= 100)
        :param mod: The type of modulation to apply to the signal ("NONE", "AM", or "FM")
        :param mod_typ: The type of signal to modulate with ("SINE", "SQUA", or "RAMP")
        :param mod_freq: The frequency to modulate with, in hertz (100 <= mod_freq <= 50000)
        :param mod_depth: In AM modulation, this value is the modulation depth (0 <= mod_depth <= 100), while in FM modulation, this value is the modulation deviation (100 <= mod_depth <= 10000)

        :returns: Nothing.
        :raises AttributeError: If any of the provided values is invalid.
        """
        if freq != 0 and not 0.1 <= freq <= 25000000:
            raise AttributeError("Invalid frequency value provided!")
        if amp != 0 and not 0.01 <= amp <= 7:
            raise AttributeError("Invalid amplitude value provided!")
        if not -3 <= offset <= 3:
            raise AttributeError("Invalid offset value provided!")
        if typ not in ["SINE", "SQUA", "RAMP", "EXP", "NOIS", "DC", "ARB1", "ARB2", "ARB3", "ARB4"]:
            raise AttributeError("Invalid type value provided!")
        if not 0 <= duty <= 100:
            raise AttributeError("Invalid duty cycle value provided!")
        if mod not in ["NONE", "AM", "FM"]:
            raise AttributeError("Invalid modulation value provided!")
        if mod_typ not in ["SINE", "SQUA", "RAMP"]:
            raise AttributeError("Invalid modulation type value provided!")
        if not 100 <= mod_freq <= 50000:
            raise AttributeError("Invalid modulation frequency value provided!")
        if (mod == "AM" and not 0 <= mod_depth <= 100) or (mod == "FM" and not 100 <= mod_depth <= 10000):
            raise AttributeError("Invalid modulation depth value provided!")

        if freq == 0 or amp == 0:
            self._conn.write(b':DDS:SWIT 0\n') # Turn off signal generator
            return

        self._conn.write(b':DDS:SWIT 1\n') # Turn on signal generator
        self._conn.write(f':DDS:TYPE {typ}\n'.encode()) # Set signal type
        self._conn.write(f':DDS:FREQ {freq}\n'.encode()) # Set signal frequency
        self._conn.write(f':DDS:AMP {amp}\n'.encode()) # Set signal amplitude
        self._conn.write(f':DDS:OFFS {offset}\n'.encode()) # Set signal offset
        self._conn.write(f':DDS:DUTY {duty}\n'.encode())

        if mod == "NONE":
            self._conn.write(b':DDS:WAVE:MODE 0\n') # Turn modulation off
            return

        self._conn.write(b':DDS:WAVE:MODE 1\n') # Turn modulation on
        self._conn.write(f':DDS:MODE:TYPE {mod}\n'.encode()) # Set modulation type
        self._conn.write(f':DDS:MODE:WAVE:TYPE {mod_typ}\n'.encode()) # Set modulation wave type
        self._conn.write(f':DDS:MODE:FREQ {mod_freq}\n'.encode()) # Set modulation frequency
        self._conn.write(f':DDS:MODE:DEPT {mod_depth}\n'.encode()) # Set modualtion depth/deviation
