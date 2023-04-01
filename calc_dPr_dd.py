import numpy as np
import matplotlib.pyplot as plt
import sympy


# 微分計算
def bibunn_keisan():
    # dを変数とする関数Prを定義
    d, h, G_t, c, f, Gamma_r, Gamma_t, eps_r, sigma = sympy.symbols('d h G_t c f Gamma_r Gamma_t eps_r sigma')
    Pr = 10 * sympy.log(G_t**2 * c**2 / ((4 * sympy.pi)**3 * (d + h)**4 * f**2) * (3/2*d)**2, 10) \
        + 10 * sympy.log(Gamma_r * Gamma_t**4, 10) \
        - (0.091 * f * sympy.sqrt(eps_r) * sympy.tan(sigma)) * 2 * d

    # Prをdで微分
    dPr = sympy.diff(Pr, d)

    # 微分結果をTeX形式で表示
    print(sympy.latex(dPr))

#bibunn_keisan()

# 微分計算なしパターン

# 横軸の値を生成
d = np.arange(0.1, 100, 0.1)

# fの値をリストに格納
f_list = [5, 25, 50, 75, 100, 150]

# 高度設定
#altitude = 25 # [km]
#h = altitude * 1000 # [m]


plt.figure(figsize=(14, 14))
plt.subplots_adjust(wspace=0.7)
plt.subplots_adjust(hspace=0.3)

    # dPr/ddの式を計算し、グラフをプロット
for i in [1, 2, 3]:
    for f in f_list:
        if i==1:
            altitude=25
        elif i==2:
            altitude=50
        elif i ==3:
            altitude=100
        h = altitude * 1000

        ddPr = 20 * ((-2/(d+h)) + (1/d)) / np.log(10) - f * 3.64e-3
        plt.subplot(3, 1, i)
        plt.plot(d, ddPr, label=f"f={f}")
        
        # dPrが0になるx座標を取得して、グラフ上に表示
        hanbetsu = np.argmin(np.abs(ddPr))
        x_intercept = d[hanbetsu]
        #if  hanbetsu<0.1:
        plt.text(x_intercept, 0, f"{x_intercept:.2f}", ha="center", va="center")

        # グラフのタイトル、ラベル、凡例を設定
        plt.title(r"h="+str(altitude)+"km", size=24)
        plt.xlabel(r"$d$",size=20)
        plt.ylabel(r"$\frac{d P_r}{d d}$", size=20)
        plt.ylim(-0.1, 0.1)
        plt.tick_params(labelsize=20)
        plt.legend(fontsize=16)

        # グリッドを表示
        plt.grid()

# グラフを保存
plt.savefig('output_recieved_power/dPr_dd.png')
# グラフを表示
plt.show()

