import matplotlib.pyplot as plt
import numpy as np

#光速
c = 299792458 # [m/s]


f0 = np.arange(1, 2000, 1) # 中心周波数

def calc_resolution():
    #誘電率
    epsilon1 = 1.0
    #epsilon2 = 4.0


    dR1 = c / (2*np.sqrt(epsilon1) * f0 *10**6 * 0.5)
    dR2 = c / (2*np.sqrt(epsilon1) * f0 *10**6 * 0.2)


    #描画
    plt.figure(figsize=(25, 16))
    plt.subplots_adjust(wspace=0.3)
    plt.subplots_adjust(hspace=0.3)

    # ----1枚目----
    plt.subplot(2, 3, 1)
    plt.plot(f0, dR1, label=r'$\Delta f = 0.5 f_c$')
    #plt.plot(f0, dR2, label=r'$\Delta f = 0.2 f_c$')

    plt.title('(a) 1-10 MHz', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Depth Resolution [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.xlim(1, 10)
    plt.grid()
    #plt.legend(fontsize='20')


    # ----2枚目----
    plt.subplot(2, 3, 2)
    plt.plot(f0, dR1, label=r'$\Delta f = 0.5 f_c$')
    #plt.plot(f0, dR2, label=r'$\Delta f = 0.2 f_c$')

    plt.title('(b) 10-50 MHz', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Depth Resolution [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.xlim(10, 50)
    plt.ylim(0, 35)
    plt.grid()
    #plt.legend(fontsize='20')


    # ----3枚目----
    plt.subplot(2, 3, 3)
    plt.plot(f0, dR1, label=r'$\Delta f = 0.5 f_c$')
    #plt.plot(f0, dR2, label=r'$\Delta f = 0.2 f_c$')

    plt.title('(c) 50-500 MHz', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Depth Resolution [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.xlim(50, 500)
    plt.ylim(0, 7.5)
    plt.grid()
    #plt.legend(fontsize='20')


    plt.subplot(2, 3, 4)
    plt.plot(f0, dR1, label=r'$\Delta f = 0.5 f_c$')
    #plt.plot(f0, dR2, label=r'$\Delta f = 0.2 f_c$')

    plt.title('(d) 500-1000 MHz', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Depth Resolution [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.xlim(500, 1000)
    plt.ylim(0, 0.75)
    plt.grid()
    #plt.legend(fontsize='20')


    plt.subplot(2, 3, 5)
    plt.plot(f0, dR1, label=r'$\Delta f = 0.5 f_c$')
    #plt.plot(f0, dR2, label=r'$\Delta f = 0.2 f_c$')

    plt.title('(e) 1000-2000 MHz', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Depth Resolution [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.xlim(1000, 2000)
    plt.ylim(0, 0.35)
    plt.grid()
    #plt.legend(fontsize='20')
    plt.savefig('output_resolution/Depth_resolutin.png')


    plt.show()

calc_resolution()


def calc_resolution_detectability():
    # 誘電率
    epsilon1 = 1.0

    # 分解能 [m]
    dR1 = c / (2*np.sqrt(epsilon1) * f0 *10**6 * 0.5)
    dR2 = c / (2*np.sqrt(epsilon1) * f0 *10**6 * 0.2)


    # 検出可能なチューブの最小高さ
    tube_h1 = dR1 * 3
    tube_h2 = dR2 * 3

    #描画
    plt.figure(figsize=(25, 16))
    plt.subplots_adjust(wspace=0.3)
    plt.subplots_adjust(hspace=0.3)

    # ----1枚目----
    plt.subplot(2, 3, 1)
    plt.plot(f0, dR1, label=r'$\Delta R$')
    plt.plot(f0, tube_h1, label='detectable tube height')
    #plt.plot(f0, tube_h2, label=r'$\Delta f = 0.2 f_c$')
    #plt.hlines(50, 0, 300, colors='r')

    plt.title(' (a) Overview', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Minimum Detactable Tube Height [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.yscale('log')
    plt.grid()
    plt.legend(fontsize='20')


    # ----2枚目----
    plt.subplot(2, 3, 4)
    plt.plot(f0, dR1, label=r'$\Delta R$')
    plt.plot(f0, tube_h1, label='detectable tube height')
    #plt.plot(f0, tube_h2, label=r'$\Delta f = 0.2 f_c$')
    #plt.hlines(50, 0, 300, colors='r')

    plt.title('(b) Detail of 1-10 MHz', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Minimum Detactable Tube Height [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.xlim(1, 10)
    plt.grid()
    plt.legend(fontsize='20')


    # ----3枚目----
    plt.subplot(2, 3, 5)
    plt.plot(f0, dR1, label=r'$\Delta R$')
    plt.plot(f0, tube_h1, label='detectable tube height')
    #plt.plot(f0, tube_h2, label=r'$\Delta f = 0.2 f_c$')
    #plt.hlines(50, 0, 300, colors='r')

    plt.title('(c) Detail of 10-60 MHz', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Minimum Detactable Tube Height [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.xlim(10, 60)
    plt.ylim(0, 100)
    plt.grid()
    plt.legend(fontsize='20')


    # ----4枚目----
    plt.subplot(2, 3, 6)
    plt.plot(f0, dR1, label=r'$\Delta R$')
    plt.plot(f0, tube_h1, label='detectable tube height')
    #plt.plot(f0, tube_h2, label=r'$\Delta f = 0.2 f_c$')

    plt.title('(d) Detail of 60-300 MHz', fontsize=24)
    plt.xlabel('Center Frequency [MHz]', fontsize=20)
    plt.ylabel('Minimum Detactable Tube Height [m]', fontsize=20)
    plt.tick_params(labelsize=20)
    plt.xlim(60, 300)
    plt.ylim(0, 20)
    plt.grid()
    
    plt.legend(fontsize='20')


    plt.savefig('output_resolution/resolution_detactability.png')


    plt.show()


#calc_resolution_detectability()