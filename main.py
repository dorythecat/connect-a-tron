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

# Measurement Settings
# TODO: Make these configurable from the command-line/UI
PLF: int    = 50                # Frequency of the powerline, in Hertz
NPLC: float = 10                # Number of powerline cycles between measurements
N: int      = 100               # Number of measurements to take (Set to -1 for infinite)
TYPE: MType = MType.DC_VOLTAGE  # Type of the measurement to take

# Data and display settings
REALTIME_GRAPH: bool = True        # Should we plot a real-time graph?
SHOW_GRAPH: bool     = True        # Should we show a graph at the end?
SAVE_GRAPH: bool     = True        # Should we save a graph?
SAVE_DATA: bool      = True        # Should we save the data?
GRAPH_FILE: str      = "graph.png" # Name of the file to save the graph to
DATA_FILE: str       = "data.csv"  # Name of the file to save the data to

# Stuff that needs to be generated from settings above
DELAY_TIME = 1.5 * (NPLC / PLF) # Multiply by 1.5 to give a good margin

times = []                       # Store the time each measurement was taken at (relative to start)
measurements = []                # Store the measurements we're about to take
mpl.rcParams['toolbar'] = 'None' # Disable graph toolbar
plt.style.use('dark_background') # Don't burn my retinas
with serial.Serial('/dev/ttyUSB0', 9600, timeout=3) as ser:
    ser.write(b'*RST\n') # Reset everything
    ser.write(f':SENS:FUNC "{TYPE.value}"\n'.encode()) # Set type of measurement to DC voltage
    ser.write(f':SENS:VOLT:DC:NPLC {NPLC}\n'.encode()) # Set measurements to the highest sampling rate
    ser.write(b':INIT:CONT ON\n') # Continuously sample data
    time.sleep(DELAY_TIME) # Make sure the first measurement has had time to settle

    i = 0
    start_time = time.time()
    while i != N:
        ser.write(b':SENS:DATA?\n') # Take a measurement
        measurements.append(float(ser.readline()))
        times.append(time.time() - start_time)
        if N > 0:
            i += 1
        plt.plot(times, measurements, color='red')
        if REALTIME_GRAPH:
            plt.pause(DELAY_TIME)
        else:
            time.sleep(DELAY_TIME)

if SAVE_GRAPH:
    plt.savefig(GRAPH_FILE)

if SHOW_GRAPH:
    plt.show()

if SAVE_DATA:
    np.savetxt(DATA_FILE, np.array((times, measurements)).T, delimiter=',')
