

import numpy as np
import matplotlib.pyplot as plt

R = 5
C = 0e-9
L = 110*1e-9
f = np.linspace(0,20e6,10303)
jw = 1j*2*np.pi*f
S11 = ((1j*2*np.pi*f*L + R) - R) / ((1j*2*np.pi*f*L + R) + R)
S21 = 2 * (R / ( 2*R + 1j*2*np.pi*f*L ))
S21_alt = np.sqrt(1-S11**2 - (1 - S11**2)*(1j*2*np.pi*f*L/(1j*2*np.pi*f*L+R)))
S11db = 20*np.log10(np.abs(S11))
S21db = 20*np.log10(np.abs(S21))
# print(S11db)


zin = R + jw*L
S11_cap = (zin - R) / (zin + R)
plt.figure()
plt.plot(f,20*np.log10(np.abs(S11_cap)))




C = 4.04e-9
L = 105e-9+37e-9
F = 1/(1 + jw*jw*C*L)
plt.figure()
plt.plot(f,F)
plt.show()