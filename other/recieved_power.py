import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize

#地表面パラメータ
epsilon_1 = 5.7
epsilon_0 = 1
losstangent = 0.01
radarcrosssection = 30.0
#レーダーパラメータ
P_t = 800 #[W]
P_min = 1e-12 #[W]
G_t = 1.64
#ノイズレベル
noise = 1e-12 #[W]
#周波数
f1 = 10
f2 = 30
f3 = 50
f4 = 100

#光速
c = 299792458 #[m/s]
#探査深度
R = np.arange(1, 100, 0.1)


#--------

def freq_depth_power(epsilon):
    #反射係数・透過係数
    reflection = (np.sqrt(epsilon) - np.sqrt(epsilon_0))**2 / (np.sqrt(epsilon) + np.sqrt(epsilon_0))**2
    through = 1-reflection
    #meshの作成
    freq = np.arange(1, 201, 0.5)
    depth = np.sort(np.arange(1, 51, 0.5))[::-1]
    f, d = np.meshgrid(freq, depth)
    #減衰率
    attenuation = 10**(-0.091*np.sqrt(epsilon)*losstangent*f*d/5)
    print('反射係数', reflection)
    print('投下係数', through)
    #パワーの計算
    power = P_t*G_t**2*(c/f*10**6)**2/(4*np.pi)**3/d**4 * radarcrosssection * through**4 *reflection * attenuation**(2*d)
    power_dB = 10*np.log10(power/noise)

    #描画
    plt.pcolormesh(f, d, power_dB, cmap='coolwarm', norm=Normalize(vmin=-100, vmax=100))
    #カラーバー
    pp = plt.colorbar(orientation='vertical')
    pp.set_label('Echo Power to Noise Level [dB]', fontsize=15)
    #グラフの体裁
    plt.grid(linestyle='--', color='grey')
    plt.title('Echo from Tube Floor', fontsize=20)
    plt.axis([min(freq), max(freq), max(depth), min(depth)])
    plt.xlabel('Frequency [MHz]', fontsize=15)
    plt.ylabel('Detecsion Depth [m]', fontsize=15)
    plt.savefig('fig/epsilon='+str(epsilon)+'.png')
    plt.show()

freq_depth_power(5.7)

#--------

def power_ratio(epsilon):
    #変数域の定義
    surface_distance = 0.5 #[m]
    floor_depth = np.arange(1, 50, 0.5)
    freq = np.arange(1, 200, 0.5)
    f, d = np.meshgrid(freq, floor_depth)
    #反射係数・透過係数
    reflection = (np.sqrt(epsilon) - np.sqrt(epsilon_0))**2 / (np.sqrt(epsilon) + np.sqrt(epsilon_0))**2
    through = 1-reflection
    #減衰率
    attenuation = 10**(-0.091*np.sqrt(epsilon)*losstangent*f*d/5)

    #地表面エコーの強度
    power_surface = P_t*G_t**2*(c/f*10**6)**2/(4*np.pi)**3/surface_distance**4 * radarcrosssection * reflection

    #地表面と床面のエコー強度比[dB]
    #floor_surface = 10*(4*np.log10(surface_distance*through/d) - 0.091*np.sqrt(epsilon_1)*losstangent*f*2*d/10)
    power_floor = P_t*G_t**2*(c/f*10**6)**2/(4*np.pi)**3/d**4 * radarcrosssection * through**4 *reflection * attenuation**(2*d)
    power_ratio_dB = 10*np.log10(power_floor/power_surface)

    #地表面エコーの強度とノイズレベルの比[dB]
    surface_noise_ratio = 10*np.log10(noise/power_surface) + d*0
    surface_floor_noise = power_ratio_dB - surface_noise_ratio

    #----プロット----
    plt.figure(figsize=(20, 7))
    #----
    plt.subplot(1, 2, 1)
    plt.pcolormesh(f, d, surface_floor_noise, cmap='coolwarm', norm=Normalize(vmin=-100, vmax=100))
    #カラーバー
    pp = plt.colorbar(orientation = 'vertical')
    pp.set_label('Echo Power Ratio [dB]', fontsize=15)
    #グラフの体裁
    plt.title('Floor Echo Power to Noise Level [dB]', fontsize=20)
    plt.grid()
    plt.axis([min(freq), max(freq), max(floor_depth), min(floor_depth)])
    plt.xlabel('Frequency [MHz]', fontsize=15)
    plt.ylabel('Floor Depth [m]', fontsize=15)
    #----
    plt.subplot(1, 2, 2)
    plt.pcolormesh(f, d, power_ratio_dB)
    #カラーバー
    pp = plt.colorbar(orientation = 'vertical')
    pp.set_label('Echo Power Ratio [dB]', fontsize=15)
    #グラフの体裁
    plt.title('Floor Echo Power to Surface Echo Power [dB]', fontsize=20)
    plt.grid()
    plt.axis([min(freq), max(freq), max(floor_depth), min(floor_depth)])
    plt.xlabel('Frequency [MHz]', fontsize=15)
    plt.ylabel('Floor Depth [m]', fontsize=15)
    
    #
    plt.savefig('fig/echo_power_ratio_epsilon='+str(epsilon)+'.png')
    plt.show()

#power_ratio(5.7)

