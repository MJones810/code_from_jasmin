#!/usr/bin/env python2.7
''' time mean, height and lat mean on ffts '''

import numpy as np
from numpy import fft
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import myplot
from matplotlib.colors import LogNorm
from jug import TaskGenerator, barrier, value, bvalue
from jug import mapreduce
activate_this = '/home/users/mjones07/science/venv/bin/activate_this.py'
execfile(activate_this,dict(__file__=activate_this))
import numexpr as ne
from time import time
from multiprocessing import Pool

def fft_task(info):
    model,timestep,date,lt1,lt2,z1,z2 = info.split(',')
    timestep = int(timestep)
    lt1 = int(lt1)
    lt2 = int(lt2)
    z1 = int(z1)
    z2 = int(z2)
    path = '/group_workspaces/jasmin/hiresgw/mj07/'
    fileu = model+'a.'+date+'.u.nc'
    filev = model+'a.'+date+'.v.nc'

    fu = Dataset(path+fileu,'r')
    fv = Dataset(path+filev,'r')
    u = fu.variables['u']
    v = fv.variables['v']   
    lon = fv.variables['longitude']
    lonindmax = len(lon)

    # take single timestep slice over the tropics in strat NH only
    u_strat_temp = np.append(u[timestep,z1:z2,lt1:lt2,:],u[timestep,z1:z2,lt1:lt2,0:1],axis=2)
    v_strat_temp =  v[timestep,z1:z2,lt1:lt2+1,:]

    ###interpolation
    u_strat = np.zeros((z2-z1,lt2-lt1,lonindmax))
    v_strat = np.zeros((z2-z1,lt2-lt1,lonindmax))
    for i in xrange(lonindmax):
        u_strat[:,:,i] = 0.5*(u_strat_temp[:,:,i]+u_strat_temp[:,:,i+1])
    for i in xrange(lt2-lt1):
        v_strat[:,i,:] = 0.5*(v_strat_temp[:,i,:]+v_strat_temp[:,i,:])
    ##KE
    KE = ne.evaluate('0.5*(u_strat**2+v_strat**2)')
    del u_strat_temp,v_strat_temp,u_strat,v_strat
    n = len(lon)
    dx = lon[1]-lon[0]
    Fk = fft.fft(KE)/n
    Fk = fft.fftshift(Fk,axes=2)
    nu = fft.fftfreq(n,dx)
    nu = fft.fftshift(nu)
    del KE
    power = np.absolute(Fk)**2
    powermean1 = power[0,:,:]
    for i in xrange(1,power.shape[0]):
        powermean1 = 0.5*(powermean1+power[i,:,:])
    powermean2 = powermean1[0,:]
    for i in xrange(1,powermean1.shape[0]):
        powermean2 = 0.5*(powermean2+powermean1[i,:])

    return powermean2,nu


def main(startinfo,timestep):
    
    model,date,zrange,latrange = startinfo.split(',')
    if latrange == 'SH':
        if model == 'xjanp':
            lat1 = 0
            lat2 = 384
        elif model == 'xjlef' or model == 'xjleh':
            lat1 = 0    
            lat2 = 162
    elif latrange == 'NH':
        if model == 'xjanp':
            lat1 = 384
            lat2 = 768
        elif model == 'xjlef' or model == 'xjleh':
            lat1 = 162    
            lat2 = 324
    elif latrange == 'NHtrop':
        if model == 'xjanp':
            lat1 = 384
            lat2 = 512
        elif model == 'xjlef' or model == 'xjleh':
            lat1 = 162
            lat2 = 216
    elif latrange == 'NHextrop':
        if model == 'xjanp':
            lat1 = 512
            lat2 = 640
        elif model == 'xjlef' or model == 'xjleh':
            lat1 = 216
            lat2 = 270
    elif latrange == 'SHtrop': 
        if model == 'xjanp':
            lat1 = 256
            lat2 = 384
        elif model == 'xjlef' or model == 'xjleh':
            lat1 = 108
            lat2 = 162
    elif latrange == 'SHextrop':
        if model == 'xjanp':    
            lat1 = 128
            lat2 = 256
        elif model == 'xjlef' or model == 'xjleh':
            lat1 = 54
            lat2 = 108
        
    else: raise ValueError('finish me')
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
    if ((lat2-lat1)*(z2-z1)*1024)>(384*180*1024):
        raise ValueError('Array too large - will probably break')
    infolist = []
    
    info = '%s,%s,%s,%s,%s,%s,%s' % (model,timestep,date,lat1,lat2,z1,z2)
   
    powermean,nu = fft_task(info)
    return powermean,nu


def subtask(info,processes,timestep):
    
    powermean,nu = main(info,timestep=0)
    for i in xrange(timestep+1,timestep+(240/processes)):
        powermean = 0.5*(powermean+main(info,timestep=i)[0])
    return powermean,nu

def plotting_task(infostring):
    processes = 24
    splitind = range(0,240,240/processes)
    pool = Pool(processes=processes)
    TASKS = [(infostring,processes,t) for t in splitind]
    powersection = [pool.apply_async(subtask, t) for t in TASKS]
    powermean,nu = powersection[0].get()
    for i in xrange(1,processes):
        powermean = 0.5*(powermean+powersection[i].get()[0])
    nu = 360*nu
    plt.loglog(nu,powermean,label=infostring)
    plt.xlim(1,1000)
    plt.ylim(10**-8,10**6)
    plt.xlabel('Wavenumber')
    plt.ylabel('Power')
    nu3 = (nu[len(nu)/2+1:])**-3
    nu53 = (nu[len(nu)/2+1:])**-(5/3)
    plt.loglog(100*nu[len(nu)/2+1:-len(nu)/3],10**6*nu3[:-len(nu)/3],'k')
    plt.loglog(100*nu[len(nu)/2+1:-len(nu)/3],10**6*nu53[:-len(nu)/3],'k')

def starter():
    infostrings = ['xjanp,19920121,strat,NHextrop',\
                   'xjanp,19920421,strat,NHextrop',\
                   'xjanp,19920721,strat,NHextrop',\
                   'xjanp,19921021,strat,NHextrop']
    fig = plt.figure(figsize=(9,9))
    for infostring in infostrings:
        print infostring
        plotting_task(infostring)
    plt.legend(loc=3)
    myplot.addInfo(fig,filename='fft_timemean.py')
    plt.savefig('xjanp_seasons_extropics.pdf')
start = time()
starter()
print 'time taken : %f' % (time()-start)
