import serial
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import time
from enum import Enum

# TODO: Make this a bit cleaner
class MType(Enum):
    DC_VOLTAGE  = "VOLT:DC"
    AC_VOLTAGE  = "VOLT:AC"
    DC_CURRENT  = "CURR:DC"
    AC_CURRENT  = "CURR:AC"
    RESISTANCE  = "RES"
    KELVIN_RES  = "FRES" # 4-wire resistance
    PERIOD      = "PER"
    TEMPERATURE = "TEMP"
    DIODE       = "DIOD"
    CONTINUITY  = "CONT"

# Settings
# TODO: Make these configurable from the command-line/UI
PLF: int    = 50                # Frequency of the powerline, in Hertz
NPLC: float = 10                # Number of powerline cycles between measurements
N: int      = 100               # Number of measurements to take (Set to -1 for infinite)
TYPE: MType = MType.DC_VOLTAGE  # Type of the measurement to take

# Auto-generated values from settings above
DELAY_TIME = 1.5 * (NPLC / PLF) # Multiply by 1.5 to give a good margin

xs = []
ys = []
mpl.rcParams['toolbar'] = 'None' # Disable graph toolbar
plt.style.use('dark_background') # Don't burn my retinas
with serial.Serial('/dev/ttyUSB0', 9600, timeout=3) as ser:
    ser.write(b'*RST\n') # Reset everything
    ser.write(f':SENS:FUNC "{TYPE.value}"\n'.encode()) # Set type of measurement to DC voltage
    ser.write(f':SENS:VOLT:DC:NPLC {NPLC}\n'.encode()) # Set measurements to the highest sampling rate
    ser.write(b':INIT:CONT ON\n') # Continuously sample data
    time.sleep(DELAY_TIME)

    i = 0
    while i != N:
        xs.append(i)
        ser.write(b':SENS:DATA?\n') # Take a measuremeny
        y = float(ser.readline())
        ys.append(y)
        plt.plot(xs,ys,color='red')
        if N > 0:
            i += 1
        plt.pause(DELAY_TIME) # Wait for the next measurement to be properly taken

plt.show()
