import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import time

import interfaces.dmm.dmm as dmm
import interfaces.dmm.keithley as keithley


# Data and display settings
N: int               = 100         # Number of datapoints (set N < 0 for infinite)
REALTIME_GRAPH: bool = True        # Should we plot a real-time graph?
SHOW_GRAPH: bool     = True        # Should we show a graph at the end?
SAVE_GRAPH: bool     = True        # Should we save a graph?
SAVE_DATA: bool      = True        # Should we save the data?
GRAPH_FILE: str      = "graph.png" # Name of the file to save the graph to
DATA_FILE: str       = "data.csv"  # Name of the file to save the data to

times = []                       # Store the time each measurement was taken at (relative to start)
measurements = []                # Store the measurements we're about to take
mpl.rcParams['toolbar'] = 'None' # Disable graph toolbar
plt.style.use('dark_background') # Don't burn my retinas
keith = keithley.Keithley2000()
keith.continuous_set(10, dmm.MType.DC_VOLT)
time.sleep(keith.delay_time)

i = 0
start_time = time.time()
while i != N:
    measurements.append(keith.continuous_get())
    times.append(time.time() - start_time)
    if N > 0:
        i += 1
    plt.plot(times, measurements, color='red')
    if REALTIME_GRAPH:
        plt.pause(keith.delay_time)
    else:
        time.sleep(keith.delay_time)

if SAVE_GRAPH:
    plt.savefig(GRAPH_FILE)

if SHOW_GRAPH:
    plt.show()

if SAVE_DATA:
    np.savetxt(DATA_FILE, np.array((times, measurements)).T, delimiter=',')
