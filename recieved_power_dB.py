from cProfile import label

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize

# 定数の設定
c = 299792458  # 光速（m/s）
pi = np.pi  # π
sigma = 30.0  # レーダー断面積（dB）
epsilon_r = 5.7  # 誘電率
epsilon_0 = 1.0  # 真空雨の誘電率　
loss_tangent = 0.01  # 損失角（tan）
Pt= 800 # 放射パワー（W）

def calc_Pr(gain, noise_level_W):  
    #　反射係数・透過係数
    Gamma_r = (np.sqrt(epsilon_r) - np.sqrt(epsilon_0))**2 / (np.sqrt(epsilon_r) + np.sqrt(epsilon_0))**2
    Gamma_t = 1-Gamma_r
    print('reflect:', Gamma_r)
    print('through:',Gamma_t)

    #周波数、深さ
    freq = np.arange(1, 201, 1.0)
    depth = np.arange(1, 51, 1.0)
    # Rとfのメッシュグリッドを生成
    f_mesh, R_mesh = np.meshgrid(freq, depth)

    # ノイズレベルの設定
    noise_dB = 10*np.log10(noise_level_W / 800)


    # 受信強度の計算[dB]
    Pr = 10.0 * np.log10(gain**2 * c**2 / (4.0 * pi)**3 / R_mesh**4 / (f_mesh*10**6)**2 * sigma) + \
        10.0 * np.log10(Gamma_r * Gamma_t**4) - \
        (0.091 * f_mesh * np.sqrt(epsilon_r) * loss_tangent) * 2.0 * R_mesh
    Pr_detectability = Pr - noise_dB


    # 特定の周波数で固定してdepth対dBのプロットを作る
    def calc_Pr_certain_freq(certain_f):
        Pr_freq = 10.0 * np.log10(gain**2 * c**2 / (4.0 * pi)**3 / depth**4 / (certain_f*10**6)**2 * sigma) + \
        10.0 * np.log10(Gamma_r * Gamma_t**4) - \
        (0.091 * certain_f * np.sqrt(epsilon_r) * loss_tangent) * 2.0 * depth
        Pr_freq_detectability = Pr_freq - noise_dB
        
        return Pr_freq_detectability
    

    Pr_10 = calc_Pr_certain_freq(10.0)
    Pr_25 = calc_Pr_certain_freq(25.0)
    Pr_50 = calc_Pr_certain_freq(50.0)
    Pr_75 = calc_Pr_certain_freq(75.0)


    # カラーマップをプロット
    plt.figure(figsize=(18, 7))


    #　Pr_dBのプロット
    plt.subplot(1, 2, 1)
    plt.pcolormesh(f_mesh, R_mesh, Pr_detectability, cmap='coolwarm', shading='auto', norm=Normalize(vmin=-150, vmax=150))

    plt.title("Recived Power")
    plt.xlabel('Frequency [MHz]')
    plt.ylabel('Depth [m]')
    plt.colorbar(label='Received power [dB]')


    plt.subplot(1, 2, 2)
    plt.plot(depth, Pr_10, label='10 MHz')
    plt.plot(depth, Pr_25, label='25 MHz')
    plt.plot(depth, Pr_50, label='50 MHz')
    plt.plot(depth, Pr_75, label='75 MHz')
    #plt.hlines(noise_dB, min(depth), max(depth), label='noise level')

    plt.title("Received Power at each Frequecy")
    plt.xlabel('Depth [m]')
    plt.ylabel('Received Power [dB]')
    plt.legend()
    plt.grid()

    plt.savefig('fig/gain_'+str(gain)+'_noise_'+str(noise_level_W)+'.png')


    plt.show()


calc_Pr(1.64, 1e-12)