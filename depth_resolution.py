from cProfile import label

import matplotlib.pyplot as plt
import numpy as np

#誘電率
epsilon1 = 4.0
epsilon2 = 5.0
epsilon3 = 6.0

#光速
c = 299792458 # [m/s]


f0 = np.arange(1, 200, 0.1) # 中心周波数

dR1 = c / (2*np.sqrt(epsilon1) * f0 *10**6 * 0.5)
dR2 = c / (2*np.sqrt(epsilon2) * f0 *10**6 * 0.5)
dR3 = c / (2*np.sqrt(epsilon3) * f0 *10**6 * 0.5)


#描画
plt.figure(figsize=(25, 16))
plt.subplot(2, 3, 1)
plt.plot(f0, dR1, label=r'$\varepsilon _r = 4.0$')
#plt.plot(f0, dR2, label=r'$\varepsilon_r = 5.0$')
#plt.plot(f0, dR3, label=r'$\varepsilon_r = 6.0$')

plt.title(' (a) Depth Resolution (Overview)', fontsize=24)
plt.xlabel('Center Frequency [MHz]', fontsize=20)
plt.ylabel('Depth Resolution [m]', fontsize=20)
plt.tick_params(labelsize=20)
plt.yscale('log')
plt.grid()


plt.subplot(2, 3, 4)
plt.plot(f0, dR1, label=r'$\varepsilon _r = 4.0$')

plt.title('(b) Depth Resolution (Detail of 1-10 MHz)', fontsize=24)
plt.xlabel('Center Frequency [MHz]', fontsize=20)
plt.ylabel('Depth Resolution [m]', fontsize=20)
plt.tick_params(labelsize=20)
plt.xlim(1, 10)
plt.grid()

plt.subplot(2, 3, 5)
plt.plot(f0, dR1, label=r'$\varepsilon _r = 4.0$')

plt.title('(c) Depth Resolution (Detail of 10-75 MHz)', fontsize=24)
plt.xlabel('Center Frequency [MHz]', fontsize=20)
plt.ylabel('Depth Resolution [m]', fontsize=20)
plt.tick_params(labelsize=20)
plt.xlim(10, 75)
plt.ylim(0, 20)
plt.grid()


plt.subplot(2, 3, 6)
plt.plot(f0, dR1, label=r'$\varepsilon _r = 4.0$')

plt.title('(d) Depth Resolution (Detail of 75-200 MHz)', fontsize=24)
plt.xlabel('Center Frequency [MHz]', fontsize=20)
plt.ylabel('Depth Resolution [m]', fontsize=20)
plt.tick_params(labelsize=20)
plt.xlim(75, 200)
plt.ylim(0, 2.5)
plt.grid()

#グラフの体裁
#plt.legend(fontsize='10')
#plt.savefig('output_resolution/Depth_resolutin.png')

#plt.subplots_adjust(wspace=2.0)

plt.show()