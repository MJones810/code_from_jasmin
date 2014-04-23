#!/usr/bin/env python2.7
''' Code to plot the KE spectrum of the models xjanp, xjlef or xjleh 
    using numpy fft. '''

import numpy as np
from numpy import fft
import matplotlib
matplotlib.use('Agg') # used on lotus to supress a display coming through
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




def fft_task(startinfo,timestep):
    ''' Calculates the fft for each longitude slice over the region 
        defined in startinfo then takes the average.
    '''
    
    model,date,zrange,latrange,colour = startinfo.split(',')
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
        
    else: raise ValueError('latrange not implemented')
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
    u_strat_temp = np.append(u[timestep,z1:z2,lat1:lat2,:],\
                        u[timestep,z1:z2,lat1:lat2,0:1],axis=2)
    v_strat_temp =  v[timestep,z1:z2,lat1:lat2+1,:]

    ###interpolation
    u_strat = np.zeros((z2-z1,lat2-lat1,lonindmax))
    v_strat = np.zeros((z2-z1,lat2-lat1,lonindmax))
    for i in xrange(lonindmax):
        u_strat[:,:,i] = 0.5*(u_strat_temp[:,:,i]+u_strat_temp[:,:,i+1])
    for i in xrange(lat2-lat1):
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

def fftwrap(info,processes,timestep):
    ''' Function that is distributed using multiprocessing.
        Calls fft function to calculate the fft then does a time 
        average on them for the required number of timesteps.

    '''
    powermean,nu = fft_task(info,timestep=0)
    for i in xrange(timestep+1,timestep+(240/processes)):
        powermean = 0.5*(powermean+fft_task(info,timestep=i)[0])
    return powermean,nu

def plotting_task(infostring,plot=True):
    ''' Distributes the calculation of the ffts over 24 processors
        (split along time axis). Will plot the resulting averaged fft 
        if plot=True. Returns the averaged fft array and 

    '''

    model,date,zrange,latrange,colour = infostring.split(',')
    processes = 24
    splitind = range(0,240,240/processes)
    pool = Pool(processes=processes)
    TASKS = [(infostring,processes,t) for t in splitind]
    powersection = [pool.apply_async(fftwrap, t) for t in TASKS]
    powermean,nu = powersection[0].get()
    for i in xrange(1,processes):
        powermean = 0.5*(powermean+powersection[i].get()[0])
    nu = 360*nu
    if plot:
        plt.loglog(nu,powermean,colour,label=infostring)
    plt.xlim(1,1000)
    plt.ylim(10**-8,10**6)
    plt.xlabel('Wavenumber')
    plt.ylabel('Power')
    nu3 = (nu[len(nu)/2+1:])**-3
    nu53 = (nu[len(nu)/2+1:])**-(5/3)
    plt.loglog(100*nu[len(nu)/2+1:-len(nu)/3],10**6*nu3[:-len(nu)/3],'k')
    plt.loglog(100*nu[len(nu)/2+1:-len(nu)/3],10**6*nu53[:-len(nu)/3],'k')
    return nu,powermean

def plotwrap(infostrings,legendlab=None,hexcolor=None,linecolor=None,\
             mon_mean=False):   
    ''' Calls the plotting function multiple time depending on whether
        mon mean is true or false. 

            
        If mon_mean=True then calculates the average fft for each of the 
        input files and averages them and puts a shaded range of the input 
        to the average (at the moment only deals with 3 input files.
        If False then only plots the single input file given.

        hexcolor defines the color used in the area plot of the
        range for the average (used if mon_mean=True). 
        (blue: #b2b2ff, green: #99cc99, red: #ff7f7f)
        
        linecolor defines the colour of the mean line over multiple 
        files (used if mon_mean=True).
        
        legendlab (only used if mon_mean=True) defines the label for
        the mean line in the legend.
    '''
    if mon_mean:
        if len(infostrings)!=3:
            raise ValueError('Only implemented for 3 files at once!')
        nu,powerarray1 = plotting_task(infostrings[0],False)
        array_to_mean = np.zeros((len(powerarray1),3))
        array_to_mean[:,0] = powerarray1[:]
        #for i in xrange(1,len(infostrings)):
        powerarray2 = plotting_task(infostrings[1],False)[1]
        array_to_mean[:,1] = powerarray2[:]
        powerarray3 = plotting_task(infostrings[2],False)[1]
        array_to_mean[:,2] = powerarray3[:]
        mon_mean_array = np.mean(array_to_mean,axis=1)
        plt.fill_between(nu, powerarray1, powerarray2,
            alpha=0.2, edgecolor=hexcolor, facecolor=hexcolor)
        plt.fill_between(nu, powerarray1, powerarray3,
            alpha=0.2, edgecolor=hexcolor, facecolor=hexcolor)
        plt.fill_between(nu, powerarray2, powerarray3,
            alpha=0.2, edgecolor=hexcolor, facecolor=hexcolor)
        plt.plot(nu,mon_mean_array,linecolor,label=legendlab,linewidth=1)
    else:
        for infostring in infostrings:
            print infostring
            plotting_task(infostring)
    


def starter():
    ''' function that sends the initial conditions to the other 
        functions. 
        
        Done this way as a clean entry into everything else.

        Examples
        1)    3 file average over a month: 
        infostrings = ['xjanp,19920901,trop,NHextrop,b',\
                       'xjanp,19920911,trop,NHextrop,b',\
                       'xjanp,19920921,trop,NHextrop,b']
        plotwrap(infostrings,legendlab='xjanp oct tropos extropics',mon_mean=True,\
                hexcolor='#b2b2ff',linecolor='b')
        # NB that more than one of these lines can be plotted by 
          repeating the code for a different set of files

        2) 2 files on one plot
        infostrings = ['xjlef,19810901,trop,NHextrop,b',\
                       'xjleh,19810901,trop,NHextrop,g']
        plotwrap(infostrings)
        # NB to repeat for these files add more files into infostrings

    '''
    fig = plt.figure(figsize=(9,9))

    infostrings = ['xjanp,19920901,trop,NHextrop,b',\
                       'xjanp,19920911,trop,NHextrop,b',\
                       'xjanp,19920921,trop,NHextrop,b']
    plotwrap(infostrings,legendlab='xjanp oct tropos extropics',mon_mean=True,\
            hexcolor='#b2b2ff',linecolor='b')
    
    plt.legend(loc=3)
    myplot.addInfo(fig,filename='fft_timemean.py')
    plt.savefig('newtest.pdf')
start = time()
starter()
print 'time taken : %f' % (time()-start)
