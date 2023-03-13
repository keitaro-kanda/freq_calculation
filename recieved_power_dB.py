import json
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize



# 選択するパラメータファイルの指定
params_file = "RoPeR"  # または "RoPeR_params.json"

# パラメータファイルの読み込み
with open(params_file + '_params.json') as f:
    params = json.load(f)



# 変数の定義
c = params['speed_of_light'] #真空中の光速[m/s]
pi = np.pi  # 円周率π

sigma = params['radar_cross_section']  # レーダー断面積[m^2]
epsilon_r = params['epsilon_r']  # 地面の比誘電率
epsilon_0 = params['epsilon_0']  # 真空雨の誘電率　
loss_tangent = params['loss_tangent']  # 損失角（tan）

gain = params['antenna_gain']
Pt = params['transmit_power'] # 放射パワー[W]
noise_level = params['noise_level'] # ノイズレベル[W]

freq_min = params['min_frequency'] # 周波数の最小値[MHz]
freq_max = params['max_frequency'] # 周波数の最大値[MHz]
freq_step = params['frequency_step'] # 周波数の刻み幅[MHz]

depth_min = params['min_depth'] # 深さの最小値[m]
depth_max = params['max_depth'] # 深さの最大値[m]
depth_step = params['depth_step'] # 深さの刻み幅[m]

altitude = params['altitude'] #探査機の高度[m]



# 受信パワーの計算
def calc_Pr():  
    #　反射係数・透過係数
    Gamma_r = (np.sqrt(epsilon_r) - np.sqrt(epsilon_0))**2 / (np.sqrt(epsilon_r) + np.sqrt(epsilon_0))**2
    Gamma_t = 1-Gamma_r
    print('reflect:', Gamma_r)
    print('through:',Gamma_t)


    #周波数、深さ
    freq = np.arange(freq_min, freq_max, freq_step)
    depth = np.arange(depth_min, depth_max, depth_step)
    # Rとfのメッシュグリッドを生成
    f_mesh, R_mesh = np.meshgrid(freq, depth)


    # ノイズレベルの算出[dB]
    noise_dB = 10*np.log10(noise_level / Pt)


    # 受信強度の計算[dB]
    Pr = 10.0 * np.log10(gain**2 * c**2 / (4.0 * pi)**3 / (R_mesh + altitude)**4 / (f_mesh*10**6)**2 * sigma) + \
        10.0 * np.log10(Gamma_r * Gamma_t**4) - \
        (0.091 * f_mesh * np.sqrt(epsilon_r) * loss_tangent) * 2.0 * R_mesh
    #　ノイズレベルに対する強度に変換
    Pr_detectability = Pr - noise_dB


    # 特定の周波数で固定してdepth対dBのプロットを作る
    def calc_Pr_certain_freq(certain_f):
        Pr_freq = 10.0 * np.log10(gain**2 * c**2 / (4.0 * pi)**3 / (depth + altitude)**4 / (certain_f*10**6)**2 * sigma) + \
        10.0 * np.log10(Gamma_r * Gamma_t**4) - \
        (0.091 * certain_f * np.sqrt(epsilon_r) * loss_tangent) * 2.0 * depth
        Pr_freq_detectability = Pr_freq - noise_dB
        
        return Pr_freq_detectability
    

    Pr_15 = calc_Pr_certain_freq(15.0)
    Pr_25 = calc_Pr_certain_freq(25.0)
    Pr_50 = calc_Pr_certain_freq(50.0)
    Pr_75 = calc_Pr_certain_freq(75.0)
    Pr_95 = calc_Pr_certain_freq(95.0)
    Pr_150 = calc_Pr_certain_freq(150.0)



    # アウトプットを保存するフォルダを作成
    folder_name = "output_recieved_power/"+params_file+"/gain"+str(gain)+"_altitude"+str(altitude)+'transmssion'+str(Pt)+'noise'+str(noise_dB)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    
    # パラメータ情報を保存
    with open(folder_name + "/params.json", "w") as f:
        json.dump(params, f)

    
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
    plt.plot(depth, Pr_15, label='15 MHz')
    plt.plot(depth, Pr_25, label='25 MHz')
    plt.plot(depth, Pr_50, label='50 MHz')
    plt.plot(depth, Pr_75, label='75 MHz')
    plt.plot(depth, Pr_95, label='95 MHz')
    plt.plot(depth, Pr_150, label='150 MHz')
    #plt.hlines(noise_dB, min(depth), max(depth), label='noise level')

    plt.title("Received Power at each Frequecy")
    plt.xlabel('Depth [m]')
    plt.ylabel('Received Power [dB]')
    plt.legend()
    plt.grid()
    
    plt.savefig(folder_name + "/detectability_map.png")

    plt.show()


calc_Pr()