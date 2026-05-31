import backend.interfaces.oscilloscope.oscilloscope as oscilloscope

class DSO2D15(oscilloscope.Oscilloscope):
    def __init__(self, port: str = "/dev/usbtmc0") -> None:
        super().__init__(port)

    def __del__(self) -> None:
        super().__del__()

    # Helper functions for the serial connection
    # These don't have any protections or description because they're only meant for internal use
    def _scpi_send(self, command: str) -> None:
        self._conn.write(f'{command}'.encode('unicode_escape'))

    def _scpi_get_bytes(self, command: str, size: int = 4096) -> bytes:
        self._conn.write(command.encode('unicode_escape'))
        return self._conn.read(size)

    def _scpi_get_str(self, command: str, size: int = 8) -> str:
        self._conn.write(command.encode('unicode_escape'))
        return self._conn.read(size).decode('unicode_escape')

    def _scpi_get_float(self, command: str, size: int = 16) -> float:
        self._conn.write(command.encode('unicode_escape'))
        return float(self._conn.read(size).decode('unicode_escape'))

    @property
    def keypad_lock(self) -> bool:
        return self._scpi_get_str(':SYST:LOCK?') == "ON"

    @keypad_lock.setter
    def keypad_lock(self, value: bool) -> None:
        self._scpi_send(f':SYST:LOCK {int(value)}')

    @property
    def trigger_status(self) -> bool:
        return self._scpi_get_str(':TRIG:STAT?') != "NOTRIG"

    def frequency(self, channel: int = 1) -> float:
        """
        Get the frequency of the waveform currently being read by the oscilloscope on the specified channel.

        :param channel: The channel to read data from. (1 or 2)

        :returns: Frequency of the waveform, in Hz.
        :raises AttributeError: If the provided channel is not valid.
        """
        if channel not in [1, 2]:
            raise AttributeError("Invalid channel provided!")

        self._scpi_send(':MEAS:ENAB 1') # Enable measurement
        self._scpi_send(f':MEAS:SOUR CHAN{channel}') # Set the proper source for measurements
        self._scpi_send(':MEAS:ADIS 0') # Turn off dispolay of all of the measurements
        return self._scpi_get_float(f':MEAS:CHAN{channel}:ITEM? FREQ')

    def period(self, channel: int = 1) -> float:
        """
        Get the period of the waveform currently being read by the oscilloscope on the specified channel.

        :param channel: The channel to read data from. (1 or 2)

        :returns: Period of the waveform, in s.
        :raises AttributeError: If the provided channel is not valid.
        """
        if channel not in [1, 2]:
            raise AttributeError("Invalid channel provided!")

        self._scpi_send(':MEAS:ENAB 1') # Enable measurement
        self._scpi_send(f':MEAS:SOUR CHAN{channel}') # Set the proper source for measurements
        self._scpi_send(':MEAS:ADIS 0') # Turn off dispolay of all of the measurements
        return self._scpi_get_float(f':MEAS:CHAN{channel}:ITEM? PERIOD')

    def rms(self, channel: int = 1) -> float:
        """
        Get the RMS voltage of the waveform currently being read by the oscilloscope on the specified channel.

        :param channel: The channel to read data from. (1 or 2)

        :returns: RMS voltage of the waveform, in Hz.
        :raises AttributeError: If the provided channel is not valid.
        """
        if channel not in [1, 2]:
            raise AttributeError("Invalid channel provided!")

        self._scpi_send(':MEAS:ENAB 1') # Enable measurement
        self._scpi_send(f':MEAS:SOUR CHAN{channel}') # Set the proper source for measurements
        self._scpi_send(':MEAS:ADIS 0') # Turn off dispolay of all of the measurements
        return self._scpi_get_float(f':MEAS:CHAN{channel}:ITEM? RMS')

    def ppk(self, channel: int = 1) -> float:
        """https://www.youtube.com/watch?v=oqOlrGPgng8
        Get the RMS voltage of the waveform currently being read by the oscilloscope on the specified channel.

        :param channel: The channel to read data from. (1 or 2)

        :returns: RMS voltage of the waveform, in Hz.
        :raises AttributeError: If the provided channel is not valid.
        """
        if channel not in [1, 2]:
            raise AttributeError("Invalid channel provided!")

        self._scpi_send(':MEAS:ENAB 1') # Enable measurement
        self._scpi_send(f':MEAS:SOUR CHAN{channel}') # Set the proper source for measurements
        self._scpi_send(':MEAS:ADIS 0') # Turn off dispolay of all of the measurements
        return self._scpi_get_float(f':MEAS:CHAN{channel}:ITEM? VPP')

    def force_trigger(self) -> None:
        """
        Force the oscilloscope to be triggered.

        :returns: Nothing.
        """
        self._scpi_send(':TRIG:FORC')

    def time_conf(self, scale: float = 0.0005, offset: float = 0, mode: str = "MAIN", window: bool = False, window_scale: float = 0.0001, window_offset: float = 0) -> None:
        """
        Configures the time domain and all of its associated settings.

        :param scale: The time scale of the oscilloscope, in seconds per division. (0.000000002 <= scale <= 100) (MUST bstart by 1, 2, or 5 (ie, 10ns, 50ms, but NOT 30ms, etc))
        :param offset: The offset of the oscilloscope from the trigger point, in seconds.
        :param mode: The display mode of the oscilloscope. ("MAIN", "XY", or "ROLL")
        :param window: Wether to enable or not the secondary window.
        :param window_scale: The time scale of the secondary window, in seconds per division. See the scale parameter for more info.
        :param window_offset: The offset of the secondary window from the trigger, in seconds.

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        if scale not in [0.000000002, 0.000000005, 0.00000001, 0.00000002, 0.00000005, 0.0000001, 0.0000002, 0.0000005, 0.000001, 0.000002, 0.000005, 0.00001, 0.00002, 0.00005, 0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]:
            raise AttributeError("Invalid scale value provided!")
        if window_scale not in [0.000000002, 0.000000005, 0.00000001, 0.00000002, 0.00000005, 0.0000001, 0.0000002, 0.0000005, 0.000001, 0.000002, 0.000005, 0.00001, 0.00002, 0.00005, 0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]:
            raise AttributeError("Invalid secondary window scale value provided!")
        if mode not in ["MAIN", "XY", "ROLL"]:
            raise AttributeError("Invalid mode value provided!")

        self._scpi_send(f':TIM:SCAL {scale}')
        self._scpi_send(f':TIM:POS {offset}')
        self._scpi_send(f':TIM:MODE {mode}')

        if not window:
            self._scpi_send(':TIM:WIND:ENAB 0')
            return

        self._scpi_send(':TIM:WIND:ENAB 1')
        self._scpi_send(f':TIM:WIND:SCAL {window_scale}')
        self._scpi_send(f':TIM:WIND:POS {window_offset}')

    def channel_conf(self, channel: int = 1, on: bool = True, scale: float = 1, offset: float = 0, probe: int = 1, invert: bool = False, coupling: str = "DC", bw_limit: bool = False) -> None:
        """
        Configures a given channel and all of its associated settings.

        :param channel: The channel to configure. (1 or 2)
        :param on: Wether the channel should be on or off.
        :param scale: The vertical scale of the channel, in Volts per division. The range of the channel will be [-4 * scale, 4 * scale]. (0.001 * probe < scale <= 10 * probe)
        :param offset: The vertical offset of the channel, in Volts. (-50 * probe <= offset <= 50 * probe)
        :param probe: The attenuation factor of the connected probe (1, 10, 50, or 100)
        :param invert: Wether to invert the channel or not.
        :param coupling: Coupling mode of the channel. ("AC", "DC", or "GND")
        :param bw_limit: Wether to activate the 20MHz bandwidth filter for this channel, to filter out high frequency noise.

        :returns: Nothing.
        :raises AttributeError: If any of the provided values is invalid.
        """
        if channel not in [1, 2]:
            raise AttributeError("Invalid channel provided!")
        if probe not in [1, 10, 50, 100]:
            raise AttributeError("Invalid probe value provided!")
        if not 0.001 < (scale / probe) <= 10:
            raise AttributeError("Invalid scale value provided!")
        if not -50 <= (offset / probe) <= 50:
            raise AttributeError("Invalid offset value provided!")
        if coupling not in ["AC", "DC", "GND"]:
            raise AttributeError("Invalid coupling value provided!")

        if not on:
            self._scpi_send(f':CHAN{channel}:DISP 0')
            return

        self._scpi_send(f':CHAN{channel}:DISP 1')
        self._scpi_send(f':CHAN{channel}:PROB {probe}')
        # If the scale is not a usually selectable one, activate vernier mode
        vernier = (scale / probe) not in [0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10]
        self._scpi_send(f':CHAN{channel}:VERN {int(vernier)}')
        self._scpi_send(f':CHAN{channel}:SCAL {scale}V')
        self._scpi_send(f':CHAN{channel}:OFFS {offset}V')
        self._scpi_send(f':CHAN{channel}:COUP {coupling}')
        self._scpi_send(f':CHAN{channel}:BWL {'1' if bw_limit else '0'}')
        self._scpi_send(f':CHAN{channel}:INV {'1' if invert else '0'}')

    def trigger_conf_general(self, mode: str = "AUTO", holdoff: float = 0.000000016) -> None:
        """
        Configures the trigger, regardless of the chosen trigger type.

        :param mode: The triggering mode. ("AUTO", "NORM", or "SING")
        :param holdoff: Trigger holdoff time, aka, trigger recovery time; in seconds. Not relevant when using video, timeout, UART, LIN, CAN, I2C, or SPI trigger modes. (0.000000016 <= holdoff <= 10)

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        if mode not in ["AUTO", "NORM", "SING"]:
            raise AttributeError("Invalid mode value provided!")
        if not 0.000000016 <= holdoff <= 10:
            raise AttributeError("Invalid holdoff value provided!")
        self._scpi_send(f':TRIG:SWE {mode}')
        self._scpi_send(f':TRIG:HOLD {holdoff}')

    def trigger_conf_edge(self, source: int = 1, level: float = 0, slope: str = "RISI") -> None:
        """
        Configures the trigger for edge mode. The trigger will respond when a wave changes from above (or below) the configured level, to below (or above) said level, depending on the configured slope response.

        :param source: Channel to use as source of the signal to trigger with. (1 or 2)
        :param level: Trigger level, in Volts. (abs(level) <= 4 * vert_scale) (see channel_conf)
        :param slope: Wether to trigger on rising, falling, or either slope. ("RISI", "FALL", or "EITH")

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        if source not in [1, 2]:
            raise AttributeError("Invalid source value provided!")
        if slope not in ["RISI", "FALL", "EITH"]:
            raise AttributeError("Invalid slope value provided!")
        # Check this last so we don't waste time if any of the other values are invalid
        if abs(level) > 4 * self._scpi_get_float(f':CHAN{source}:SCAL?'):
            raise AttributeError("Invalid level value provided!")

        self._scpi_send(':TRIG:MODE EDGE')
        self._scpi_send(f':TRIG:EDG:SOUR CHAN{source}')
        self._scpi_send(f':TRIG:EDG:SLOP {slope}')
        self._scpi_send(f':TRIG:EDG:LEV {level}')

    def trigger_conf_pulse(self, source: int = 1, level: float = 0, polarity: bool = True, width: float = 0.0000002, when: str = "GREA") -> None:
        """
        Configures the trigger for pulse mode. The trigger will respond when a pulse is sensed.

        :param source: Channel to use as source of the signal to trigger with. (1 or 2)
        :param level: Trigger level, in Volts. (abs(level) <= 4 * vert_scale) (see channel_conf)
        :param polarity: Polarity of the pulse trigger. True is positive, False is negative.
        :param width: Pulse width to compare against, in seconds. (0.000000008 <= width <= 10)
n hantek_testing.py
        :param when: How to compare the width of the received pulse to the width value provided. ("EQUA", "NEQU", "GREA", or "LESS") (~5% error on comparison)

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        if source not in [1, 2]:
            raise AttributeError("Invalid source value provided!")
        if not 0.000000008 <= width <= 10:
            raise AttributeError("Invalid width value provided!")
        if when not in ["EQUA", "NEQU", "GREA", "LESS"]:
            raise AttributeError("Invalid when value provided!")
        # Check this last so we don't waste time if any of the other values are invalid
        if abs(level) > 4 * self._scpi_get_float(f':CHAN{source}:SCAL?'):
            raise AttributeError("Invalid level value provided!")

        self._scpi_send(b':TRIG:MODE PULS')
        self._scpi_send(f':TRIG:PULS:SOUR CHAN{source}')
        self._scpi_send(f':TRIG:PULS:POL {'POSI' if polarity else 'NEGA'}')
        self._scpi_send(f':TRIG:PULS:WHEN {when}')
        self._scpi_send(f':TRIG:PULS:WID {width}')
        self._scpi_send(f':TRIG:PULS:LEV {level}')

    def trigger_conf_slope(self, source: int = 1, upper_level: float = 2, lower_level: float = -2, polarity: bool = True, width: float = 0.0000002, when: str = "GREA") -> None:
        """
        Configures the trigger for slope mode. The trigger will respond when a slope is sensed.

        :param source: Channel to use as source of the signal to trigger with. (1 or 2)
        :param upper_level: Upper trigger level, in Volts. (abs(upper_level) <= 4 * vert_scale) (see channel_conf)
        :param lower_level: Lower trigger level, in Volts. (abs(lower_level) <= 4 * vert_scale) (see channel_conf)
        :param polarity: Polarity of the slope trigger. True is positive, False is negative.
        :param width: Pulse width to compare against, in seconds. (0.000000008 <= width <= 10)
        :param when: How to compare the width of the received pulse to the width valued provided. ("EQUA", "NEQU", "GREA", or "LESS") (~5% error on comparison)

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        if source not in [1, 2]:
            raise AttributeError("Invalid source value provided!")
        if upper_level <= lower_level:
            raise AttributeError("The upper level value must be greater than the lower level value!")
        if not 0.000000008 <= width <= 10:
            raise AttributeError("Invalid width value provided!")
        if when not in ["EQUA", "NEQU", "GREA", "LESS"]:
            raise AttributeError("Invalid when value provided!")
        #Check this last so we don't waste time if any of the other values are invalid
        vert_scale = 4 * self._scpi_get_float(f':CHAN{source}:SCAL?')
        if abs(upper_level) > vert_scale:
            raise AttributeError("Invalid upper level value provided!")
        if abs(lower_level) > vert_scale:
            raise AttributeError("Invalid lower level value provided!")

        self._scpi_send(':TRIG:MODE SLOP')
        self._scpi_send(f':TRIG:SLOP:SOUR CHAN{source}')
        self._scpi_send(f':TRIG:SLOP:POL {'POSI' if polarity else 'NEGA'}')
        self._scpi_send(f':TRIG:SLOP:WHEN {when}')
        self._scpi_send(f':TRIG:SLOP:WID {width}')
        self._scpi_send(f':TRIG:SLOP:ALEV {upper_level}')
        self._scpi_send(f':TRIG:SLOP:BLEV {lower_level}')

    def trigger_conf_interval(self, source: int = 1, level: float = 0, slope: str = "RISI", time: float = 0.0000002, when: str = "GREA") -> None:
        """
        Configures the trigger for interval mode. The trigger will respond to edges of the specified type that satisfy the chosen compairson against the given time between them.

        :param source: Channel to use as source of the signal to trigger with. (1 or 2)
        :param level: Trigger level, in Volts. (abs(level) <= 4 * vert_scale) (see channel_conf)
        :param slope: Wether to trigger on the rising, falling, or either slope. ("RISI", "FALL", or "DOUB")
        :param time: Time to compare against, in seconds. (0.000000008 <= width <= 10)
        :param when: How to compare the time between slopes against the width value provided. ("EQUA", "NEQU", "GREA", or "LESS")

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        if source not in [1, 2]:
            raise AttributeError("Invalid source value provided!")
        if slope not in ["RISI", "FALL", "DOUB"]:
            raise AttributeError("Invalid slope value provided!")
        if not 0.000000008 <= time <= 10:
            raise AttributeError("Invalid width value provided!")
        if when not in ["EQUA", "NEQU", "GREA", "LESS"]:
            raise AttributeError("Invalid when value provided!")
        # Check this last so we don't waste time if any of the other values are invalid
        if abs(level) > 4 * self._scpi_get_float(f':CHAN{source}:SCAL?'):
            raise AttributeError("Invalid level value provided!")

        self._scpi_send(':TRIG:MODE INT')
        self._scpi_send(f':TRIG:INTERVAL:SOUR CHAN{source}')
        self._scpi_send(f':TRIG:INTERVAL:SLO {slope}')
        self._scpi_send(f':TRIG:INTERVAL:WHEN {when}')
        self._scpi_send(f':TRIG:INTERVAL:TIME {time}')
        self._scpi_send(f':TRIG:INTERVAL:ALEV {level}')

    def trigger_conf_underthrow(self, source: int = 1, upper_level: float = 2, lower_level: float = -2, polarity: bool = True, time: float = 0.0000002, when: str = "GREA") -> None:
        """
        Configures the trigger for underthrow mode. The trigger will respond when the signal triggers the lower level and not the upper level (if polarity is positive), or if it triggers the upper level, and not the lower level (if polarity is negative).

        :param source: Channel to use as source of the signal to trigger with. (1 or 2)
        :param upper_level: Upper trigger level, in Volts. (abs(upper_level) <= 4 * vert_scale) (see channel_conf)
        :param lower_level: Lower trigger level, in Volts. (abs(lower_level) <= 4 * vert_scale) (see channel_conf)
        :param polarity: Polarity of the trigger. True is positivhttps://www.youtube.com/watch?v=oqOlrGPgng8e, False is negative.
        :param time: Time to compare against, in seconds. (0.000000008 <= time <= 10)
        :param when:: How to compare the time value provided againt the signal. ("EQUA", "NEQU", "GREA", or "LESS")

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        if source not in [1, 2]:
            raise AttributeError("Invalid source value provided!")
        if upper_level <= lower_level:
            raise AttributeError("The upper level value must be greater than the lower level value!")
        if not 0.000000008 <= time <= 10:
            raise AttributeError("Invalid time value provided!")
        if when not in ["EQUA", "NEQU", "GREA", "LESS"]:
            raise AttributeError("Invalid when value provided!")
        # Check this last so we don't waste time if any of the other values are invalid
        vert_scale = 4 * self._scpi_get_float(f':CHAN{source}:SCAL?')
        if abs(upper_level) > vert_scale:
            raise AttributeError("Invalid upper level value provided!")
        if abs(lower_level) > vert_scale:
            raise AttributeError("Invalid lower level value provided!")

        self._scpi_send(':TRIG:MODE UND')
        self._scpi_send(f':TRIG:UNDER_A:SOUR CHAN{source}')
        self._scpi_send(f':TRIG:UNDER_A:POL {'POSI' if polarity else 'NEGA'}')
        self._scpi_send(f':TRIG:UNDER_A:WHEN {when}')
        self._scpi_send(f':TRIG:UNDER_A:TIME {time}')
        self._scpi_send(f':TRIG:UNDER_A:ALEV {upper_level}')
        self._scpi_send(f':TRIG:UNDER_A:BLEV {lower_level}')

    def trigger_conf_timeout(self, source: int = 1, level: float = 0, polarity: bool = True, width: float = 0.0000002) -> None:
        """
        Configures the trigger for timeout (also known as overtime or dropout) mode. The trigger will respond when the signal has an edge spaced by a time lesser or equal to the specified width.

        :param source: Channel to use as source of the signal to trigger with. (1 or 2)
        :param level: Trigger level, in Volts. (abs(level) <= 4 * vert_scale) (see channel_conf)
        :param polarity: Polarity of the trigger. True is positive, False is negative.
        :param width: Maximum spacing between two triggering edges, in seconds. (0.000000008 <= width <= 10)

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        if source not in [1, 2]:
            raise AttributeError("Invalid source value provided!")
        if not 0.000000008 <= width <= 10:
            raise AttributeError("Invalid width value provided!")
        # Check this last so we don't waste time if any of the other values are invalid
        if abs(level) > 4 * self._scpi_get_float(f':CHAN{source}:SCAL?'):
            raise AttributeError("Invalid level value provided!")

        self._scpi_send(':TRIG:MODE TIM')
        self._scpi_send(f':TRIG:TIM:SOUR CHAN{source}')
        self._scpi_send(f':TRIG:TIM:LEV {level}')
        self._scpi_send(f':TRIG:TIM:WID {width}')
        self._scpi_send(f':TRIG:TIM:POL {'POSI' if polarity else 'NEGA'}')

    def trigger_conf_window(self, source: int = 1, upper_level: float = 2, lower_level: float = -2) -> None:
        """
        Configures the trigger for window mode. The trigger will respond when the signal is within the upper or lower trigger level.

        :param source: Channel to use as source of the signal to trigger with. (1 or 2)
        :param upper_level: Upper trigger level, in Volts. (abs(upper_level) <= 4 * vert_scale) (see channel_conf)
        :param lower_level: Lower trigger level, in Volts. (abs(lower_level) <= 4 * vert_scale) (see channel_conf)

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        if source not in [1, 2]:
            raise AttributeError("Invalid source value provided!")
        if upper_level <= lower_level:
            raise AttributeError("The upper level value must be greater than the lower level value!")
        # Check this last so we don't waste time if any of the other values are invalid
        vert_scale = 4 * self._scpi_get_float(f':CHAN{source}:SCAL?')
        if abs(upper_level) > vert_scale:
            raise AttributeError("Invalid upper level value provided!")
        if abs(lower_level) > vert_scale:
            raise AttributeError("Invalid lower level value provided!")

        self._scpi_send(':TRIG:MODE WIN')
        self._scpi_send(f':TRIG:WINDO:SOUR CHAN{source}')
        self._scpi_send(f':TRIG:WINDO:ALEV {upper_level}')
        self._scpi_send(f':TRIG:WINDO:BLEV {lower_level}')

    def trigger_conf_pattern(self, pattern: str = "R,X", levels: str = "1,0;2,0") -> None:
        """
        Configures the trigger for pattern mode. The trigger will respond if all conditions given are met. See parameter description on how to pass these conditions.

        :param pattern: Two letters, comma-separated, indicating what the pattern should be. First letter is channel one, second letter is channel 2. "X" ignores the channel, "L" triggers when low, "H" triggers when high, "F" triggers on falling edge, "R" triggers on rising edge, and "D" triggers on either falling or rising edge.
        :param levels: Channel trigger levels, in Volts. Following the scheme: "1,0.16;2,0". (abs(level) <= 4 * vert_scale) (see channel_conf)

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        pattern_list: list[str] = pattern.split(",")
        levels_list: list[str] = levels.split(";")
        if len(pattern_list) != 2:
            raise AttributeError("Invalid pattern value provided! Exactly two channels must be provided!")
        for p in pattern_list:
            if p.strip() not in ["X", "L", "H", "F", "R", "D"]:
                raise AttributeError(f"Invalid pattern value provided! \"{p.strip()}\" is not an allowed setting!")
        # Check this last so we don't waste time if any of the other values are invalid
        for channel in [1, 2]:
            if abs(levels_list[channel - 1][1]) > 4 * self._scpi_get_float(f':CHAN{source}:SCAL?'):
                raise AttributeError(f"Invalid levels value provided! Channel {channel}'s level is out of range!")
        self._scpi_send(':TRIG:MODE PATT')
        self._scpi_send(f':TRIG:PATT:PATT {pattern}')
        for channel in [0, 1]:
            self._scpi_send(f':TRIG:PATT:LEV CHAN{levels_list[channel]}')

    def trigger_conf_video(self, source: int = 1, level: float = 0, polarity: bool = True, standard: str = "PAL", mode: str = "ALIN", line: int = 1) -> None:
        """
        Configures the trigger for video (also known as TV) mode. The trigger will respond when it detects a PAL/NTSC (depending on configured mode) television broadcast signal on the chosen channel.

        :param source: Channel to use as source of the signal to trigger with. (1 or 2)
        :param level: Trigger level, in Volts. (abs(level) <= 4 * vert_scale) (see channel_conf)
        :param polarity: Polarity of the trigger signal. True is positive, False is negative.
        :param standard: What video standard to use. ("NTSC" or "PAL")
        :param mode: What trigger mode to use. ("ALIN", "LINE", "FIE1", or "FIE2")
        :param line: What line to trigger on, when on line mode. (1 <= line <= (525 if NTSC, 625 if PAL))

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        if source not in [1, 2]:
            raise AttributeError("Provided source value is invalid!")
        if standard not in ["NTSC", "PAL"]:
            raise AttributeError("Provided standard value is invalid!")
        if mode not in ["ALIN", "LINE", "FIE1", "FIE2"]:
            raise AttributeError("Provided mode value is invalid!")
        if not 1 <= line <= (525 if standard == "NTSC" else 625):
            raise AttributeError("Provided line value is invalid!")
        # Check this last so we don't waste time if any of the other values are invalid
        if abs(level) > 4 * self._scpi_get_float(f':CHAN{source}:SCAL?'):
            raise AttributeError("Invalid level value provided!")

        self._scpi_send(':TRIG:MODE TV')
        self._scpi_send(f':TRIG:TV:SOUR CHAN{source}')
        self._scpi_send(f':TRIG:TV:POL {'POSI' if polarity else 'NEGA'}')
        self._scpi_send(f':TRIG:TV:MODE {mode}')
n hantek_testing.py
        self._scpi_send(f':TRIG:TV:STAN {standard}')
        self._scpi_send(f':TRIG:VID:LEV {level}')
        if mode == "LINE":
            self._scpi_send(':TRIG:TV:LINE {line}')

    def trigger_conf_uart(self, source: int = 1, level: float = 0, width: int = 8, baud_rate: int = 9600, parity: str = "NONE", data: int = 0xff, condition: str = "START") -> None:
        """
        Configures the trigger for UART mode. The trigger will respond to UART data sent on the selected channel.

        :param source: Channel to use as source of the signal to trigger with. (1 or 2)
        :param level: Trigger level, in Volts. (abs(level) <= 4 * vert_scale) (see channel_conf)
        :param width: Data width, in bits. (5, 6, 7, 8)
        :param baud_rate: Baud rate of the UART communication, in bits per second. 0 for "USER" setting. (0, 110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 230400, 380400, 460400, or 921600)
        :param parity: Parity bit setting. ("NONE", "ODD", or "EVEN")
        :param data: Data to trigger at when trigger mode is "READ_DATA". (0 <= data <= 2^(width - 1) - 1)
        :param condition: Trigger condition. ("START", "STOP", "READ_DATA", "PARITY_ERR", or "COM_ERR")

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        if source not in [1, 2]:
            raise AttributeError("Provided source value is invalid!")
        if width not in [5, 6, 7, 8]:
            raise AttributeError("Provided width value is invalid!")
        if baud_rate not in [0, 110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 230400, 380400, 464400, 921600]:
            raise AttributeError("Provided baud rate value is invalid!")
        if parity not in ["NONE", "ODD", "EVEN"]:
            raise AttributeError("Provided parity value is invalid!")
        if not 0 <= data <= 2**(width - 1) - 1:
            raise AttributeError("Provided data value is invalid!")
        if condition not in ["START", "STOP", "READ_DATA", "PARITY_ERR", "COM_ERR"]:
            raise AttributeError("Provided condition value is invalid!")
        # Check this last so we don't waste time if any of the other values are invalid
        if abs(level) > 4 * self._scpi_get_float(f':CHAN{source}:SCAL?'):
            raise AttributeError("Invalid level value provided!")

        self._scpi_send(':TRIG:MODE UART')
        self._scpi_send(f':TRIG:UART:SOUR CHAN{source}')
        self._scpi_send(f':TRIG:UART:COND {condition}')
        self._scpi_send(f':TRIG:UART:BAU {'USER' if baud_rate == 0 else baud_rate}')
        self._scpi_send(f':TRIG:UART:ALEV {level}')
        if condition == "READ_DATA":
            self._scpi_send(f':TRIG:UART:DATA {data}')
        elif condition in ["PARITY_ERR", "COM_ERR"]:
            self._scpi_send(f':TRIG:UART:WIDT {width}')
            self._scpi_send(f':TRIG:UART:PARI {parity}')

    def trigger_conf_spi(self, source_sda: int = 1, source_scl: int = 2, level_sda: float = 0, level_scl: float = 0, clock_edge: bool = True, width: int = 8, data: int = 0xff, mask: int = 0) -> None:
        """
        Configures the trigger for SPI mode. The trigger will respond to SPI data sent on the selected channels.

        :param source_sda: Channel to use as source of the data signal. (1 or 2)
        :param source_scl: Channel to use as source of the clock signal. (1 or 2)
        :param level_sda: Trigger level of the data signal. (abs(level_sda) <= 4 * vert_scale) (see channel_conf)
        :param level_scl: Trigger level of the clock signal. (abs(level_scl) <= 4 * vert_scale) (see channel_conf)
        :param clock_edge: Type of clock edge triggered by SPI. True means rising, False means falling.
        :param width: Bit width of the SPI signal. (4 <= width <= 32)
        :param data: Data value to trigger to. (0 <= data <= 4294967295)
        :param mask: Mask to trigger to. (0 <= mask <= 4294967295)

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        if source_sda not in [1, 2]:
            raise AttributeError("Invalid data source value provided!")
        if source_scl not in [1, 2]:
            raise AttributeError("Invalid clock source value provided!")
        if source_sda == source_scl:
            raise AttributeError("Data and clock source channels can't be the same!")
        if not 4 <= width <= 32:
            raise AttributeError("Invalid width value provided!")
        if not 0 <= data <= 4294967295:
            raise AttributeError("Invalid data value provided!")
        if not 0 <= mask <= 4294967295:
            raise AttributeError("Invalid mask value provided!")
        # Check this last so we don't waste time if any of the other values are invalid
        if abs(level_sda) > 4 * self._scpi_get_float(f':CHAN{source_sda}:SCAL?'):
            raise AttributeError("Invalid data level value provided!")
        if abs(level_scl) > 4 * self. _scpi_get_float(f':CHAN{source_scl}:SCAL?'):
            raise AttributeError("Invalid clock level value provided!")

        self._scpi_send(':TRIG:MODE SPI')
        self._scpi_send(f':TRIG:SPI:SDA:SOUR CHAN{source_sda}')
        self._scpi_send(f':TRIG:SPI:SCL:SOUR CHAN{source_scl}')
        self._scpi_send(f':TRIG:SPI:SCK {'R' if clock_edge else 'F'}')
        self._scpi_send(f':TRIG:SPI:WID {width}')
        self._scpi_send(f':TRIG:SPI:DATA {data}')
        self._scpi_send(f':TRIG:SPI:MASK {mask}')
        self._scpi_send(f':TRIG:SPI:ALEV {level_scl}')
        self._scpi_send(f':TRIG:SPI:BLEV {level_sda}')

    def trigger_conf_i2c(self, source_sda: int = 1, source_scl: int = 2, level_sda: float = 0, level_scl: float = 0, address: int = 0x3f, data: int = 0xff, data_index: int = 0, condition: str = "START") -> None:
        """
        Configures the trigger for I2C mode. The trigger will respond to I2C data sent on the selected channels.

        :param source_sda: Channel to use as source of the data signal. (1 or 2)
        :param source_scl: Channel to use as source of the clock signal. (1 or 2)
        :param level_sda: Trigger level of the data signal. (abs(level_sda) <= 4 * vert_scale) (see channel_conf)
        :param level_scl: Trigger level of the clock signal. (abs(level_scl) <= 4 * vert_scale) (see channel_conf)
        :param address: The I2C adress on which the trigger will respond. (0 <= address <= 255)
        :param data: The data on which the trigger will respond. (0 <= data <= 255)
        :param data_index: The index of the I2C data. (0 <= data_index <= 8)
        :param condition: The condition under which to trigger. ("START", "STOP", "ACK_LOST", "ADDR_NO_ACK", "RESTART", or "READ_DATA")

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        if source_sda not in [1, 2]:
            raise AttributeError("Invalid data source value provided!")
        if source_scl not in [1, 2]:
            raise AttributeError("Invalid clock source value provided!")
        if source_sda == source_scl:
            raise AttributeError("Data and clock source channels can't be the same!")
        if not 0 <= address <= 255:
            raise AttributeError("Invalid address value provided!")
        if not 0 <= data <= 255:
            raise AttributeError("Invalid data value provided!")
        if not 0 <= data_index <= 8:
            raise AttributeError("Invalid data index value provided!")
        if condition not in ["START", "STOP", "ACK_LOST", "ADDR_NO_ACK", "RESTART", "READ_DATA"]:
            raise AttributeError("Invalid condition value provided!")
        # Check this last so we don't waste time if any of the other values are invalid
        if level_sda > 4 * self._scpi_get_float(f':CHAN{source_sda}:SCAL?'):
            raise AttributeError("Invalid data level value provided!")
        if level_scl > 4 * self._scpi_get_float(f':CAN{source_scl}:SCAL?'):
            raise AttributeError("Invalid clock level value provided!")

        self._scpi_send(':TRIG:MODE IIC')
        self._scpi_send(f':TRIG:IIC:SDA:SOUR CHAN{source_sda}')
        self._scpi_send(f':TRIG:IIC:SCL:SOUR CHAN{source_scl}')
        self._scpi_send(f':TRIG:IIC:CON {condition}')
        self._scpi_send(f':TRIG:IIC:ALEV {level_scl}')
        self._scpi_send(f':TRIG:IIC:BLEV {level_sda}')
        if condition in ["ADDR_NO_ACK", "READ_DATA"]:
            self._scpi_send(f':TRIG:IIC:ADD {address}')
        if condition == "READ_DATA":
            self._scpi_send(f':TRIG:IIC:DATA {data_index},{data}')

    def trigger_conf_can(self, source: int = 1, level: float = 0, baud_rate: int = 125000, idle: bool = True, identifier: int = 0, data_len: int = 0, data: int = 0xff, data_index: int = 0, condition: str = "FRAM_STARE") -> None:
        """
        Configures the trigger for CAN mode. The trigger will respond to CAN data sent on the specified channel.

        :param source: Channel to use as source of the data. (1 or 2)
        :param level: Trigger level of the channel. (abs(level) <= 4 * vert_scale) (see channel_conf)
        :param baud_rate: The baud rate of the CAN bus. Use 0 for "USER" setting. (0, 10000, 20000, 33300, 50000, 62500, 83300, 100000, 125000, 250000, 500000, 800000, or 1000000)
        :param idle: The idle level of the CAN bus. True is high, False is low.
        :param identifier: The identifier to trigger to. (0 <= identifier <= 28)
        :param data_len: The data length code of the CAN bus. (0 <= data_len <= 15)
        :param data: The data to trigger to. (0 <= data <= 255)
        :param data_index: Index of the data. (0 <= data_index <= 3)
        :param condition: The condition  to trigger under. ("FRAM_STARE", "FRAM_REMO_ID", "FRAM_DATA_ID", "REMO", "DATA", "FRAM_REMO_ID_EXT", "FRAM_DATA_ID_EXT", "FRAM_REE", "FRAM_OVERLOAD", "ERR_ALL", or "ACK_ERR")

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        if source not in [1, 2]:
            raise AttributeError("Invalid source value provided!")
        if baud_rate not in [0, 10000, 20000, 33300, 50000, 62500, 83300, 100000, 125000, 250000, 500000, 800000, 1000000]:
            raise AttributeError("Invalid baud rate value provided!")
        if not 0 <= identifier <= 28:
            raise AttributeError("Invalid identifier value provided!")
        if not 0 <= data_len <= 15:
            raise AttributeError("Invalid data length value provided!")
        if not 0 <= data <= 255:
            raise AttributeError("Invalid data value provided!")
        if not 0 <= data_index <= 3:
            raise AttributeError("Invalid data index value provided!")
        if condition not in ["FRAM_STARE", "FRAM_REMO_ID", "FRAM_DATA_ID", "REMO", "DATA", "FRAM_REMO_ID_EXT", "FRAM_REE", "FRAM_OVERLOAD", "ERR_ALL", "ACK_ERR"]:
            raise AttributeError("Invalid condition value provided!")
        # Check this last so we don't waste time if any of the other values are invalid
        if abs(level) > 4 * self._scpi_get_float(f':CHAN{source}:SCAL?'):
            raise AttributeError("Invalid level value provided!")

        self._scpi_send(':TRIG:MODE CAN')
        self._scpi_send(f':TRIG:CAN:SOUR CHAN{source}')
        self._scpi_send(f':TRIG:CAN:IDL {'HIGH' if idle else 'LOW'}')
        self._scpi_send(f':TRIG:CAN:BAU {'USER' if baud_rate == 0 else baud_rate}')
        self._scpi_send(f':TRIG:CAN:CON {condition}')
        self._scpi_send(f':TRIG:CAN:ID {identifier}')
        self._scpi_send(f':TRIG:CAN:DLC {data_len}')
        self._scpi_send(f':TRIG:CAN:DATA {data_index},{data}')
        self._scpi_send(f':TRIG:CAN:ALEV {level}')

    def trigger_conf_lin(self, source: int = 1, level: float = 0, baud_rate: int = 115200, idle: bool = True, identifier: int = 0, data: int = 0xff, data_index: int = 0, condition: str = "IDENTIFIER") -> None:
        """
        Configures the trigger for LIN mode. The trigger will respond to LIN data sent on the specified channel.

        :param source: Channel to use as source of the data. (1 or 2)
        :param level: Trigger level of the channle. (abs(level) <= 4 * vert_scale) (see channel_conf)
        :param baud_rate: Baud rate of the LIN data. Use 0 for "USER" setting. (0, 110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 230400, 380400, 460400, or 921600)
        :param idle: Idle level triggered by LIN bus. True for high, False for low.
        :param identifier: Identifier to trigger to. (0 <= identifier <= 63)
        :param data: Data to trigger to. (0 <= data <= 255)
        :param data_index: Data index of data. (0 <= data_index <= 3)
        :param condition: Condition to trigger to. ("INTERVAL_FIELD", "SYNC_FIELD", "ID_FIELD", "DATA", "IDENTIFIER", or "ID_DATA")

        :returns: Nothing.
        :raises AttributeError: If any of the provided values are invalid.
        """
        if source not in [1, 2]:
            raise AttributeError("Invalid source value provided!")
        if baud_rate not in [0, 110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 230400, 380400, 460400, 921600]:
            raise AttributeError("Invalid baud rate value provided!")
        if not 0 <= identifier <= 63:
            raise AttributeError("Invalid identifier value provided!")
        if not 0 <= data <= 255:
            raise AttributeError("Invalid data value provided!")
        if not 0 <= data_index <= 3:
            raise AttributeError("Invalid data index value provided!")
        if condition not in ["INTERVAL_FIELD", "SYNC_FIELD", "ID_FIELD", "DATA", "IDENTIFIER", "ID_DATA"]:
            raise AttributeError("Invalid condition value provided!")
        # Check this last so we don't waste time if any of the other values are invalid
        if abs(level) > 4 * self._scpi_get_float(f':CHAN{source}:SCAL?'):
            raise AttributeError("Invalid level value provided!")

        self._scpi_send(':TRIG:MODE LIN')
        self._scpi_send(f':TRIG:LIN:SOUR CHAN{source}')
        self._scpi_send(f':TRIG:LIN:IDL {'HIGH' if idle else 'LOW'}')
        self._scpi_send(f':TRIG:LIN:BAU {'USER' if baud_rate == 0 else baud_rate}')
        self._scpi_send(f':TRIG:LIN:CON {condition}')
        self._scpi_send(f':TRIG:LIN:ID {identifier}')
        self._scpi_send(f':TRIG:LIN:DATA {data_index},{data}')
        self._scpi_send(f':TRIG:LIN:ALEV {level}')

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

        self._scpi_send(':CHAN1:DISP 1') # Make sure channel 1 is enabled (we don't care about the status of channel 2)
        self._scpi_send(f':ACQ:POIN {points}')
        self._scpi_send(f':ACQ:TYPE {mode}')
        if mode == "AVER":
            self._scpi_send(f':ACQ:COUN {samples}')

        data: str = self._scpi_get_str(':WAV:DATA:ALL?', 128) # Query header
        if data[:2] != "#9":
            raise RuntimeError("Response header is corrupted or invalid!")
        offset = float(data[31:35])
        voltage = float(data[47:53])
        counter = int(data[11:20]) - int(data[2:11]) # Total size of the packages to receive, minus this package
        channel_counter = points
        out: list[float] = []
        while counter > 0:
            data: str = self._scpi_get_bytes(':WAV:DATA:ALL?', 4029)
            if data[:2] != b'#9':
                raise RuntimeError("Response header is corrupted or invalid!")
            packet_size = int(data[2:11])
            counter -= packet_size
            if channel_counter < 0:
                continue # Don't read channel 2 data
            for i in range(29, len(data)):
                val = int(data[i])
                val = val if val <= 127 else val - 256 # Handle negative numbers
                out.append((val - offset) * voltage)
            channel_counter -= packet_size
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
            self._scpi_send(':DDS:SWIT 0')
            return

        self._scpi_send(':DDS:SWIT 1')
        self._scpi_send(f':DDS:TYPE {typ}')
        self._scpi_send(f':DDS:FREQ {freq}')
        self._scpi_send(f':DDS:AMP {amp}')
        self._scpi_send(f':DDS:OFFS {offset}')
        self._scpi_send(f':DDS:DUTY {duty}')

        if mod == "NONE":
            self._scpi_send(':DDS:WAVE:MODE 0')
            return

        self._scpi_send(':DDS:WAVE:MODE 1')
        self._scpi_send(f':DDS:MODE:TYPE {mod}')
        self._scpi_send(f':DDS:MODE:WAVE:TYPE {mod_typ}')
        self._scpi_send(f':DDS:MODE:FREQ {mod_freq}')
        self._scpi_send(f':DDS:MODE:DEPT {mod_depth}')
