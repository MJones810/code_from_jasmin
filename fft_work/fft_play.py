#!/usr/bin/env python2.7
''' playing with how to work out fft '''
import numpy as np
from numpy import fft
import matplotlib.pyplot as plt
from netCDF4 import Dataset
activate_this = '/home/users/mjones07/science/venv/bin/activate_this.py'
execfile(activate_this,dict(__file__=activate_this))
import numexpr as ne

# first try to get a fourier transform of a single lat circle
path = '/group_workspaces/jasmin/hiresgw/mj07/'
date = '19910601'
fileu = path+'xjanpa.pj'+date+'.u.nc'
fu = Dataset(fileu,'r')
u_nc = fu.variables['u']
lat = fu.variables['latitude']
lon = fu.variables['longitude']
z = fu.variables['z_hybrid_height']
filev = path+'xjanpa.pi'+date+'.v.nc'
fv = Dataset(filev,'r')
v_nc = fv.variables['v']
deg2S = 375
deg50N = 600
# trop 0->70, strat, 70->130, meso 130->-1
strat1 = 0  
strat2 = 70

u_slicetemp = u_nc[0,strat1:strat2,deg50N,:]
v_slicetemp = v_nc[0,strat1:strat2,deg50N,:]

u_slice = u_slicetemp[0,:]
v_slice = v_slicetemp[0,:]
for i in xrange(1,strat2-strat1):
    u_slice = 0.5*(u_slicetemp[i,:]+u_slice)
    v_slice = 0.5*(v_slicetemp[i,:]+v_slice)

# just going to use KE = 0.5(u^2+v^2)
KE = ne.evaluate('0.5*(u_slice**2+v_slice**2)')

### FFT ###

n = len(lon[:])
dx = lon[1]-lon[0]
Fk = fft.fft(KE)/n
Fk = fft.fftshift(Fk)
nu = fft.fftfreq(n,dx)
nu = fft.fftshift(nu)
power = np.absolute(Fk)**2

fig = plt.figure()

plt.subplot(4,1,1)
plt.suptitle('%s at %fN from %dm to %dm' % (date,lat[deg50N],z[strat1],z[strat2]))
plt.plot(lon,KE)
plt.title('midnight UTC')
plt.xlabel('Longitude')
plt.ylabel('KE (m$^2$s$^{-2}$)')
plt.xlim(lon[0],lon[-1])
plt.subplot(4,1,2)
plt.loglog(360*nu[len(nu)/2+1:],power[len(nu)/2+1:])
plt.ylabel('Power')
plt.xlabel('wavenumber')
nu3 = (360*nu[len(nu)/2+1:])**-3
nu53 = (360*nu[len(nu)/2+1:])**-(5/3)
plt.loglog(360*nu[len(nu)/2+1:],nu3)
plt.loglog(360*nu[len(nu)/2+1:],nu53)
plt.xlim(360*nu[len(nu)/2+1],360*nu[-1])



# average over a day

u_slicetemp = u_nc[0:24,strat1:strat2,deg50N,:]
v_slicetemp = v_nc[0:24,strat1:strat2,deg50N,:]

u_slice = u_slicetemp[:,0,:]
v_slice = v_slicetemp[:,0,:]
for i in xrange(1,strat2-strat1):
    u_slice = 0.5*(u_slicetemp[:,i,:]+u_slice)
    v_slice = 0.5*(v_slicetemp[:,i,:]+v_slice)

u_mean_slice = u_slice[0]
v_mean_slice = v_slice[0]

for t in xrange(1,24):
    u_mean_slice = 0.5*(u_mean_slice+u_slice[t])
    v_mean_slice = 0.5*(v_mean_slice+v_slice[t])

# just going to use KE = 0.5(u^2+v^2)
KE = ne.evaluate('0.5*(u_mean_slice**2+v_mean_slice**2)')

### FFT ###

n = len(lon[:])
dx = lon[1]-lon[0]
Fk = fft.fft(KE)/n
Fk = fft.fftshift(Fk)
nu = fft.fftfreq(n,dx)
nu = fft.fftshift(nu)
power = np.absolute(Fk)**2



plt.subplot(4,1,3)
plt.plot(lon,KE)
plt.title('day average')
plt.xlabel('Longitude')
plt.ylabel('KE (m$^2$s$^{-2}$)')
plt.xlim(lon[0],lon[-1])
plt.subplot(4,1,4)
plt.loglog(360*nu[len(nu)/2+1:],power[len(nu)/2+1:])
plt.ylabel('Power')
plt.xlabel('wavenumber')
plt.xlim(360*nu[len(nu)/2+1],360*nu[-1])
nu3 = (360*nu[len(nu)/2+1:])**-3
nu53 = (360*nu[len(nu)/2+1:])**-(5/3)
plt.loglog(360*nu[len(nu)/2+1:],nu3)
plt.loglog(360*nu[len(nu)/2+1:],nu53)
plt.show()
