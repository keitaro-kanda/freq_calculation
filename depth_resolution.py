from cProfile import label

import matplotlib.pyplot as plt
import numpy as np

#誘電率
epsilon1 = 4.0
epsilon2 = 5.0
epsilon3 = 6.0

#光速
c = 299792458 #[m/s]


f0 = np.arange(1, 200) # 中心周波数

dR1 = c / (2*np.sqrt(epsilon1) * f0*10**6)
dR2 = c / (2*np.sqrt(epsilon2) * f0*10**6)
dR3 = c / (2*np.sqrt(epsilon3) * f0*10**6)


#描画
plt.figure(figsize=(8, 8))
plt.plot(f0, dR1, label='$\varepsilon_r = 4.0$')
plt.plot(f0, dR2, label='$\varepsilon_r = 5.0$')
plt.plot(f0, dR3, label='$\varepsilon_r = 6.0$')

#グラフの体裁
plt.title('Depth Resolution', fontsize=20)
plt.xlabel('Center Frequency [MHz]', fontsize=15)
plt.ylabel('Depth Resolution [m]', fontsize=15)
plt.tick_params(labelsize=15)
plt.ylim(0, 5)
plt.grid()
plt.legend(fontsize='10')
plt.savefig('output_resolution/Depth_resolutin.png')
plt.show()