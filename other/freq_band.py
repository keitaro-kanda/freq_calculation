import numpy as np

#光速
c = 299792458 #[m/s]
#天井
delta_R_roof = 1.0
epsilon_roof = 4
#床
delta_R_floor = 1.0
epsilon_floor = 1

#計算
#天井
delta_f_roof = c/(2*np.sqrt(epsilon_roof)*delta_R_roof)/10**6 #MHz
print('天井',delta_f_roof)
#床
delta_f_floor = c/(2*np.sqrt(epsilon_floor)*delta_R_floor)/10**6 #MHz
print('床',delta_f_floor)