#!/usr/bin/env python2.7
''' meridional mean ffts '''
import numpy as np
from numpy import fft
import matplotlib.pyplot as plt
from netCDF4 import Dataset
activate_this = '/home/users/mjones07/science/venv/bin/activate_this.py'
execfile(activate_this,dict(__file__=activate_this))
import numexpr as ne
import myplot

date = '19920411'
path = '/group_workspaces/jasmin/hiresgw/mj07/'
filenameu = 'xjanpa.pj'+date+'.u.nc'

fu = Dataset(path+filenameu,'r')
u = fu.variables['u']
lat = fu.variables['latitude']
lon = fu.variables['longitude']
z = fu.variables['z_hybrid_height']

# take single timestep slice over the tropics in strat NH only
u_strat_trop = u[0,70:130,256:512,:]

u_strat_trop_mean = u_strat_trop[0,:,:]
for i in xrange(u_strat_trop.shape[0]):
    u_strat_trop_mean = (u_strat_trop_mean+u_strat_trop[i,:,:])/2

u_strat_trop_mean_ = u_strat_trop_mean[0,:]
for i in xrange(u_strat_trop_mean.shape[0]):
    u_strat_trop_mean_ = (u_strat_trop_mean_+u_strat_trop_mean[i,:])/2

filenamev = 'xjanpa.pi'+date+'.v.nc'

fv = Dataset(path+filenamev,'r')
v = fv.variables['v']

# take single timestep slice over the tropics in strat
v_strat_trop = v[0,70:130:,256:512,:]

v_strat_trop_mean = v_strat_trop[0,:,:]
for i in xrange(v_strat_trop.shape[0]):
    v_strat_trop_mean = (v_strat_trop_mean+v_strat_trop[i,:,:])/2

v_strat_trop_mean_ = v_strat_trop_mean[0,:]
for i in xrange(v_strat_trop_mean.shape[0]):
    v_strat_trop_mean_ = (v_strat_trop_mean_+v_strat_trop_mean[i,:])/2

## KE
# just going to use KE = 0.5(u^2+v^2)
KE = ne.evaluate('0.5*(u_strat_trop_mean_**2+v_strat_trop_mean_**2)')


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
plt.plot(lon,KE)
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

#### ex trop

u_strat_trop = u[0,70:130,512:640,:]
u_strat_trop1 = u[0,70:130,128:256,:]

u_strat_trop_mean = u_strat_trop[0,:,:]
u_strat_trop_mean1 = u_strat_trop1[0,:,:]
for i in xrange(u_strat_trop.shape[0]):
    u_strat_trop_mean = (u_strat_trop_mean+u_strat_trop[i,:,:])/2
    u_strat_trop_mean1 = (u_strat_trop_mean1+u_strat_trop1[i,:,:])/2

u_strat_trop_mean_2 = u_strat_trop_mean[0,:]
u_strat_trop_mean_1 = u_strat_trop_mean1[0,:]
for i in xrange(u_strat_trop_mean.shape[0]):
    u_strat_trop_mean_2 = (u_strat_trop_mean_2+u_strat_trop_mean[i,:])/2
    u_strat_trop_mean_1 = (u_strat_trop_mean_1+u_strat_trop_mean1[i,:])/2

u_strat_trop_mean_ = 0.5*(u_strat_trop_mean_1+u_strat_trop_mean_2)

filenamev = 'xjanpa.pi'+date+'.v.nc'

fv = Dataset(path+filenamev,'r')
v = fv.variables['v']

# take single timestep slice over the ex-tropics in strat
v_strat_trop = v[0,70:130,512:640,:]
v_strat_trop1 = v[0,70:130,128:256,:]

v_strat_trop_mean = v_strat_trop[0,:,:]
v_strat_trop_mean1 = v_strat_trop1[0,:,:]
for i in xrange(v_strat_trop.shape[0]):
    v_strat_trop_mean = (v_strat_trop_mean+v_strat_trop[i,:,:])/2
    v_strat_trop_mean1 = (v_strat_trop_mean1+v_strat_trop1[i,:,:])/2

v_strat_trop_mean_2 = v_strat_trop_mean[0,:]
v_strat_trop_mean_1 = v_strat_trop_mean1[0,:]
for i in xrange(v_strat_trop_mean.shape[0]):
    v_strat_trop_mean_2= (v_strat_trop_mean_2+v_strat_trop_mean[i,:])/2
    v_strat_trop_mean_1 = (v_strat_trop_mean_1+v_strat_trop_mean1[i,:])/2

v_strat_trop_mean_ = 0.5*(v_strat_trop_mean_1+v_strat_trop_mean_2)

## KE
# just going to use KE = 0.5(u^2+v^2)
KE = ne.evaluate('0.5*(u_strat_trop_mean_**2+v_strat_trop_mean_**2)')


### FFT ###

n = len(lon[:])
dx = lon[1]-lon[0]
Fk = fft.fft(KE)/n
Fk = fft.fftshift(Fk)
nu = fft.fftfreq(n,dx)
nu = fft.fftshift(nu)
power = np.absolute(Fk)**2

plt.subplot(4,1,1)
plt.plot(lon,KE,'r')
plt.title('%s average over the stratosphere: tropics blue, extratropics red' % (date))
plt.subplot(4,1,2)
plt.loglog(360*nu[len(nu)/2+1:],power[len(nu)/2+1:],'r')

#### other month ########
date = '19911011'
path = '/group_workspaces/jasmin/hiresgw/mj07/'
filenameu = 'xjanpa.pj'+date+'.u.nc'

fu = Dataset(path+filenameu,'r')
u = fu.variables['u']
lat = fu.variables['latitude']
lon = fu.variables['longitude']
z = fu.variables['z_hybrid_height']

# take single timestep slice over the tropics in strat NH only
u_strat_trop = u[0,70:130,256:512,:]

u_strat_trop_mean = u_strat_trop[0,:,:]
for i in xrange(u_strat_trop.shape[0]):
    u_strat_trop_mean = (u_strat_trop_mean+u_strat_trop[i,:,:])/2

u_strat_trop_mean_ = u_strat_trop_mean[0,:]
for i in xrange(u_strat_trop_mean.shape[0]):
    u_strat_trop_mean_ = (u_strat_trop_mean_+u_strat_trop_mean[i,:])/2

filenamev = 'xjanpa.pi'+date+'.v.nc'

fv = Dataset(path+filenamev,'r')
v = fv.variables['v']

# take single timestep slice over the tropics in strat
v_strat_trop = v[0,70:130:,256:512,:]

v_strat_trop_mean = v_strat_trop[0,:,:]
for i in xrange(v_strat_trop.shape[0]):
    v_strat_trop_mean = (v_strat_trop_mean+v_strat_trop[i,:,:])/2

v_strat_trop_mean_ = v_strat_trop_mean[0,:]
for i in xrange(v_strat_trop_mean.shape[0]):
    v_strat_trop_mean_ = (v_strat_trop_mean_+v_strat_trop_mean[i,:])/2

## KE
# just going to use KE = 0.5(u^2+v^2)
KE = ne.evaluate('0.5*(u_strat_trop_mean_**2+v_strat_trop_mean_**2)')


### FFT ###

n = len(lon[:])
dx = lon[1]-lon[0]
Fk = fft.fft(KE)/n
Fk = fft.fftshift(Fk)
nu = fft.fftfreq(n,dx)
nu = fft.fftshift(nu)
power = np.absolute(Fk)**2


plt.subplot(4,1,3)
plt.title('%s average over the stratosphere: tropics blue, extratropics red' % (date))
plt.plot(lon,KE)
plt.xlabel('Longitude')
plt.ylabel('KE (m$^2$s$^{-2}$)')
plt.xlim(lon[0],lon[-1])
plt.subplot(4,1,4)
plt.loglog(360*nu[len(nu)/2+1:],power[len(nu)/2+1:])
plt.ylabel('Power')
plt.xlabel('wavenumber')
nu3 = (360*nu[len(nu)/2+1:])**-3
nu53 = (360*nu[len(nu)/2+1:])**-(5/3)
plt.loglog(360*nu[len(nu)/2+1:],nu3)
plt.loglog(360*nu[len(nu)/2+1:],nu53)
plt.xlim(360*nu[len(nu)/2+1],360*nu[-1])

#### ex trop

u_strat_trop = u[0,70:130,512:640,:]
u_strat_trop1 = u[0,70:130,128:256,:]

u_strat_trop_mean = u_strat_trop[0,:,:]
u_strat_trop_mean1 = u_strat_trop1[0,:,:]
for i in xrange(u_strat_trop.shape[0]):
    u_strat_trop_mean = (u_strat_trop_mean+u_strat_trop[i,:,:])/2
    u_strat_trop_mean1 = (u_strat_trop_mean1+u_strat_trop1[i,:,:])/2

u_strat_trop_mean_2 = u_strat_trop_mean[0,:]
u_strat_trop_mean_1 = u_strat_trop_mean1[0,:]
for i in xrange(u_strat_trop_mean.shape[0]):
    u_strat_trop_mean_2 = (u_strat_trop_mean_2+u_strat_trop_mean[i,:])/2
    u_strat_trop_mean_1 = (u_strat_trop_mean_1+u_strat_trop_mean1[i,:])/2

u_strat_trop_mean_ = 0.5*(u_strat_trop_mean_1+u_strat_trop_mean_2)

filenamev = 'xjanpa.pi'+date+'.v.nc'

fv = Dataset(path+filenamev,'r')
v = fv.variables['v']

# take single timestep slice over the ex-tropics in strat
v_strat_trop = v[0,70:130,512:640,:]
v_strat_trop1 = v[0,70:130,128:256,:]

v_strat_trop_mean = v_strat_trop[0,:,:]
v_strat_trop_mean1 = v_strat_trop1[0,:,:]
for i in xrange(v_strat_trop.shape[0]):
    v_strat_trop_mean = (v_strat_trop_mean+v_strat_trop[i,:,:])/2
    v_strat_trop_mean1 = (v_strat_trop_mean1+v_strat_trop1[i,:,:])/2

v_strat_trop_mean_2 = v_strat_trop_mean[0,:]
v_strat_trop_mean_1 = v_strat_trop_mean1[0,:]
for i in xrange(v_strat_trop_mean.shape[0]):
    v_strat_trop_mean_2= (v_strat_trop_mean_2+v_strat_trop_mean[i,:])/2
    v_strat_trop_mean_1 = (v_strat_trop_mean_1+v_strat_trop_mean1[i,:])/2

v_strat_trop_mean_ = 0.5*(v_strat_trop_mean_1+v_strat_trop_mean_2)

## KE
# just going to use KE = 0.5(u^2+v^2)
KE = ne.evaluate('0.5*(u_strat_trop_mean_**2+v_strat_trop_mean_**2)')


### FFT ###

n = len(lon[:])
dx = lon[1]-lon[0]
Fk = fft.fft(KE)/n
Fk = fft.fftshift(Fk)
nu = fft.fftfreq(n,dx)
nu = fft.fftshift(nu)
power = np.absolute(Fk)**2

plt.subplot(4,1,3)
plt.plot(lon,KE,'r')
plt.subplot(4,1,4)
plt.loglog(360*nu[len(nu)/2+1:],power[len(nu)/2+1:],'r')



myplot.addInfo(fig)
plt.show()
