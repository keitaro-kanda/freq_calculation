import numpy as np
import matplotlib.pyplot as plt

# 横軸の値を生成
d = np.linspace(0.1, 10, 100)

# fの値をリストに格納
f_list = [5, 25, 50, 100, 150]
h = 25e3 # 高度

# dPr/ddの式を計算し、グラフをプロット
for f in f_list:
    ddPr = 20 * ((-2/(d+h)) + (1/d)) / np.log(10) - f * 3.64e-3
    plt.plot(d, ddPr, label=f"f={f}")
    
    # dPrが0になるx座標を取得して、グラフ上に表示
    x_intercept = d[np.argmin(np.abs(ddPr))]
    plt.text(x_intercept, 0, f"{x_intercept:.2f}", ha="center", va="center")

# グラフのタイトル、ラベル、凡例を設定
plt.title(r"$\frac{d P_r}{d d}$")
plt.xlabel("d")
plt.ylabel(r"$\frac{d P_r}{d d}$")
plt.yscale('log')
plt.legend()

# グリッドを表示
plt.grid()

# グラフを表示
plt.show()

