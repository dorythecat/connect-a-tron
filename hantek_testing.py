fd = open("/dev/usbtmc0", "r+b", buffering=0)

fd.write(b'*IDN?\n')

print(fd.read(1024))
