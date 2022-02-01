#Script Kelomok 10

import numpy as nps
import scipy
import matplotlib.pyplot as prn
import pykrige.kriging_tools as kt
from pykrige.ok import OrdinaryKriging
 
#Mengimport data
datarover = nps.loadtxt('magnet.txt', skiprows=1)
database = nps.loadtxt('basemagnet.txt', skiprows=1)

#Mencari nilai Tobs rata-rata
t1 = datarover[:,5] 
t2 = datarover[:,6]
t3 = datarover[:,7]

tobs_aver = []
for i in range(len(t1)):
    tobs_aver = (t1+t2+t3)/3
print('tobs_aver = ', tobs_aver)

# Mencari Hbase dengan mengunakan interpolasi
t_rover = datarover[:,4]
t_base = database[:,0]
bacaanbase = database[:,2]
Hbase = []
for i in range(len(t_rover)):
    for j in range(len(t_base)):
        if( t_rover[i] == t_base[j]):
            hbase = bacaanbase[j]
    else:
        s = t_rover[i] - t_base[j]
        t = t_rover[i]- t_base[j-1]
        z = t_base[j] - t_base[j-1]
        hbase = bacaanbase[j] + ((s/t)* z)
    Hbase.append(hbase)

print('Hbase = ', Hbase)

#Mencari nilai koreksi diurnal menggunakan rumus interpolasi
Tvh = []
KoreksiDiurnal = []
for i in range(len(Hbase)):
    Tvh = Hbase[i]-Hbase[0]
    KoreksiDiurnal.append(Tvh)
print('Tvh = ',KoreksiDiurnal)

#Masukkan nilai IGRF
T_IGRF = float(input('Masukkan nilai IGRF = '))

#Mencari nilai Anomali Magnetik
anomali_magnetik = tobs_aver - T_IGRF - KoreksiDiurnal 
print('Anomali_Magnetik =', anomali_magnetik)


koor_x = datarover[:,0]
koor_y = datarover[:,1]

#definisi grid UTM X dan UTM Y, yang ingin di interpolasi
dx, dy = 10, 10
gridx = nps.arange(koor_x.min(), koor_x.max(), dx)
gridy = nps.arange(koor_y.min(), koor_y.max(), dy)

#melakukan interpolasi dengan menggunakan ordinary kriging 
OK = OrdinaryKriging(koor_x, koor_y, anomali_magnetik, variogram_model='linear',verbose=True, enable_plotting=False) #dengan menggunkan metode spherical
z, ss = OK.execute('grid', gridx, gridy)
#print('Nilai Variogram=', z)


#Plotting
prn.contour(z)
prn.imshow(z,cmap='jet', aspect='auto', origin='lower', extent=[koor_x.min(), koor_x.max(), koor_y.min(), koor_y.max()])
prn.title('Peta Anomali Magnetik Kel. 10')
prn.xlabel('UTM X')
prn.ylabel('UTM Y')
prn.colorbar(label='Tobs [mT]')
prn.show()