import matplotlib.pyplot as plt
import numpy as np

# 中心周波数の範囲を設定 [MHz]
fc_range = np.arange(1, 301, 1) 

# 洞窟の高さの範囲を設定 [m]
h_range = np.arange(1, 101, 0.5)  

# 検出可能かどうかの結果を格納する2次元配列を初期化
fh_mesh = np.zeros((len(h_range), len(fc_range)))

# delta_fの定義
#delta_f_range = 0.5 * fc_range

# 誘電率
epsilon_r = 1.0

# 高速 [m/s]
c = 299792458

# 中心周波数と洞窟の高さの組み合わせごとに検出可能かどうかを計算
for i, fc in enumerate(h_range):
    for j, h in enumerate(fc_range):
        delta_f = 0.5 * fc * 10**6
        delta_R = c / (2 * delta_f * np.sqrt(epsilon_r))
        #print(f"fc={fc}, h={h}, delta_R={delta_R}")
        if delta_R <= h / 3:
            fh_mesh[i, j]= 1

#print(fh_mesh)
# プロットを作成
plt.figure(figsize=(20, 15))
plt.subplots_adjust(wspace=0.7)
plt.subplots_adjust(hspace=0.3)

plt.subplot(2, 3, 1)
plt.imshow(fh_mesh, origin='lower', 
           extent=[fc_range[0], fc_range[-1], h_range[0], h_range[-1]], 
           aspect='auto', cmap='coolwarm', vmin=0, vmax=1.0)
#plt.colorbar(label='Detectable')  # カラーバーを追加
plt.xlabel('Center Frequency [MHz]')  # 横軸のラベルを設定
plt.ylabel('Cave Height [m]')  # 縦軸のラベルを設定
plt.title('Detectability of Caves by Ground Penetrating Radar')  # タイトルを設定
plt.grid()

plt.subplot(2, 3, 4)
plt.imshow(fh_mesh[1:100, 1:50], origin='lower', 
           #extent=[fc_range[0], fc_range[-1], h_range[0], h_range[-1]], 
           aspect='auto', cmap='coolwarm', vmin=0, vmax=1.0)
#plt.colorbar(label='Detectable')  # カラーバーを追加
plt.xlabel('Center Frequency [MHz]')  # 横軸のラベルを設定
plt.ylabel('Cave Height [m]')  # 縦軸のラベルを設定
plt.title('Detectability of Caves by Ground Penetrating Radar')  # タイトルを設定
plt.grid()

plt.subplot(2, 3, 5)
plt.imshow(fh_mesh[1:30, 50:150], origin='lower', 
           #extent=[fc_range[0], fc_range[-1], h_range[0], h_range[-1]], 
           aspect='auto', cmap='coolwarm', vmin=0, vmax=1.0)
#plt.colorbar(label='Detectable')  # カラーバーを追加
plt.xlabel('Center Frequency [MHz]')  # 横軸のラベルを設定
plt.ylabel('Cave Height [m]')  # 縦軸のラベルを設定
plt.title('Detectability of Caves by Ground Penetrating Radar')  # タイトルを設定
plt.grid()

plt.subplot(2, 3, 6)
plt.imshow(fh_mesh[1:10, 150:300], origin='lower', 
           #extent=[fc_range[0], fc_range[-1], h_range[0], h_range[-1]], 
           aspect='auto', cmap='coolwarm', vmin=0, vmax=1.0)
#plt.colorbar(label='Detectable')  # カラーバーを追加
plt.xlabel('Center Frequency [MHz]')  # 横軸のラベルを設定
plt.ylabel('Cave Height [m]')  # 縦軸のラベルを設定
plt.title('Detectability of Caves by Ground Penetrating Radar')  # タイトルを設定
plt.show()

