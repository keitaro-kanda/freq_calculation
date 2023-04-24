import json
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import lineStyles

# 選択するパラメータファイルの指定
params_file = "orbiter"  # orbiter/rover
setting = 'LRS' # LRS/other

# パラメータファイルの読み込み
with open('params/'+params_file + '_params.json') as f:
    params = json.load(f)


# Cese Number
case_num = 1
# 中心周波数
frequency = params['center_freq'+str(case_num)]



# 変数の定義
c = params['speed_of_light'] #真空中の光速[m/s]
pi = np.pi  # 円周率π

epsilon_r = params['epsilon_r']  # 地面の比誘電率
epsilon_0 = params['epsilon_0']  # 真空の誘電率　

loss_tangent = params['loss_tangent']  # losstangent
gain = 10 ** (params['antenna_gain']/10) # アンテナゲイン[dBi]
Pt = params['transmit_power'] # 放射パワー[W]
noise_level = params['noise_level'] # ノイズレベル[W]

width_min = params['width_min'] # チューブ幅の最小値[m]
width_max = params['width_max'] # チューブ幅の最大値[m]
width_step = params['width_step'] # チューブ幅のステップ


roof_min = params['roof_min'] # 深さの最小値[m]
roof_max = params['roof_max'] # 深さの最大値[m]
roof_step = params['roof_step'] # 深さの刻み幅[m]

altitude = params['altitude'] #探査機の高度[m]

# 必要分解能
#dR_need = 3

#　反射係数・透過係数
Gamma_r = (np.sqrt(epsilon_r) - np.sqrt(epsilon_0))**2 / (np.sqrt(epsilon_r) + np.sqrt(epsilon_0))**2
Gamma_t = 1-Gamma_r


#周波数、深さ
width = np.arange(width_min, width_max, width_step)
roof = np.arange(roof_min, roof_max, roof_step)

# ノイズレベルの算出[dB]
noise_dB = 10*np.log10(noise_level / Pt)


# fw_arrayの初期化
fw_array = np.zeros((len(roof), len(width)))


# 受信強度の計算[dB]
def calc_detectability():
    for index_w, w in enumerate(width):
        for index_r, r in enumerate(roof):
            h = w/3
            RCS = w**2
            
            # エコー強度計算
            Pr = 10.0 * np.log10(gain**2 * c**2 / (4.0 * pi)**3 / ((r + h) + altitude)**4 / (frequency*10**6)**2 * RCS) + \
                10.0 * np.log10(Gamma_r * Gamma_t**4) - \
                (0.091 * frequency * np.sqrt(epsilon_r) * loss_tangent) * 2.0 * r
            Pr_detectability = Pr - noise_dB
            
            if setting == 'other':
                freq_width = 0.5 * frequency
            elif setting == 'LRS':
                freq_width = 0.5 * frequency
            dR = c / (2*np.sqrt(epsilon_0) * freq_width * 10**6)
                

            # 検出可能性の判定
            if Pr_detectability > 0 and dR<=h/3:
                fw_array[index_r, index_w] = 1
            else:
                fw_array[index_r, index_w] = -1

    return fw_array

calc_detectability()


# アウトプットを保存するフォルダを作成
if setting == 'other':
    folder_name = "output_detectability/"+str(params_file)+'/'+str(case_num)
elif setting == 'LRS':
    folder_name = "output_detectability/LRS"

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# パラメータの書き出し（txt形式）
with open(folder_name + '/params.txt', mode='w') as f:
    for key, value in params.items():
        f.write(str(key) + ": " + str(value) + "\n")


# プロットの作成
plt.figure(figsize=(12, 10))

plt.imshow(fw_array, origin='lower', cmap='coolwarm', aspect='equal',  vmin=-1, vmax=1)
#plt.colorbar()

# タイトルの設定
if setting == 'other':
    plt.title('Cese'+str(case_num), size=24)
    plt.xticks(np.arange(0, len(width), 2), width[::2])
    plt.yticks(np.arange(0, len(roof), 2), roof[::2])
elif setting == 'LRS':
    plt.title('LRS', size=24)
    plt.xticks(np.arange(1, len(width), 4), width[::4])
    plt.yticks(np.arange(1, len(roof), 5), roof[::5])

plt.xlabel('Tube Width [m]', size=20)  # 横軸のラベルを設定
plt.ylabel('Roof Hight [m]', size=20)  # 縦軸のラベルを設定
plt.tick_params(axis='both', labelsize=15)

plt.minorticks_on()
plt.grid()

# プロットの保存
plt.savefig(folder_name+'/detectabilitymap.png')


#plt.savefig(folder_name + "/power.png")
plt.show()