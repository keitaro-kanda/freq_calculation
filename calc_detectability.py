import json
import os

import matplotlib.pyplot as plt
import numpy as np

# 選択するパラメータファイルの指定
params_file = "orbiter"  # LRS/RoPeR/RIMFAX/rover

# パラメータファイルの読み込み
with open('params/'+params_file + '_params.json') as f:
    params = json.load(f)



# 変数の定義
c = params['speed_of_light'] #真空中の光速[m/s]
pi = np.pi  # 円周率π

epsilon_r = params['epsilon_r']  # 地面の比誘電率
epsilon_0 = params['epsilon_0']  # 真空の誘電率　

loss_tangent = params['loss_tangent']  # losstangent
gain = 10 ** (params['antenna_gain']/10) # アンテナゲイン[dBi]
Pt = params['transmit_power'] # 放射パワー[W]
noise_level = params['noise_level'] # ノイズレベル[W]

frequency = params['center_frequency'] # 中心周波数

width_min = params['width_min'] # チューブ幅の最小値[m]
width_max = params['width_max'] # チューブ幅の最大値[m]
width_step = params['width_step'] # チューブ幅のステップ


roof_min = params['roof_min'] # 深さの最小値[m]
roof_max = params['roof_max'] # 深さの最大値[m]
depth_step = params['roof_step'] # 深さの刻み幅[m]

altitude = params['altitude'] #探査機の高度[m]

# 必要分解能
dR_need = 3

#　反射係数・透過係数
Gamma_r = (np.sqrt(epsilon_r) - np.sqrt(epsilon_0))**2 / (np.sqrt(epsilon_r) + np.sqrt(epsilon_0))**2
Gamma_t = 1-Gamma_r


#周波数、深さ
width = np.arange(width_min, width_max, width_step)
depth = np.arange(depth_min, depth_max, depth_step)
height = width/3

# ノイズレベルの算出[dB]
noise_dB = 10*np.log10(noise_level / Pt)


fw_array = np.zeros((len(depth), len(width)))
print(len(depth), len(width))

# 受信強度の計算[dB]
def calc_detectability():
    for index_w, w in enumerate(width):
        for index_d, d in enumerate(depth):
            h = w/3
            RCS = w**2
            
            # エコー強度計算
            Pr = 10.0 * np.log10(gain**2 * c**2 / (4.0 * pi)**3 / (d + altitude)**4 / (f*10**6)**2 * RCS) + \
                10.0 * np.log10(Gamma_r * Gamma_t**4) - \
                (0.091 * f * np.sqrt(epsilon_r) * loss_tangent) * 2.0 * (d - h)
            Pr_detectability = Pr - noise_dB
                
            dR = c / (2*np.sqrt(epsilon_0) * 2 * 10**6)
                

            # 検出可能性の判定
            if d < h:
                fw_array[index_d, index_w] = 0
            elif Pr_detectability > 0 and dR <= h/dR_need:
                fw_array[index_d, index_w] = 1
            else:
                fw_array[index_d, index_w] = -1

    return fw_array

calc_detectability()


# アウトプットを保存するフォルダを作成
folder_name = "output_detectability/LRS_only"


if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# パラメータの書き出し（txt形式）
with open(folder_name + '/params.txt', mode='w') as f:
    for key, value in params.items():
        f.write(str(key) + ": " + str(value) + "\n")


# プロットの作成
plt.figure(figsize=(20, 10))
plt.subplots_adjust(wspace=0.3)
plt.subplots_adjust(hspace=0.3)

plt.plot(width, height, 'k', label='tube height h')
plt.imshow(fw_array, origin='lower', cmap='coolwarm', aspect='equal',  vmin=-1, vmax=1)
#plt.colorbar()

# タイトルの設定
plt.title('Frequency: 4-6 MHz', size=24)
#else:
#    plt.title('Case'+ str(params['case_number']) + ':' \
#        r"$h = $" + str(altitude/1000) +'[km], '+  'Noise Level=' + str(params['noise_level']) + '[W]', size = 24)
plt.xlabel('Tube Width [m]', size=20)  # 横軸のラベルを設定
plt.ylabel('Tube Depth [m]', size=20)  # 縦軸のラベルを設定
plt.xticks(np.arange(len(width)), width)
plt.yticks(np.arange(len(depth)), depth)
#plt.xlim(0, 20)
#plt.ylim(0, 10)
plt.tick_params(axis='both', labelsize=15)
plt.grid()
plt.legend(fontsize=16)


# プロットの保存
#plt.savefig(folder_name + '/detectabilitymap.png')


plt.savefig(folder_name + "/power.png")
plt.show()