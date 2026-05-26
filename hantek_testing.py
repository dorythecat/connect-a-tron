import matplotlib.pyplot as plt

import backend.interfaces.oscilloscope.hantek as hantek

osc = hantek.DSO2D15()

print(f"Frequency: {osc.frequency()} Hz")
print(f"Period: {osc.period()} s")
print(f"RMS: {osc.rms()} V")
print(f"PPK: {osc.ppk()} V")
#ch1 = osc.get_waveform(mode="HRES")
#plt.plot(ch1, 'b')
#plt.show()

freq = range(1000000, 20000000, 1000000)
resp = []
for i in freq:
    osc.set_waveform(freq=i, amp=5)
    resp.append(osc.ppk())
plt.plot(freq, resp)
plt.show()
