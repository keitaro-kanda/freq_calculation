import json
import os

import matplotlib.pyplot as plt
import numpy as np

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
epsilon_0 = params['epsilon_0']  # 真空の誘電率　
loss_tangent = params['loss_tangent']  # 損失角（tan）
#width = params['tube_width'] # チューブ幅
width_array = [3, 10, 15, 30, 50, 60]
for w in width_array:
    width = w
    RCS = width**2 # レーダー断面積

    gain = 10 ** (params['antenna_gain']/10) # アンテナゲイン[dBi]
    Pt = params['transmit_power'] # 放射パワー[W]
    noise_level = params['noise_level'] # ノイズレベル[W]

    freq_min = params['min_frequency'] # 周波数の最小値[MHz]
    freq_max = params['max_frequency'] # 周波数の最大値[MHz]
    freq_step = params['frequency_step'] # 周波数の刻み幅[MHz]

    h = width / 3 # チューブの高さ [m]
    depth_min = params['min_depth'] # 深さの最小値[m]
    depth_max = params['max_depth'] # 深さの最大値[m]
    depth_step = params['depth_step'] # 深さの刻み幅[m]

    altitude = params['altitude'] #探査機の高度[m]

    # 必要分解能
    dR_need = 2

    #　反射係数・透過係数
    Gamma_r = (np.sqrt(epsilon_r) - np.sqrt(epsilon_0))**2 / (np.sqrt(epsilon_r) + np.sqrt(epsilon_0))**2
    Gamma_t = 1-Gamma_r


    #周波数、深さ
    freq = np.arange(freq_min, freq_max, freq_step)
    depth = np.arange(depth_min, depth_max, depth_step)
    # Rとfのメッシュグリッドを生成
    f_mesh, d_mesh = np.meshgrid(freq, depth)

    # ノイズレベルの算出[dB]
    noise_dB = 10*np.log10(noise_level / Pt)


    fd_array = np.zeros((len(depth), len(freq)))

    # 受信強度の計算[dB]
    def calc_detectability():
        for index_f, f in enumerate(freq):
            for index_d, d in enumerate(depth):
                # エコー強度計算
                #RCS = (d * 3/2)**2
                Pr = 10.0 * np.log10(gain**2 * c**2 / (4.0 * pi)**3 / (d + altitude)**4 / (f*10**6)**2 * RCS) + \
                    10.0 * np.log10(Gamma_r * Gamma_t**4) - \
                    (0.091 * f * np.sqrt(epsilon_r) * loss_tangent) * 2.0 * (d - h)
                Pr_detectability = Pr - noise_dB
                
                # 分解能計算
                if params_file == "rover":
                    dR = c / (2*np.sqrt(epsilon_0) * f * 0.5 * 10**6)
                elif params_file == 'LRS':
                    dR = c / (2*np.sqrt(epsilon_0) * f * 0.2 * 10**6)
                else:
                    dR = c / (2*np.sqrt(epsilon_0) * f * 0.5 * 10**6)
                

                # 検出可能性の判定
                if d < h+1:
                    fd_array[index_d, index_f] = 0
                elif Pr_detectability > 0 and dR <= h/dR_need:
                    fd_array[index_d, index_f] = 1
                else:
                    fd_array[index_d, index_f] = -1
                
        return fd_array

    calc_detectability()



    # アウトプットを保存するフォルダを作成
    if params_file == 'rover' or 'LRS':
        folder_name = "output_detectability/"+params_file + '_dRneed'+str(dR_need) + '/RCS' + str(RCS)
    else:
        folder_name = "output_detectability/"+params_file + \
        '_noise'+str(noise_dB) + "_h"+str(altitude)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # パラメータの書き出し（txt形式）
    with open(folder_name + '/params.txt', mode='w') as f:
        for key, value in params.items():
            f.write(str(key) + ": " + str(value) + "\n")


    # プロットの作成
    plt.figure(figsize=(20, 20))
    plt.subplots_adjust(wspace=0.3)
    plt.subplots_adjust(hspace=0.3)

    plt.subplot(2, 2, 1)
    plt.imshow(fd_array, origin='lower', cmap='coolwarm', aspect='auto',  vmin=-1, vmax=1)
    #plt.colorbar()

    # タイトルの設定
    #if params_file == 'rover':
    plt.title('(a) RCS='+str(RCS)+':Overview', size=24)
    #else:
    #    plt.title('Case'+ str(params['case_number']) + ':' \
    #        r"$h = $" + str(altitude/1000) +'[km], '+  'Noise Level=' + str(params['noise_level']) + '[W]', size = 24)
    plt.xlabel('Center Frequency [MHz]', size=20)  # 横軸のラベルを設定
    plt.ylabel('Tube Depth [m]', size=20)  # 縦軸のラベルを設定
    plt.tick_params(axis='both', labelsize=15)
    plt.grid()


    x_list = np.linspace(freq_min, freq_max, 4)

    #====2枚目====
    plt.subplot(2, 2, 2)
    plt.imshow(fd_array, cmap='coolwarm', origin='lower', aspect='auto', vmin=-1, vmax=1)

    # タイトルの設定
    plt.title('(b) Detail:' + str(x_list[0]) + '-' + str(x_list[1]-1) + 'MHz', size = 24)
    plt.xlim(x_list[0]-1, x_list[1]-1)
    #plt.ylim(y_list[0], y_list[1])
    plt.xlabel('Center Frequency [MHz]', size=20)  # 横軸のラベルを設定
    plt.ylabel('Tube Depth [m]', size=20)  # 縦軸のラベルを設定
    plt.tick_params(axis='both', labelsize=15)
    plt.grid()


    #====3枚目====
    plt.subplot(2, 2, 3)
    plt.imshow(fd_array, cmap='coolwarm', origin='lower', aspect='auto', vmin=-1, vmax=1)

    # タイトルの設定
    plt.title('(c) Detail:' + str(x_list[1]) + '-' + str(x_list[2]-1) + 'MHz', size = 24)
    plt.xlim(x_list[1]-1, x_list[2]-1)
    #plt.ylim(y_list[0], y_list[1])
    plt.xlabel('Center Frequency [MHz]', size=20)  # 横軸のラベルを設定
    plt.ylabel('Tube Depth [m]', size=20)  # 縦軸のラベルを設定
    plt.tick_params(axis='both', labelsize=15)
    plt.grid()


    #====4枚目====
    plt.subplot(2, 2, 4)
    plt.imshow(fd_array, cmap='coolwarm', origin='lower', aspect='auto', vmin=-1, vmax=1)

    # タイトルの設定
    plt.title('(d) Detail:' + str(x_list[2]) + '-' + str(x_list[3]-1) + 'MHz', size = 24)
    plt.xlim(x_list[2]-1, x_list[3]-1)
    #plt.ylim(y_list[0], y_list[1])
    plt.xlabel('Center Frequency [MHz]', size=20)  # 横軸のラベルを設定
    plt.ylabel('Tube Depth [m]', size=20)  # 縦軸のラベルを設定
    plt.tick_params(axis='both', labelsize=15)
    plt.grid()

    # プロットの保存
    #plt.savefig(folder_name + '/detectabilitymap.png')

    if params_file == 'rover':
            plt.savefig(folder_name + "/detectablity_rover_" + str(RCS) + ".png")

    elif params_file == 'LRS':
        plt.savefig(folder_name + "/power_orbiter_" + str(RCS) + ".png")
        
    else:
        plt.savefig(folder_name + "/power.png")
    plt.show()