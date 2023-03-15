### 3. Radar sounder design and lava tubes detectability analysis
#### 考慮してるもの
- レゴリスの影響（3.1章）
- レーダー方程式
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
        - $\sigma_f^0(0) =  \frac{C_f \Gamma _{34}}{2} \left( \frac{1}{\mathrm{cos}^4 \theta + C_f \mathrm{sin}^2 \theta} \right)^{3/2} $ 
        ：単位面積あたりの背景散乱断面積？(backscattering cross-section normalized to unit area)
