import matplotlib.pyplot as plt

import backend.interfaces.oscilloscope.hantek as hantek

osc = hantek.DSO2D15()

print(f"Frequency: {osc.frequency()} Hz")
print(f"Period: {osc.period()} s")
print(f"RMS: {osc.rms()} V")
print(f"PPK: {osc.ppk()} V")
ch1 = osc.get_waveform(mode="HRES")
plt.plot(ch1, 'b')
plt.show()
