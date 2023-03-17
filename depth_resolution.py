from cProfile import label

import matplotlib.pyplot as plt
import numpy as np

#誘電率
epsilon1 = 4.0
epsilon2 = 5.0
epsilon3 = 6.0

#光速
c = 299792458 # [m/s]


f0 = np.arange(1, 200) # 中心周波数

dR1 = c / (2*np.sqrt(epsilon1) * f0*10**6)
dR2 = c / (2*np.sqrt(epsilon2) * f0*10**6)
dR3 = c / (2*np.sqrt(epsilon3) * f0*10**6)


#描画
plt.figure(figsize=(25, 7))
plt.subplot(1, 3, 1)
plt.plot(f0, dR1, label=r'$\varepsilon _r = 4.0$')
#plt.plot(f0, dR2, label=r'$\varepsilon_r = 5.0$')
#plt.plot(f0, dR3, label=r'$\varepsilon_r = 6.0$')

plt.title('Depth Resolution', fontsize=20)
plt.xlabel('Center Frequency [MHz]', fontsize=15)
plt.ylabel('Depth Resolution [m]', fontsize=15)
plt.tick_params(labelsize=15)
plt.yscale('log')
plt.grid()


plt.subplot(1, 3, 2)
plt.plot(f0, dR1, label=r'$\varepsilon _r = 4.0$')

plt.title('Depth Resolution (1 ~ 10 MHz)', fontsize=20)
plt.xlabel('Center Frequency [MHz]', fontsize=15)
plt.ylabel('Depth Resolution [m]', fontsize=15)
plt.tick_params(labelsize=15)
plt.xlim(1, 10)
plt.grid()


plt.subplot(1, 3, 3)
plt.plot(f0, dR1, label=r'$\varepsilon _r = 4.0$')

plt.title('Depth Resolution (75 ~ MHz)', fontsize=20)
plt.xlabel('Center Frequency [MHz]', fontsize=15)
plt.ylabel('Depth Resolution [m]', fontsize=15)
plt.tick_params(labelsize=15)
plt.xlim(75, 200)
plt.grid()

#グラフの体裁
#plt.legend(fontsize='10')
plt.savefig('output_resolution/Depth_resolutin.png')
plt.show()