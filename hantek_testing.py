import matplotlib.pyplot as plt

import backend.interfaces.oscilloscope.hantek as hantek

osc = hantek.DSO2D15()

plt.plot(osc.get_waveform())
plt.show()
