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
def calc_dPr_dd(altitude):
    # 横軸の値を生成
    d = np.arange(0.1, 100, 0.1)

    # fの値をリストに格納
    f_list = [5, 25, 50, 75, 100, 150]

    h = altitude * 1000 # 高度



    # dPr/ddの式を計算し、グラフをプロット
    for f in f_list:
        ddPr = 20 * ((-2/(d+h)) + (1/d)) / np.log(10) - f * 3.64e-3
        plt.figure(figsize=(7, 4))
        plt.plot(d, ddPr, label=f"f={f}")
        
        # dPrが0になるx座標を取得して、グラフ上に表示
        x_intercept = d[np.argmin(np.abs(ddPr))]
        plt.text(x_intercept, 0, f"{x_intercept:.2f}", ha="center", va="center")

    # グラフのタイトル、ラベル、凡例を設定
    plt.title(r"h="+str(altitude)+"km")
    plt.xlabel("d")
    plt.ylabel(r"$\frac{d P_r}{d d}$")
    plt.ylim(-1, 1)
    plt.legend()

    # グリッドを表示
    plt.grid()

    # グラフを表示
    plt.show()

calc_dPr_dd(25)
