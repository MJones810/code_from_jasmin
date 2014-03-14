#!/usr/bin/env python2.7
''' meridional mean ffts, mean after fft'''
import numpy as np
from numpy import fft
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import myplot
activate_this = '/home/users/mjones07/science/venv/bin/activate_this.py'
execfile(activate_this,dict(__file__=activate_this))
import numexpr as ne
from multiprocessing import Pool

def splitfft(KE_strat,lon,splitindstep,nsplit):
    ''' Fucntion that calculates ffts then averages.
    '''
    KE = KE_strat[:,nsplit:nsplit+splitindstep,:]

    n = len(lon)
    dx = lon[1]-lon[0]
    
    Fk = fft.fft(KE)/n
    Fk = fft.fftshift(Fk)
    nu = fft.fftfreq(n,dx)
    nu = fft.fftshift(nu)
    power = np.absolute(Fk)**2
    powermean1 = power[0,:,:]
    for i in xrange(1,power.shape[0]):
        powermean1 = 0.5*(powermean1+power[i,:,:])
    powermean2 = powermean1[0,:]
    for i in xrange(1,powermean1.shape[0]):
        powermean2 = 0.5*(powermean2+powermean1[i,:])

    return powermean2
    
    

def instfield(date,subplot,latrange):
    '''!!!!! needs updating to be like other !!!!'''
    path = '/group_workspaces/jasmin/hiresgw/mj07/'
    filenameu = 'xjanpa.pj'+date+'.u.nc'
    filenamev = 'xjanpa.pi'+date+'.v.nc'

    fu = Dataset(path+filenameu,'r')
    u = fu.variables['u']
    fv = Dataset(path+filenamev,'r')
    v = fv.variables['v']
    lat = fu.variables['latitude']
    lon = fu.variables['longitude']
    z = fu.variables['z_hybrid_height']

    #strat
    z1 = 70
    z2 = 130
    #tropics
    lt1 = latrange[0]
    lt2 = latrange[1]

    # take single timestep slice over the tropics in strat NH only
    u_strat_temp = np.append(u[0,z1:z2,lt1:lt2,:],u[0,z1:z2,lt1:lt2,0:1],axis=2)
    v_strat_temp =  v[0,z1:z2,lt1:lt2+1,:]

    ###interpolation
    u_strat = np.zeros((z2-z1,lt2-lt1,1024))
    v_strat = np.zeros((z2-z1,lt2-lt1,1024))
    for i in xrange(1024):
        u_strat[:,:,i] = 0.5*(u_strat_temp[:,:,i]+u_strat_temp[:,:,i+1])
    for i in xrange(lt2-lt1):
        v_strat[:,i,:] = 0.5*(v_strat_temp[:,i,:]+v_strat_temp[:,i,:])
    print 'Interp done'
    ##KE
    KE_strat = ne.evaluate('0.5*(u_strat**2+v_strat**2)')
    processes = 8
    splitind = range(0,lt2-lt1,(lt2-lt1)/processes)
    pool = Pool(processes=processes)
    TASKS = [(KE_strat,lon[:],n) for n in splitind]
    meansection = [pool.apply_async(splitfft, t) for t in TASKS]
    print 'Parallel section done'
    power = meansection[0].get()
    for i in xrange(1,processes):
        power = 0.5*(power+meansection[i].get())
    print 'Mean done'
    n = len(lon[:])
    dx = lon[1]-lon[0]
    nu = fft.fftfreq(n,dx)
    nu = 360*fft.fftshift(nu)

    plt.subplot(subplot[0],subplot[1],subplot[2])
    plt.title('%s from %d to %d deg N' % (date,lat[lt1],lat[lt2-1]))
    plt.loglog(nu[len(nu)/2+1:],power[len(nu)/2+1:])
    plt.xlim(1,1000)
    plt.ylim(10**-8,10**6)
    plt.ylabel('Power')
    scale = 360.
    plt.xlabel('Wavelength (deg)')
    nu3 = (nu[len(nu)/2+1:])**-3
    nu53 = (nu[len(nu)/2+1:])**-(5/3)
    plt.loglog(nu[len(nu)/2+1:-450],0.01*nu3[:-450])
    plt.loglog(nu[len(nu)/2+1:-450],0.01*nu53[:-450])
    plt.xticks([1,2,5,10,20,50,100,300,360/(2*dx)],\
        [scale/1,scale/2,scale/5,scale/10,scale/20,scale/50,scale/100,\
         scale/300,'2dx'])
    
def monthfield(month,subplot,latrange,zrange,labelpad = 0):
    ''' takes only data from first year'''
    
    if month == 'jan': monthval=11
    elif month == 'feb': monthval = 10
    elif month == 'mar': monthval = 0
    elif month == 'apr': monthval = 1
    elif month == 'may': monthval = 2
    elif month == 'jun': monthval = 3
    elif month == 'jul': monthval = 4
    elif month == 'aug': monthval = 5
    elif month == 'sep': monthval = 6
    elif month == 'oct': monthval = 7
    elif month == 'nov': monthval = 8
    elif month == 'dec': monthval = 9
    else: raise ValueError('Month entered wrong!')

    path = '/group_workspaces/jasmin/hiresgw/mj07/monthly_means/'
    filenameu = 'xjanpa.monthlymean.u.nc'
    filenamev = 'xjanpa.monthlymean.v.nc'

    fu = Dataset(path+filenameu,'r')
    u = fu.variables['u']
    fv = Dataset(path+filenamev,'r')
    v = fv.variables['v']
    lat = fu.variables['latitude']
    lon = fu.variables['longitude']
    z = fu.variables['z_hybrid_height']

    # range in height
    if zrange == 'trop':
        z1 = 0
        z2 = 70
    elif zrange == 'strat':
        z1 = 70
        z2 = 130
    elif zrange == 'meso':
        z1 = 130
        z2 = 180
    else: raise ValueError('Height entered wrong!')
    
    # range in lat
    lt1 = latrange[0]
    lt2 = latrange[1]

    # take single timestep slice over the tropics in strat NH only
    u_strat_temp = np.append(u[monthval,z1:z2,lt1:lt2,:],u[monthval,z1:z2,lt1:lt2,0:1],axis=2)
    v_strat_temp =  v[monthval,z1:z2,lt1:lt2+1,:]

    ###interpolation
    u_strat = np.zeros((z2-z1,lt2-lt1,1024))
    v_strat = np.zeros((z2-z1,lt2-lt1,1024))
    for i in xrange(1024):
        u_strat[:,:,i] = 0.5*(u_strat_temp[:,:,i]+u_strat_temp[:,:,i+1])
    for i in xrange(lt2-lt1):
        v_strat[:,i,:] = 0.5*(v_strat_temp[:,i,:]+v_strat_temp[:,i,:])
    print 'Interp done'
    ##KE
    KE_strat = ne.evaluate('0.5*(u_strat**2+v_strat**2)')
    processes = 4
    splitind = range(0,lt2-lt1,(lt2-lt1)/processes)
    pool = Pool(processes=processes)
    TASKS = [(KE_strat,lon[:],(lt2-lt1)/processes,n) for n in splitind]
    meansection = [pool.apply_async(splitfft, t) for t in TASKS]
    print 'Parallel section done'
    power = meansection[0].get()
    for i in xrange(1,processes):
        power = 0.5*(power+meansection[i].get())
    print 'Mean done'
    n = len(lon[:])
    dx = lon[1]-lon[0]
    nu = fft.fftfreq(n,dx)
    nu = 360*fft.fftshift(nu)

    plt.subplot(subplot[0],subplot[1],subplot[2])
    
    ax = plt.loglog(nu[len(nu)/2+1:],power[len(nu)/2+1:])
    plt.title('%s from %d to %d deg N, %s' % (month,lat[lt1],\
                            lat[lt2-1],zrange))
    plt.xlim(1,1000)
    plt.ylim(10**-8,10**6)
    plt.ylabel('Power')
    scale = 360.
    plt.xlabel('Wavenumber',labelpad = labelpad)
    
    nu3 = (nu[len(nu)/2+1:])**-3
    nu53 = (nu[len(nu)/2+1:])**-(5/3)
    plt.loglog(nu[len(nu)/2+1:-450],0.01*nu3[:-450])
    plt.loglog(nu[len(nu)/2+1:-450],0.01*nu53[:-450])
    #plt.xticks([1,2,5,10,20,50,100,300,360/(2*dx)],\
    #    [scale/1,scale/2,scale/5,scale/10,scale/20,scale/50,scale/100,\
    #     scale/300,'2dx'])

fig = plt.figure(frameon=False,figsize=(9,9))
monthfield(month='jan', subplot=[3,1,1], latrange=[384,768], zrange='trop',labelpad=-15)
monthfield(month='jan', subplot=[3,1,2], latrange=[384,768], zrange='strat',labelpad=-15)
monthfield(month='jan', subplot=[3,1,3], latrange=[384,768], zrange='meso',labelpad=-15)
myplot.addInfo(fig,filename='mean_ffts.py')
plt.show()#savefig('meanfft_jul_tropstratmes.pdf')
