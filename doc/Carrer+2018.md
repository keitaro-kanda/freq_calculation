### 3. Radar sounder design and lava tubes detectability analysis
#### 考慮してるもの
- ##### 3.1.章：レゴリスの影響
- ##### 3.2.章：解像度
- ##### 3.3.章：レーダー方程式
    - エコー強度密度＠アンテナ位置： 
    $S_1 = \frac{P_t G^2 \lambda ^2}{(4 \pi)^3 R_e ^4}$

    - 地中の減衰
    $S_2 = S_1 \times \mathrm{exp} \{-2 \alpha f_0 (\sqrt{\varepsilon _2} h_r +\sqrt{\varepsilon _1} r_t) \}$
        - $\alpha = 2 \pi / c_0 \mathrm{tan} \sigma $

    - 誘電率境界面における透過、反射
    $S_3 = S_2 \times T_{01}^2 \rho_{12} T_{12}^2 T_{23}^2 $
        - $T_{ij} = 1 - \Gamma_{ij} $
        - $\Gamma_{ij} = \left| \frac{1 - \sqrt{\varepsilon _j / \varepsilon _i}}{1 + \sqrt{\varepsilon _j / \varepsilon _i}} \right| ^2 $
        - $\rho = J_0^2 \frac {\Psi ^2}{2}e^{-\Psi ^2}  $ 
        ：Regolith境界：2-way rough surface transmission power loss

    - チューブ床エコー（レーダー断面積を考慮）
    $P_f = S_3 \sigma_f^0(0) A_f  $
        - $A_f = min (w, \sqrt{2 \lambda h}) \times \sqrt{2 \lambda h} $　
        ：チューブ床の有効面積？(equivalent areaof the lava tube fllor) 
            - $h$：25 km ??
            - $w$：250 m〜
            - $\lambda$：30 m (10 MHz) / 5 m (60 MHz) / 3 m (100MHz)
            - $\sqrt{2 \lambda h} =  500 (\lambda = 5 \mathrm{m})$
            - →$A_f = 125000$から$250000$？？？
        - $\sigma_f^0(0) =  \frac{C_f \Gamma _{34}}{2} \left( \frac{1}{\mathrm{cos}^4 \theta + C_f \mathrm{sin}^2 \theta} \right)^{3/2} $ 
        ：単位面積あたりの背景散乱断面積？(backscattering cross-section normalized to unit area)
- ##### 3.4.章：S/N比(SNR)
    - $ SNR = \frac{P_f}{P_n} = P_f / k_b T_e(f_0)B $
        - $k_b$：ボルツマン定数
        - $T_e(f_0)$：frequency dependent galactic noise temperature
        - $B (= 0.5f_0)$：frequency band width
    - Range Compression Gain
        $G_r = B \times T_s$
        - $B = 0.5 f_0$
        - $T_s$：パルス時間幅
    - Azimuth Compression Gain
    $G_{az} = \frac{L_s}{\nu_s PRI} = \frac{\sqrt{2 \lambda h}}{\nu_s}PRF $
        - $PRF = \frac{4 \nu_s}{\lambda}\mathrm{sin}\theta _c $：minimum pulse repitition freqenxy
        - $\nu_s$：軌道上での衛星の速度
        - $\theta_c$：clutter角度
- ##### 3.5.章：Signal/Clutter比(SCR)
    - Clutter Echo Power
    $P_c = \frac{P_t G^2 \lambda ^2 \sigma_s^0 A_c}{(4 \pi)^3 R_c ^4} $
        - $R_c =  h + r_t \sqrt{\varepsilon_1} + h_r \sqrt{\varepsilon_2} + w/3$
        Clutter Slant Range
        - $A_c = \sqrt{2 \lambda h} \frac{c_0}{B \mathrm{sin} \theta _c} $
        Equivalent Clutter Area
        - \theta _c = \mathrm{cos}^{-1}(h/R_c) $
        Clutter Angle
        - $\sigma_s^0$：surface back-scattering coefficient
    - Signal-to-Clutter Ratio (SCR)
    $SCR = \frac{P_f}{P_c} $


#### パラメータの設定
Parameter | Value
--- | ---
Transmission Power | 800 W
Antenna Gain | 1.0 dB
Pulse Repetition Frequency | 500 Hz 
Pulse Width | 100 μsec
Altitude | 25 km 
Carrier Frequency | 10, 50, 100 MHz 
Relative Permitivity | $\varepsilon_1 = 2.7$ <br> $\varepsilon_2 = 4.0$ <br> $\varepsilon_4 = 4.0$
Losstangent | 0.01
Regolith Layer | 8.5 m
Detectability の定義| 1. $SCR>0$ <br> 2. $SNR>10 \mathrm{dB}$ <br> 3.  $h_r$がレンジ解像度の２倍以上 <br> 4. $w$がaong-track解像度以上