#!/usr/bin/env python2.7
''' comparing ffts from xjanp N512L180 and xjleh, xjlef N216L180
    
    Very similar to mean_ffts.py initially, may stay very similar.
    '''

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
from matplotlib.colors import LogNorm

def splitfft(KE_strat,lon,splitindstep,nsplit):
    ''' Fucntion that calculates ffts then averages.
    '''
    KE = KE_strat[:,nsplit:nsplit+splitindstep,:]

    n = len(lon)
    dx = lon[1]-lon[0]
    
    Fk = fft.fft(KE)/n
    Fk = fft.fftshift(Fk,axes=2)
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

def splitfft2dheight(KE_strat,lon,splitindstep,nsplit):
    ''' Fucntion that calculates ffts then averages.
    '''
    KE = KE_strat[:,nsplit:nsplit+splitindstep,:]

    n = len(lon)
    dx = lon[1]-lon[0]
    
    Fk = fft.fft(KE)/n
    Fk = fft.fftshift(Fk,axes=2)
    nu = fft.fftfreq(n,dx)
    nu = fft.fftshift(nu)
    power = np.absolute(Fk)**2
    powermean = power[:,0,:]
    for i in xrange(1,power.shape[1]):
        powermean = 0.5*(powermean+power[:,i,:])

    return powermean
    
def instfield(model,month,subplot,latrange,zrange,labelpad = 0,processes = 4):
    '''  NOT FINISHED!! / abandoned

takes last 10 days from the month in 1992

        No interpolation!
        '''
    raise ValueError('function does not work!')
    if model == 'xjanp':
        lonindmax = 1024
        if month == 'jan': monthval='19920121'
        elif month == 'feb': monthval = '19920221'
        elif month == 'mar': monthval = '19920321'
        elif month == 'apr': monthval = '19920421'
        elif month == 'may': monthval = '19920521'
        elif month == 'jun': monthval = '19920621'
        elif month == 'jul': monthval = '19920721'
        elif month == 'aug': monthval = '19920821'
        elif month == 'sep': monthval = '19920921'
        elif month == 'oct': monthval = '19921021'
        elif month == 'nov': monthval = '19921121'
        elif month == 'dec': monthval = '19921221'
        else: raise ValueError('Month entered wrong!')
    elif model == 'xjlef' or model == 'xjleh': 
        lonindmax = 432
        if month == 'sep': monthval='19810921'
        else: raise ValueError('only september in xjlef')
    else: raise ValueError('xjanp, xjleh or xjlef only')

    path = '/group_workspaces/jasmin/hiresgw/mj07/monthly_means/'
    filenameu = model+'a.'+month+'.u.nc'
    filenamev = model+'a.'+month+'.v.nc'

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
    elif zrange == 'all':
        z1 = 0
        z2 = 180
    else: raise ValueError('Height entered wrong!')
    
    # range in lat
    lt1 = latrange[0]
    lt2 = latrange[1]

def monthfield(model,month,subplot,latrange,zrange,labelpad = 0,processes = 4):
    ''' takes only data from first year'''
     
    if model == 'xjanp':
        lonindmax = 1024
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
    elif model == 'xjlef' or model == 'xjleh': 
        lonindmax = 432
        if month == 'sep': monthval=0
        else: raise ValueError('only september in xjlef')
    else: raise ValueError('xjanp, xjleh or xjlef only')

    path = '/group_workspaces/jasmin/hiresgw/mj07/monthly_means/'
    filenameu = model+'a.monthlymean.u.nc'
    filenamev = model+'a.monthlymean.v.nc'

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
    elif zrange == 'all':
        z1 = 0
        z2 = 180
    else: raise ValueError('Height entered wrong!')
    
    # range in lat
    lt1 = latrange[0]
    lt2 = latrange[1]

    # take single timestep slice over the tropics in strat NH only
    u_strat_temp = np.append(u[monthval,z1:z2,lt1:lt2,:],u[monthval,z1:z2,lt1:lt2,0:1],axis=2)
    v_strat_temp =  v[monthval,z1:z2,lt1:lt2+1,:]

    ###interpolation
    u_strat = np.zeros((z2-z1,lt2-lt1,lonindmax))
    v_strat = np.zeros((z2-z1,lt2-lt1,lonindmax))
    for i in xrange(lonindmax):
        u_strat[:,:,i] = 0.5*(u_strat_temp[:,:,i]+u_strat_temp[:,:,i+1])
    for i in xrange(lt2-lt1):
        v_strat[:,i,:] = 0.5*(v_strat_temp[:,i,:]+v_strat_temp[:,i,:])
    print 'Interp done'
    ##KE
    KE_strat = ne.evaluate('0.5*(u_strat**2+v_strat**2)')
    
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
    
    ax = plt.loglog(nu[len(nu)/2+1:],power[len(nu)/2+1:],label=model)
    plt.title('%s from %d to %d deg N, %s' % (month,lat[lt1],\
                            lat[lt2-1],zrange))
    plt.xlim(1,1000)
    plt.ylim(10**-8,10**6)
    plt.ylabel('Power')
    scale = 360.
    plt.xlabel('Wavelength (deg)',labelpad = labelpad)
    
    nu3 = (nu[len(nu)/2+1:])**-3
    nu53 = (nu[len(nu)/2+1:])**-(5/3)
    plt.loglog(100*nu[len(nu)/2+1:-len(nu)/3],10**6*nu3[:-len(nu)/3],'k')
    plt.loglog(100*nu[len(nu)/2+1:-len(nu)/3],10**6*nu53[:-len(nu)/3],'k')
    plt.xticks([1,2,5,10,20,50,100,300,360/(2*dx)],\
        [scale/1,scale/2,scale/5,scale/10,scale/20,scale/50,scale/100,\
         scale/300,'2dx'])

def contourpower(model,month,subplot,latrange,zrange,labelpad = 0,processes = 4):
    ''' Draws a contour of the power for wavenumber vs height
    
        takes only data from first year
    '''
    
    if model == 'xjanp':
        lonindmax = 1024
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
    elif model == 'xjlef': 
        lonindmax = 432
        if month == 'sep': monthval=0
        else: raise ValueError('only september in xjlef')
    else: raise ValueError('xjanp or xjlef only')

    path = '/group_workspaces/jasmin/hiresgw/mj07/monthly_means/'
    filenameu = model+'a.monthlymean.u.nc'
    filenamev = model+'a.monthlymean.v.nc'

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
    elif zrange == 'all':
        z1 = 0
        z2 = 180
    else: raise ValueError('Height entered wrong!')
    
    # range in lat
    lt1 = latrange[0]
    lt2 = latrange[1]

    # take single timestep slice over the tropics in strat NH only
    u_strat_temp = np.append(u[monthval,z1:z2,lt1:lt2,:],u[monthval,z1:z2,lt1:lt2,0:1],axis=2)
    v_strat_temp =  v[monthval,z1:z2,lt1:lt2+1,:]

    ###interpolation
    u_strat = np.zeros((z2-z1,lt2-lt1,lonindmax))
    v_strat = np.zeros((z2-z1,lt2-lt1,lonindmax))
    for i in xrange(lonindmax):
        u_strat[:,:,i] = 0.5*(u_strat_temp[:,:,i]+u_strat_temp[:,:,i+1])
    for i in xrange(lt2-lt1):
        v_strat[:,i,:] = 0.5*(v_strat_temp[:,i,:]+v_strat_temp[:,i,:])
    print 'Interp done'
    ##KE
    KE_strat = ne.evaluate('0.5*(u_strat**2+v_strat**2)')
    
    splitind = range(0,lt2-lt1,(lt2-lt1)/processes)
    pool = Pool(processes=processes)
    TASKS = [(KE_strat,lon[:],(lt2-lt1)/processes,n) for n in splitind]
    meansection = [pool.apply_async(splitfft2dheight, t) for t in TASKS]
    print 'Parallel section done'
    
    power = meansection[0].get()
    for i in xrange(1,processes):
        power = 0.5*(power+meansection[i].get())
    print 'Mean done'
    n = len(lon[:])
    dx = lon[1]-lon[0]
    nu = fft.fftfreq(n,dx)
    nu = 360*fft.fftshift(nu)

    ax = plt.subplot(subplot[0],subplot[1],subplot[2])
    plt.contourf(nu[len(nu)/2+1:],z[z1:z2]/1000,power[:,len(nu)/2+1:],\
                    norm=LogNorm(),cmap='Oranges',\
                    levels=[1e-7,1e-5,1e-3,1e-1,10,1000,1e5,1e7])
    ax.set_xscale('log')
    plt.colorbar()
    plt.title('%s, %s from %d to %d deg N, %s' % (model,month,lat[lt1],\
                            lat[lt2-1],zrange))
    plt.ylabel('Height (km)')
    scale = 360.
    plt.xlabel('Wavenumber',labelpad = labelpad)
    
def onelat_contourpower(model,month,subplot,lattarg,zrange,labelpad = 0,processes = 4):
    ''' Draws a contour of the power for wavenumber vs height
    
        takes only data from first year
    '''
    if lattarg == '2.5S':
        if model == 'xjanp':
            latval = 373
        if model == 'xjlef':
            latval = 157
    else: raise ValueError("only valid lat targs: \n '2.5'")

    if model == 'xjanp':
        lonindmax = 1024
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
    elif model == 'xjlef': 
        lonindmax = 432
        if month == 'sep': monthval=0
        else: raise ValueError('only september in xjlef')
    else: raise ValueError('xjanp or xjlef only')

    path = '/group_workspaces/jasmin/hiresgw/mj07/monthly_means/'
    filenameu = model+'a.monthlymean.u.nc'
    filenamev = model+'a.monthlymean.v.nc'

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
    elif zrange == 'all':
        z1 = 0
        z2 = 180
    else: raise ValueError('Height entered wrong!')
    

    # take single timestep slice over the tropics in strat NH only
    u_strat_temp = np.append(u[monthval,z1:z2,latval,:],u[monthval,z1:z2,latval,0:1],axis=1)
    v_strat_temp =  v[monthval,z1:z2,latval:latval+2,:]

    ###interpolation
    u_strat = np.zeros((z2-z1,lonindmax))
    v_strat = np.zeros((z2-z1,lonindmax))
    for i in xrange(lonindmax):
        u_strat[:,i] = 0.5*(u_strat_temp[:,i]+u_strat_temp[:,i+1])
    v_strat[:,:] = 0.5*(v_strat_temp[:,0,:]+v_strat_temp[:,1,:])
    print 'Interp done'
    ##KE
    KE = ne.evaluate('0.5*(u_strat**2+v_strat**2)')
    
    n = len(lon[:])
    dx = lon[1]-lon[0]
    
    Fk = fft.fft(KE)/n
    Fk = fft.fftshift(Fk,axes=1)
    nu = fft.fftfreq(n,dx)
    power = np.absolute(Fk)**2

    nu = 360*fft.fftshift(nu)

    ax = plt.subplot(subplot[0],subplot[1],subplot[2])
    plt.contourf(nu[len(nu)/2+1:],z[z1:z2]/1000,power[:,len(nu)/2+1:],\
                    norm=LogNorm(),cmap='Oranges',\
                    levels=[1e-7,1e-5,1e-3,1e-1,10,1000,1e5,1e7])
    ax.set_xscale('log')
    plt.colorbar()
    plt.title('%s, %s at %f deg N, %s' % (model,month,lat[latval],zrange))
    plt.ylabel('Height (km)')
    scale = 360.
    plt.xlabel('Wavenumber',labelpad = labelpad)
    

fig = plt.figure(frameon=False,figsize=(9,9))
monthfield(model='xjlef',month='sep', subplot=[2,1,1], latrange=[162,216], zrange='strat',processes=2)
monthfield(model='xjleh',month='sep', subplot=[2,1,1], latrange=[162,216], zrange='strat',processes=2)
monthfield(model='xjanp',month='sep', subplot=[2,1,1], latrange=[384,512], zrange='strat',processes=2)
plt.legend(loc=3)
monthfield(model='xjlef',month='sep', subplot=[2,1,2], latrange=[216,270], zrange='strat',processes=2)
monthfield(model='xjleh',month='sep', subplot=[2,1,2], latrange=[216,270], zrange='strat',processes=2)
monthfield(model='xjanp',month='sep', subplot=[2,1,2], latrange=[512,640], zrange='strat',processes=2)
plt.legend(loc=3)

#monthfield(model='xjlef',month='sep', subplot=[3,1,3], latrange=[0,324], zrange='trop',processes=2,labelpad=-15)
#monthfield(model='xjlef',month='sep', subplot=[2,2,2], latrange=[0,162], zrange='all',processes=2)
#monthfield(model='xjanp',month='sep', subplot=[2,2,3], latrange=[384,768], zrange='all',processes=2)
#monthfield(model='xjlef',month='sep', subplot=[2,2,4], latrange=[162,324], zrange='all',processes=2)
#contourpower(model='xjlef',month='sep', subplot=[2,2,1], latrange=[162,216], zrange='all',processes=2)
#contourpower(model='xjlef',month='sep', subplot=[2,2,2], latrange=[216,270], zrange='all',processes=2)
#contourpower(model='xjanp',month='sep', subplot=[2,2,3], latrange=[384,512], zrange='all',processes=2)
#contourpower(model='xjanp',month='sep', subplot=[2,2,4], latrange=[512,640], zrange='all',processes=2)

#onelat_contourpower(model='xjanp',month='sep', subplot=[2,1,1], lattarg='2.5S', zrange='all',processes=2)
#onelat_contourpower(model='xjlef',month='sep', subplot=[2,1,2], lattarg='2.5S', zrange='all',processes=2)

myplot.addInfo(fig,filename='compare_xjanp_xjlef_xjleh.py')
plt.show()#plt.savefig('pcolor_test.pdf')
