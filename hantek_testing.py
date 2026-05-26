import matplotlib.pyplot as plt

import backend.interfaces.oscilloscope.hantek as hantek

osc = hantek.DSO2D15()

ch1 = osc.get_waveform(mode="HRES")
plt.plot(ch1, 'b')
plt.show()
