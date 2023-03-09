from cProfile import label

import matplotlib.pyplot as plt
import numpy as np

#誘電率
epsilon1 = 4.0
epsilon0 = 1.0
#光速
c = 299792458 #[m/s]


df = np.arange(1, 200) #MHz

dR_basalt = c/(2*np.sqrt(epsilon1)*df*10**6)
dR_vacuum = c/(2*np.sqrt(epsilon0)*df*10**6)


#描画
plt.figure(figsize=(8, 8))
#plt.plot(df, dR_basalt, label='in basalt')
plt.plot(df, dR_vacuum)

#グラフの体裁
plt.title('Depth Resolution', fontsize=20)
plt.xlabel('$\Delta f$ [MHz]', fontsize=15)
plt.ylabel('$\Delta R$ [m]', fontsize=15)
plt.tick_params(labelsize=15)
plt.ylim(0, 5)
plt.grid()
#plt.legend(fontsize='10')
plt.savefig('fig/Depth_resolutin.png')
plt.show()