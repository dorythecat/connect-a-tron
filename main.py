import serial

with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
    ser.write(b'*RST\n')
    ser.write(b':MEAS:VOLT:DC?\n')
    print(ser.readline())
