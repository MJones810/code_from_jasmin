#!/usr/bin/env python2.7
''' temp wind plots
'''
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import myplot
from multiprocessing import Pool
activate_this = '/home/users/mjones07/science/venv/bin/activate_this.py'
execfile(activate_this,dict(__file__=activate_this))
import numexpr as ne

def timeheight():
    
    vmin = -100
    vmax = 100
    levs = 20
    lat_val = 374

    u_at_2degS = u[:,:,lat_val,:]
    T_at_2degS = T[:,:,lat_val,:]

    print 'assignment done'
    u_zonalmean_at_2degS = u_at_2degS[:,:,0]
    T_zonalmean_at_2degS = T_at_2degS[:,:,0]
    print 'slice done'

    for i in xrange(1,len(u_at_2degS[0,0,:])):
        
        u_zonalmean_at_2degS = (u_zonalmean_at_2degS+u_at_2degS[:,:,i])/2
        T_zonalmean_at_2degS = (T_zonalmean_at_2degS+T_at_2degS[:,:,i])/2

    ax = plt.figure()
    CS = plt.contour(t,z,u_zonalmean_at_2degS.T,levs,colors='k')
    plt.clabel(CS,fontsize=9,inline=True,inline_spacing=5,fmt='%d')
    plt.contourf(t,z,T_zonalmean_at_2degS.T)
    plt.colorbar(orientation='horizontal')
    #plt.contour(t,z,u_zonalmean_at_2degS.T,levels=[0],linewidth=2,colors='k')
    plt.xlabel('Months since start of model')
    plt.ylabel('Hybrid height (m)')
    plt.title('Time series of zonal mean at %d deg N' % lat[lat_val])
    myplot.addInfo(ax)
    plt.show()

filename = '/group_workspaces/jasmin/hiresgw/mj07/monthly_means/xjanpa.monthlymean.u.nc'
f = Dataset(filename,'r')
u = f.variables['u']
lat = f.variables['latitude']
lon = f.variables['longitude']
t = f.variables['time']
z = f.variables['z_hybrid_height']
filenameT = '/group_workspaces/jasmin/hiresgw/mj07/monthly_means/xjanpa.monthlymean.T.nc'
fT = Dataset(filenameT,'r')
T = fT.variables['T']

timeheight()
