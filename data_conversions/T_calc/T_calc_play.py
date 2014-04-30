#!/usr/bin/env python2.7
''' playin trying to get the temp from pot temp and pressure :- SERIAL'''

from netCDF4 import Dataset
import matplotlib.pyplot as plt
from jug import TaskGenerator
import numpy as np
activate_this = '/home/users/mjones07/science/venv/bin/activate_this.py'
execfile(activate_this,dict(__file__=activate_this))
import numexpr as ne
import time as timepack


# lets start by getting a temp profile at a single point 
time_range = 1

# get the data from the files
pt_file = '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pb19910601.theta.nc'
f_pt = Dataset(pt_file,'r')
pt = f_pt.variables['theta']
p_file = '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.ph19910601.p.nc'
f_p = Dataset(p_file,'r')
p = f_p.variables['p']
# get height and time
z = f_p.variables['z_hybrid_height']
time = f_p.variables['time']
time_plot = time[::time_range]
# select a midlat point for the profile ~50N
start2 = timepack.time()
pt_slice = pt[::time_range,:,0:96,0:128]
p_slice = p[::time_range,:,0:96,0:128]
end2 = timepack.time()-start2
print 'time taken for slice %f' % end2
# send off calcs
start1 = timepack.time()
temp = ne.evaluate('pt_slice*(1000/(p_slice/100))**-0.286') # p/100 conv to hPa
end1 = timepack.time()-start1
print 'time taken for (%d,%d,%d,%d) array %f, %d points' % (temp.shape[0],temp.shape[1],temp.shape[2],temp.shape[3],end1,temp.shape[0]*temp.shape[1]*temp.shape[2]*temp.shape[3])
'''
# plot the profiles of each
fig = plt.figure()
plt.contourf(time_plot,z,temp.T,12)
plt.xlabel(str(time.units))
plt.ylabel('%s (%s)' % (p.standard_name,p.units))
plt.colorbar()
plt.show()
'''
