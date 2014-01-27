#!/usr/bin/env python2.7
''' Plot results from the monthly mean.
'''

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np

filename = '/group_workspaces/jasmin/hiresgw/mj07/monthly_means/xjanpa.monthlymean.u.nc'

f = Dataset(filename,'r')

time = f.variables['time']
lat = f.variables['latitude']
lon = f.variables['longitude']
z = f.variables['z_hybrid_height']
u = f.variables['u']

#plt.subplot(2,1,1)
plt.contourf(time,lat,u[:,30,:,500].T)
plt.colorbar(orientation='horizontal')
plt.ylabel('Height (km)')
plt.xlabel('Months since start of model')
plt.title('Monthly Mean') 

plt.show()

'''
filename1 = '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj19920201.u.nc'
f1 = Dataset(filename1,'r')

time1 = f1.variables['time']
lat1 = f1.variables['latitude']
lon1 = f1.variables['longitude']
z1 = f1.variables['z_hybrid_height']
u1 = f1.variables['u']

u_1 = u1[::5,:,360,500]
t_1 = time1[::5]

filename2 = '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj19920211.u.nc'
f2 = Dataset(filename2,'r')

time2 = f2.variables['time']
lat2 = f2.variables['latitude']
lon2 = f2.variables['longitude']
z2 = f2.variables['z_hybrid_height']
u2 = f2.variables['u']

u_2 = u2[::5,:,360,500]
t_2 = time2[::5]

filename3 = '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj19920221.u.nc'
f3 = Dataset(filename3,'r')

time3 = f3.variables['time']
lat3 = f3.variables['latitude']
lon3 = f3.variables['longitude']
z3 = f3.variables['z_hybrid_height']
u3 = f3.variables['u']

u_3 = u3[::5,:,360,500]
t_3 = time3[::5]

u_concat = np.concatenate((u_1,u_2,u_3),0)
t_concat = np.concatenate((t_1,t_2,t_3))

plt.subplot(2,1,2)
plt.contourf(t_concat,z2,u_concat.T,20)
plt.colorbar(orientation='horizontal')
plt.ylabel('Height (km)')
plt.xlabel('Hours since start of model')
plt.title('January') 


plt.show()


'''



