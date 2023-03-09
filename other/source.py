import matplotlib.pyplot as plt
import numpy as np

Amp = 5.0
center = 5e6
chirp_coefficient = 1e14
t = np.arange(0, 1.5e-6, 1e-9)

E = Amp*np.cos(2*np.pi*center*t + chirp_coefficient*t**2)
f_t = center+chirp_coefficient*t/np.pi

plt.figure(figsize=(30, 7))

plt.subplot(1,2,1)
plt.plot(t, E)
plt.xlabel('time')
plt.ylabel('Amplitude')

plt.subplot(1,2,2)
plt.plot(t, f_t)
plt.xlabel('time')
plt.ylabel('Frequency')

#plt.show()

src = np.array([t, E])
print(src)
print(src.shape)