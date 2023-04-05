import matplotlib.pyplot as plt
import numpy as np

#光速
c = 299792458 # [m/s]


f0 = np.arange(1, 300, 0.1) # 中心周波数

def calc_resolution():
    #誘電率
    epsilon1 = 1.0
    epsilon2 = 4.0


    dR1 = c / (2*np.sqrt(epsilon1) * f0 *10**6 * 0.5)
    dR2 = c / (2*np.sqrt(epsilon2) * f0 *10**6 * 0.5)


    #描画
    plt.figure(figsize=(25, 16))
    plt.subplots_adjust(wspace=0.7)
    plt.subplots_adjust(hspace=0.3)

    # ----1枚目----
    plt.subplot(2, 3, 1)
    plt.plot(f0, dR1, label=r'$\varepsilon _r = 1.0$')
    plt.plot(f0, dR2, label=r'$\varepsilon_r = 4.0$')

    plt.title(' (a) Depth Resolution (Overview)', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Depth Resolution [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.yscale('log')
    plt.grid()
    plt.legend(fontsize='20')


    # ----2枚目----
    plt.subplot(2, 3, 4)
    plt.plot(f0, dR1, label=r'$\varepsilon _r = 1.0$')
    plt.plot(f0, dR2, label=r'$\varepsilon_r = 4.0$')

    plt.title('(b) Depth Resolution (Detail of 1-10 MHz)', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Depth Resolution [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.xlim(1, 10)
    plt.grid()
    plt.legend(fontsize='20')


    # ----3枚目----
    plt.subplot(2, 3, 5)
    plt.plot(f0, dR1, label=r'$\varepsilon _r = 1.0$')
    plt.plot(f0, dR2, label=r'$\varepsilon_r = 4.0$')

    plt.title('(c) Depth Resolution (Detail of 10-60 MHz)', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Depth Resolution [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.xlim(10, 60)
    plt.ylim(0, 32)
    plt.grid()
    plt.legend(fontsize='20')


    # ----4枚目----
    plt.subplot(2, 3, 6)
    plt.plot(f0, dR1, label=r'$\varepsilon _r = 1.0$')
    plt.plot(f0, dR2, label=r'$\varepsilon_r = 4.0$')

    plt.title('(d) Depth Resolution (Detail of 60-300 MHz)', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Depth Resolution [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.xlim(50, 300)
    plt.ylim(0, 5.2)
    plt.grid()
    plt.legend(fontsize='20')


    plt.savefig('output_resolution/Depth_resolutin.png')


    plt.show()

#calc_resolution()


def calc_resolution_detectability():
    # 誘電率
    epsilon1 = 1.0

    # 分解能 [m]
    dR1 = c / (2*np.sqrt(epsilon1) * f0 *10**6 * 0.5)

    # 検出可能なチューブの最小高さ
    tube_h = dR1 * 3


    #描画
    plt.figure(figsize=(25, 16))
    plt.subplots_adjust(wspace=0.7)
    plt.subplots_adjust(hspace=0.3)

    # ----1枚目----
    plt.subplot(2, 3, 1)
    plt.plot(f0, tube_h, label=r'$\varepsilon _r = 1.0$')
    #plt.hlines(50, 0, 300, colors='r')

    plt.title(' (a) Overview', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Minimum Detactable Tube Height [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.yscale('log')
    plt.grid()
    #plt.legend(fontsize='20')


    # ----2枚目----
    plt.subplot(2, 3, 4)
    plt.plot(f0, tube_h, label=r'$\varepsilon _r = 1.0$')
    #plt.hlines(50, 0, 300, colors='r')

    plt.title('(b) Detail of 1-10 MHz', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Minimum Detactable Tube Height [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.xlim(1, 10)
    plt.grid()
    #plt.legend(fontsize='20')


    # ----3枚目----
    plt.subplot(2, 3, 5)
    plt.plot(f0, tube_h, label=r'$\varepsilon _r = 1.0$')
    #plt.hlines(50, 0, 300, colors='r')

    plt.title('(c) Detail of 10-60 MHz', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Minimum Detactable Tube Height [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.xlim(10, 60)
    plt.ylim(0, 100)
    plt.grid()
    #plt.legend(fontsize='20')


    # ----4枚目----
    plt.subplot(2, 3, 6)
    plt.plot(f0, tube_h, label=r'$\varepsilon _r = 1.0$')

    plt.title('(d) Detail of 60-300 MHz', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Minimum Detactable Tube Height [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.xlim(60, 300)
    plt.ylim(0, 20)
    plt.grid()
    
    #plt.legend(fontsize='20')


    plt.savefig('output_resolution/resolution_detactability.png')


    plt.show()


calc_resolution_detectability()