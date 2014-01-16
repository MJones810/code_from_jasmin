#!/usr/bin/env python2.7

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

f = Dataset('xjanpa.pj19910301.u.nc','r')
f2 = Dataset('xjanpa.pj19910301.serial.u.nc','r')

u = f.variables['u']
lat = f.variables['latitude']
lon = f.variables['longitude']
height = f.variables['z_hybrid_height']
time = f.variables['time']
u2 = f2.variables['u']
lat2 = f2.variables['latitude']
lon2 = f2.variables['longitude']
height2 = f2.variables['z_hybrid_height']
time2 = f2.variables['time']

h = height[:]
t = time[:]

plt.figure()
plt.subplot(2,1,1)
plt.contourf(lat[:],h,u[0,:,:,708])
plt.colorbar()
plt.subplot(2,1,2)
plt.contourf(lat[:],h,u2[0,:,:,708])
plt.colorbar()
plt.show()

f.close()
f2.close()
