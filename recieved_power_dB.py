import json
import os
from ast import Gt

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize

# 選択するパラメータファイルの指定
params_file = "rover"  # LRS/RoPeR/RIMFAX/rover

# パラメータファイルの読み込み
with open('params/'+params_file + '_params.json') as f:
    params = json.load(f)



# 変数の定義
c = params['speed_of_light'] #真空中の光速[m/s]
pi = np.pi  # 円周率π

#sigma = params['radar_cross_section']  # レーダー断面積[m^2]
epsilon_r = params['epsilon_r']  # 地面の比誘電率
epsilon_0 = params['epsilon_0']  # 真空雨の誘電率　
loss_tangent = params['loss_tangent']  # 損失角（tan）

gain = 10 ** (params['antenna_gain']/10) # アンテナゲイン[dBi]
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

    # レーダー断面積を深さに応じて変化させる
    sigma1 = (R_mesh * 3/2) ** 2
    sigma2 = (depth * 3/2) ** 2


    # ノイズレベルの算出[dB]
    noise_dB = 10*np.log10(noise_level / Pt)


    # 受信強度の計算[dB]
    Pr = 10.0 * np.log10(gain**2 * c**2 / (4.0 * pi)**3 / (R_mesh + altitude)**4 / (f_mesh*10**6)**2 * sigma1) + \
        10.0 * np.log10(Gamma_r * Gamma_t**4) - \
        (0.091 * f_mesh * np.sqrt(epsilon_r) * loss_tangent) * 2.0 * R_mesh
    #　ノイズレベルに対する強度に変換
    Pr_detectability = Pr - noise_dB


    # 特定の周波数で固定してdepth対dBのプロットを作る
    def calc_Pr_certain_freq(certain_f):
        Pr_freq = 10.0 * np.log10(gain**2 * c**2 / (4.0 * pi)**3 / (depth + altitude)**4 / (certain_f*10**6)**2 * sigma2) + \
        10.0 * np.log10(Gamma_r * Gamma_t**4) - \
        (0.091 * certain_f * np.sqrt(epsilon_r) * loss_tangent) * 2.0 * depth
        Pr_freq_detectability = Pr_freq - noise_dB
        
        return Pr_freq_detectability
    
    if params_file == 'rover' :
        Pr_1 = calc_Pr_certain_freq(5.0)
        Pr_2 = calc_Pr_certain_freq(25.0)
        Pr_3 = calc_Pr_certain_freq(50.0)
        Pr_4 = calc_Pr_certain_freq(100.0)
        Pr_5 = calc_Pr_certain_freq(200.0)
        Pr_6 = calc_Pr_certain_freq(300.0)
    
    else:
        Pr_1 = calc_Pr_certain_freq(5.0)
        Pr_2 = calc_Pr_certain_freq(25.0)
        Pr_3 = calc_Pr_certain_freq(50.0)
        Pr_4 = calc_Pr_certain_freq(75.0)
        Pr_5 = calc_Pr_certain_freq(200.0)
        Pr_6 = calc_Pr_certain_freq(150.0)



    # アウトプットを保存するフォルダを作成
    if params_file == 'rover':
        folder_name = "output_recieved_power/"+params_file + '/Case' + str(params['case_number'])

    elif params_file == 'LRS':
        folder_name = "output_recieved_power/"+params_file + '/' + str(altitude) + \
        '_noise'+str(noise_dB) + "_h"+str(altitude)

    else:
        folder_name = "output_recieved_power/"+params_file + \
        '_noise'+str(noise_dB) + "_h"+str(altitude)


    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    
    # パラメータ情報を保存
    with open(folder_name + "/params.json", "w") as f:
        json.dump(params, f)


    # パラメータの書き出し（txt形式）
    with open(folder_name + '/params.txt', mode='w') as f:
        for key, value in params.items():
            f.write(str(key) + ": " + str(value) + "\n")
    

    # レーダー断面積のプロット
    plt.figure(figsize=(10, 7))
    plt.plot(depth, sigma2)


    plt.xlabel('Depth [m]', size = 20)
    plt.ylabel('Radar Cross Section [m^2]', size = 20)
    plt.tick_params(axis='both', labelsize=15)
    plt.grid()

    plt.savefig('output_recieved_power/radar_cross_section.png')
    #plt.show()
    


    # カラーマップをプロット
    plt.figure(figsize=(18, 7))


    plt.subplot(1, 2, 1)
    plt.pcolormesh(f_mesh, R_mesh, Pr_detectability, cmap='coolwarm', shading='auto', norm=Normalize(vmin= -50, vmax=50))

    if params_file == 'rover':
        plt.title('Case'+ str(params['case_number']) + ':' \
            r"$P_t = $" + str(Pt) +'[W], '+  r'$G_t =$' + str(params['antenna_gain']) + '[dBi]', size = 24)
    else:
        plt.title(r"$h = $" + str(altitude) +'[km], '+  r'$Noise Level =$' + str(noise_level) + '[W]', size = 24)
    plt.xlabel('Frequency [MHz]', size = 20)
    plt.ylabel('Depth [m]', size = 20)
    cbar = plt.colorbar(label='Received power [dB]')
    cbar.ax.tick_params(labelsize=16)
    plt.tick_params(axis='both', labelsize=15)



    plt.subplot(1, 2, 2)
    plt.plot(depth, Pr_1, label='5 MHz')
    plt.plot(depth, Pr_2, label='25 MHz')
    plt.plot(depth, Pr_3, label='50 MHz')
    plt.plot(depth, Pr_4, label='100 MHz')
    plt.plot(depth, Pr_5, label='200 MHz')
    plt.plot(depth, Pr_6, label='300 MHz')

    plt.title("Received Power at each Frequecy", size = 24)
    plt.xlabel('Depth [m]', size=20)
    plt.ylabel('Received Power [dB]', size=20)
    #plt.yscale('log')
    plt.legend(fontsize = 15)
    plt.grid()
    
    plt.savefig(folder_name + "/detectability_map.png")

    plt.subplots_adjust(wspace=0.2)
    plt.show()

calc_Pr()