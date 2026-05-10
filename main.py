import serial
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import time

xs = []
ys = []
mpl.rcParams['toolbar'] = 'None' # Disable graph toolbar
plt.style.use('dark_background') # Don't burn my retinas
with serial.Serial('/dev/ttyUSB0', 9600, timeout=3) as ser:
    ser.write(b'*RST\n') # Reset everything
    ser.write(b':SENS:FUNC "VOLT:DC"\n') # Set type of measurement to DC voltage
    ser.write(b':SENS:VOLT:DC:NPLC 10\n') # Set measurements to the highest sampling rate
    ser.write(b':INIT:CONT ON\n')
    time.sleep(0.3)
    for i in range(100):
        xs.append(i)
        ser.write(b':SENS:DATA?\n') # Take a measurement
        y = float(ser.readline())
        ys.append(y)
        plt.plot(xs,ys,color='red')
        plt.pause(0.3) # Wait a bit before taking next measurement

plt.show()
