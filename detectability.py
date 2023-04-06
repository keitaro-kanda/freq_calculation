import json
import os

import matplotlib.pyplot as plt
import numpy as np

# 選択するパラメータファイルの指定
params_file = "LRS"  # LRS/RoPeR/RIMFAX/rover

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
            RCS = (d * 3/2)**2
            Pr = 10.0 * np.log10(gain**2 * c**2 / (4.0 * pi)**3 / (d + altitude)**4 / (f*10**6)**2 * RCS) + \
                10.0 * np.log10(Gamma_r * Gamma_t**4) - \
                (0.091 * f * np.sqrt(epsilon_0) * loss_tangent) * 2.0 * d
            Pr_detectability = Pr - noise_dB
            
            dR = c / (2*np.sqrt(epsilon_r) * f * 0.5 * 10**6)

            if Pr > noise_dB and dR <= d/6:
                fd_array[index_d, index_f] = 1
            
    return fd_array

calc_detectability()



# アウトプットを保存するフォルダを作成
if params_file == 'rover' or 'LRS':
    folder_name = "output_detectability/"+params_file + '/Case' + str(params['case_number'])
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
plt.figure(figsize=(20, 10))
plt.subplots_adjust(wspace=0.3)

plt.subplot(1, 2, 1)
plt.imshow(fd_array, cmap='coolwarm', origin='lower', aspect='auto')
plt.colorbar()

# タイトルの設定
if params_file == 'rover':
    plt.title('Case'+ str(params['case_number']) + ':' \
        r"$P_t = $" + str(Pt) +'[W], '+  r'$G_t =$' + str(params['antenna_gain']) + '[dBi]', size = 24)
else:
    plt.title('Case'+ str(params['case_number']) + ':' \
        r"$h = $" + str(altitude/1000) +'[km], '+  'Noise Level=' + str(params['noise_level']) + '[W]', size = 24)
plt.xlabel('Center Frequency [MHz]', size=20)  # 横軸のラベルを設定
plt.ylabel('Tube Depth [m]', size=20)  # 縦軸のラベルを設定
plt.grid()

x_min = 1
x_max = 20
y_min = 60
y_max = 100

plt.subplot(1, 2, 2)
plt.imshow(fd_array, cmap='coolwarm', origin='lower', aspect='auto')
plt.colorbar()

# タイトルの設定
if params_file == 'rover':
    plt.title('Case'+ str(params['case_number']) + ':' \
        r"$P_t = $" + str(Pt) +'[W], '+  r'$G_t =$' + str(params['antenna_gain']) + '[dBi]', size = 24)
else:
    plt.title('Case'+ str(params['case_number']) +',Detail', size = 24)
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xlabel('Center Frequency [MHz]', size=20)  # 横軸のラベルを設定
plt.ylabel('Tube Depth [m]', size=20)  # 縦軸のラベルを設定
plt.grid()


# プロットの保存
plt.savefig(folder_name + '/detectabilitymap.png')
plt.show()