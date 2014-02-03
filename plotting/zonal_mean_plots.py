#!/usr/bin/env python2.7
''' Zonal mean plots. 
'''

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def timeheight():
    u_zonalmean_at_2degS = u[:,:,lat_val,0]

    vmin = -100
    vmax = 100
    levs = 24
    lat_val = 374

    for i in xrange(1,len(u[0,0,0,:])):
        
        u_zonalmean_at_2degS = (u_zonalmean_at_2degS+u[:,:,lat_val,i])/2#

        if i%50 == 0: print 't-z -2deg : ',i
    plt.figure()
    plt.contourf(t,z,u_zonalmean_at_2degS.T,levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(t,z,u_zonalmean_at_2degS.T,levels=[0],linewidth=2,colors='w')
    plt.xlabel('Months since start of model')
    plt.ylabel('Hybrid height (m)')
    plt.title('Time series of zonal mean at %d deg N' % lat[lat_val])
    plt.show()

# height lat plots
def heightlat():
    april = 1
    july = 4
    octob = 7
    jan = 9

    vmin = -140
    vmax = 140
    levs = 24

    u_zonalmean_april = u[april,:,:,0]
    u_zonalmean_july= u[july,:,:,0]
    u_zonalmean_octob = u[octob,:,:,0]
    u_zonalmean_jan = u[jan,:,:,0]

    for i in xrange(1,len(u[0,0,0,:])):
        
        u_zonalmean_april = (u_zonalmean_april+u[april,:,:,i])/2
        u_zonalmean_july = (u_zonalmean_july+u[july,:,:,i])/2
        u_zonalmean_octob = (u_zonalmean_octob+u[octob,:,:,i])/2
        u_zonalmean_jan = (u_zonalmean_jan+u[jan,:,:,i])/2
        
        if i%50 == 0: print 'y-z : ',i

    plt.figure()
    plt.suptitle('height-lat zonalmean plots')
    plt.subplot(2,2,1)
    plt.contourf(lat,z,u_zonalmean_april,levs,vmin=vmin,vmax=vmax)
    plt.ylabel('hybrid height')
    plt.title('April')
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u_zonalmean_april,levels=[0],linewidth=2,colors='w')
    plt.subplot(2,2,2)
    plt.contourf(lat,z,u_zonalmean_july,levs,vmin=vmin,vmax=vmax)
    plt.title('July')
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u_zonalmean_july,levels=[0],linewidth=2,colors='w')
    plt.subplot(2,2,3)
    plt.contourf(lat,z,u_zonalmean_octob,levs,vmin=vmin,vmax=vmax)
    plt.ylabel('hybrid height')
    plt.xlabel('latitude')
    plt.title('October')
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u_zonalmean_octob,levels=[0],linewidth=2,colors='w')
    plt.subplot(2,2,4)
    plt.contourf(lat,z,u_zonalmean_jan,levs,vmin=vmin,vmax=vmax)
    plt.xlabel('latitude')
    plt.title('january')
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u_zonalmean_jan,levels=[0],linewidth=2,colors='w')
    plt.show()
    
def heightlat2():
    ''' to look at winter period '''
    april = 1 
    july = 11 #### ----->>>>>> feb
    octob = 0 #### ----->>>>> march
    jan = 10  

    vmin = -140
    vmax = 140
    levs = 24

    u_zonalmean_april = u[april,:,:,0]
    u_zonalmean_july= u[july,:,:,0]
    u_zonalmean_octob = u[octob,:,:,0]
    u_zonalmean_jan = u[jan,:,:,0]

    for i in xrange(1,len(u[0,0,0,:])):
        
        u_zonalmean_april = (u_zonalmean_april+u[april,:,:,i])/2
        u_zonalmean_july = (u_zonalmean_july+u[july,:,:,i])/2
        u_zonalmean_octob = (u_zonalmean_octob+u[octob,:,:,i])/2
        u_zonalmean_jan = (u_zonalmean_jan+u[jan,:,:,i])/2
        
        if i%50 == 0: print 'y-z : ',i

    plt.figure()
    plt.suptitle('height-lat zonalmean plots')
    plt.subplot(2,2,1)
    plt.contourf(lat,z,u_zonalmean_april,levs,vmin=vmin,vmax=vmax)
    plt.ylabel('hybrid height')
    plt.title('April')
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u_zonalmean_april,levels=[0],linewidth=2,colors='w')
    plt.subplot(2,2,2)
    plt.contourf(lat,z,u_zonalmean_july,levs,vmin=vmin,vmax=vmax)
    plt.title('feb')
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u_zonalmean_july,levels=[0],linewidth=2,colors='w')
    plt.subplot(2,2,3)
    plt.contourf(lat,z,u_zonalmean_octob,levs,vmin=vmin,vmax=vmax)
    plt.ylabel('hybrid height')
    plt.xlabel('latitude')
    plt.title('march')
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u_zonalmean_octob,levels=[0],linewidth=2,colors='w')
    plt.subplot(2,2,4)
    plt.contourf(lat,z,u_zonalmean_jan,levs,vmin=vmin,vmax=vmax)
    plt.xlabel('latitude')
    plt.title('january')
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u_zonalmean_jan,levels=[0],linewidth=2,colors='w')
    plt.show()

def heightlat3():
    ''' to look around october '''
    april = 5 #### ---->>>> august
    july = 6 #### ----->>>>>> sept
    octob = 7 
    jan = 8  #### ------>>>> nov

    vmin = -140
    vmax = 140
    levs = 24

    u_zonalmean_april = u[april,:,:,0]
    u_zonalmean_july= u[july,:,:,0]
    u_zonalmean_octob = u[octob,:,:,0]
    u_zonalmean_jan = u[jan,:,:,0]

    for i in xrange(1,len(u[0,0,0,:])):
        
        u_zonalmean_april = (u_zonalmean_april+u[april,:,:,i])/2
        u_zonalmean_july = (u_zonalmean_july+u[july,:,:,i])/2
        u_zonalmean_octob = (u_zonalmean_octob+u[octob,:,:,i])/2
        u_zonalmean_jan = (u_zonalmean_jan+u[jan,:,:,i])/2
        
        if i%50 == 0: print 'y-z : ',i

    plt.figure()
    plt.suptitle('height-lat zonalmean plots')
    plt.subplot(2,2,1)
    plt.contourf(lat,z,u_zonalmean_april,levs,vmin=vmin,vmax=vmax)
    plt.ylabel('hybrid height')
    plt.title('August')
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u_zonalmean_april,levels=[0],linewidth=2,colors='w')
    plt.subplot(2,2,2)
    plt.contourf(lat,z,u_zonalmean_july,levs,vmin=vmin,vmax=vmax)
    plt.title('sept')
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u_zonalmean_july,levels=[0],linewidth=2,colors='w')
    plt.subplot(2,2,3)
    plt.contourf(lat,z,u_zonalmean_octob,levs,vmin=vmin,vmax=vmax)
    plt.ylabel('hybrid height')
    plt.xlabel('latitude')
    plt.title('oct')
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u_zonalmean_octob,levels=[0],linewidth=2,colors='w')
    plt.subplot(2,2,4)
    plt.contourf(lat,z,u_zonalmean_jan,levs,vmin=vmin,vmax=vmax)
    plt.xlabel('latitude')
    plt.title('nov')
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u_zonalmean_jan,levels=[0],linewidth=2,colors='w')
    plt.show()

def yzsections():
    ''' for a given long plots lat height profiles for inst field '''
    
    april = 1
    july = 4
    octob = 7
    jan = 9
    lon_ind = 350
    t_ind = 120
    vmin = -140
    vmax = 140
    levs = 24

    plt.figure()
    plt.suptitle('y-z sections at %f deg E, instantaneous taken half way through month' % lon[lon_ind])
    ### APRIL ###
    plt.subplot(4,2,1)
    plt.contourf(lat,z,u[april,:,:,lon_ind],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u[april,:,:,lon_ind],levels=[0],linewidth=2,colors='w')
    plt.title('April Monthly mean')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    plt.subplot(4,2,2)
    plt.contourf(lat,z,u_april[t_ind,:,:,lon_ind],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u_april[t_ind,:,:,lon_ind],levels=[0],linewidth=2,colors='w')
    plt.title('April instantaneous')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    ### July ###
    plt.subplot(4,2,3)
    plt.contourf(lat,z,u[july,:,:,lon_ind],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u[july,:,:,lon_ind],levels=[0],linewidth=2,colors='w')
    plt.title('July Monthly mean')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    plt.subplot(4,2,4)
    plt.contourf(lat,z,u_july[t_ind,:,:,lon_ind],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u_july[t_ind,:,:,lon_ind],levels=[0],linewidth=2,colors='w')
    plt.title('July instantaneous')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    ### Oct ###
    plt.subplot(4,2,5)
    plt.contourf(lat,z,u[octob,:,:,lon_ind],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u[octob,:,:,lon_ind],levels=[0],linewidth=2,colors='w')
    plt.title('October Monthly mean')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    plt.subplot(4,2,6)
    plt.contourf(lat,z,u_oct[t_ind,:,:,lon_ind],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u_oct[t_ind,:,:,lon_ind],levels=[0],linewidth=2,colors='w')
    plt.title('October instantaneous')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    ### Jan ###
    plt.subplot(4,2,7)
    plt.contourf(lat,z,u[jan,:,:,lon_ind],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u[jan,:,:,lon_ind],levels=[0],linewidth=2,colors='w')
    plt.title('January Monthly mean')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    plt.subplot(4,2,8)
    plt.contourf(lat,z,u_jan[t_ind,:,:,lon_ind],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lat,z,u_jan[t_ind,:,:,lon_ind],levels=[0],linewidth=2,colors='w')
    plt.title('January instantaneous')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    #plt.tight_layout()
    plt.show()

def xzsections():
    ''' for a given lat plots long height profiles for inst field '''
    
    april = 1
    july = 4
    octob = 7
    jan = 9
    lat_ind = 374
    t_ind = 120
    vmin = -140
    vmax = 140
    levs = 24

    plt.figure()
    plt.suptitle('x-z sections at %f deg N, instantaneous taken half way through month' % lat[lat_ind])
    ### APRIL ###
    plt.subplot(4,2,1)
    plt.contourf(lon,z,u[april,:,lat_ind,:],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lon,z,u[april,:,lat_ind,:],levels=[0],linewidth=2,colors='w')
    plt.title('April Monthly mean')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    plt.subplot(4,2,2)
    plt.contourf(lon,z,u_april[t_ind,:,lat_ind,:],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lon,z,u_april[t_ind,:,lat_ind,:],levels=[0],linewidth=2,colors='w')
    plt.title('April instantaneous')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    ### July ###
    plt.subplot(4,2,3)
    plt.contourf(lon,z,u[july,:,lat_ind,:],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lon,z,u[july,:,lat_ind,:],levels=[0],linewidth=2,colors='w')
    plt.title('July Monthly mean')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    plt.subplot(4,2,4)
    plt.contourf(lon,z,u_july[t_ind,:,lat_ind,:],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lon,z,u_july[t_ind,:,lat_ind,:],levels=[0],linewidth=2,colors='w')
    plt.title('July instantaneous')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    ### Oct ###
    plt.subplot(4,2,5)
    plt.contourf(lon,z,u[octob,:,lat_ind,:],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lon,z,u[octob,:,lat_ind,:],levels=[0],linewidth=2,colors='w')
    plt.title('October Monthly mean')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    plt.subplot(4,2,6)
    plt.contourf(lon,z,u_oct[t_ind,:,lat_ind],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lon,z,u_oct[t_ind,:,lat_ind],levels=[0],linewidth=2,colors='w')
    plt.title('October instantaneous')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    ### Jan ###
    plt.subplot(4,2,7)
    plt.contourf(lon,z,u[jan,:,lat_ind,:],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lon,z,u[jan,:,lat_ind,:],levels=[0],linewidth=2,colors='w')
    plt.title('January Monthly mean')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    plt.subplot(4,2,8)
    plt.contourf(lon,z,u_jan[t_ind,:,lat_ind,:],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lon,z,u_jan[t_ind,:,lat_ind,:],levels=[0],linewidth=2,colors='w')
    plt.title('January instantaneous')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    #plt.tight_layout()
    plt.show()

def xysections():
    ''' for a given height plots long lat profiles for inst field '''
    
    april = 1
    july = 4
    octob = 7
    jan = 9
    z_ind = 140
    t_ind = 120
    vmin = -100
    vmax = 100
    levs = 24

    plt.figure()
    plt.suptitle('x-y sections at %f m, instantaneous taken half way through month' % z[z_ind])
    ### APRIL ###
    plt.subplot(4,2,1)
    plt.contourf(lon,lat,u[april,z_ind,:,:],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lon,lat,u[april,z_ind,:,:],levels=[0],linewidth=2,colors='w')
    plt.title('April Monthly mean')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    plt.subplot(4,2,2)
    plt.contourf(lon,lat,u_april[t_ind,z_ind,:,:],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lon,lat,u_april[t_ind,z_ind,:,:],levels=[0],linewidth=2,colors='w')
    plt.title('April instantaneous')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    ### July ###
    plt.subplot(4,2,3)
    plt.contourf(lon,lat,u[july,z_ind,:,:],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lon,lat,u[july,z_ind,:,:],levels=[0],linewidth=2,colors='w')
    plt.title('July Monthly mean')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    plt.subplot(4,2,4)
    plt.contourf(lon,lat,u_july[t_ind,z_ind,:,:],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lon,lat,u_july[t_ind,z_ind,:,:],levels=[0],linewidth=2,colors='w')
    plt.title('July instantaneous')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    ### Oct ###
    plt.subplot(4,2,5)
    plt.contourf(lon,lat,u[octob,z_ind,:,:],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lon,lat,u[octob,z_ind,:,:],levels=[0],linewidth=2,colors='w')
    plt.title('October Monthly mean')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    plt.subplot(4,2,6)
    plt.contourf(lon,lat,u_oct[t_ind,z_ind,:,:],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lon,lat,u_oct[t_ind,z_ind,:,:],levels=[0],linewidth=2,colors='w')
    plt.title('October instantaneous')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    ### Jan ###
    plt.subplot(4,2,7)
    plt.contourf(lon,lat,u[jan,z_ind,:,:],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lon,lat,u[jan,z_ind,:,:],levels=[0],linewidth=2,colors='w')
    plt.title('January Monthly mean')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    plt.subplot(4,2,8)
    plt.contourf(lon,lat,u_jan[t_ind,z_ind,:,:],levs,vmin=vmin,vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.contour(lon,lat,u_jan[t_ind,z_ind,:,:],levels=[0],linewidth=2,colors='w')
    plt.title('January instantaneous')
    #plt.xlabel('Lat (deg N)')
    #plt.ylabel('Hybrid Height (m)')
    #plt.tight_layout()
    plt.show()

def yzannualzonalmean():
    ''' y-z section of annual mean of zonal mean '''

    vmin = -140
    vmax = 140
    levs = 24

    u_annual = np.mean(u[:,::2,::10,::10],0)
    print u_annual.shape()

    #for i in xrange(1,len(u[0,0,0,:])):
        
        #u_zonalmean = (u_zonalmean+u[april,:,:,i])/2
        #u_zonalmean_july = (u_zonalmean_july+u[july,:,:,i])/2
        #u_zonalmean_octob = (u_zonalmean_octob+u[octob,:,:,i])/2
        #u_zonalmean_jan = (u_zonalmean_jan+u[jan,:,:,i])/2
        
        #if i%50 == 0: print 'y-z : ',i

    #plt.figure()
    #plt.suptitle('height-lat zonalmean plots')
    #plt.subplot(2,2,1)
    #plt.contourf(lat,z,u_zonalmean_april,levs,vmin=vmin,vmax=vmax)
    #plt.ylabel('hybrid height')
    #plt.title('April')
    #plt.colorbar(orientation='horizontal')
    #plt.contour(lat,z,u_zonalmean_april,levels=[0],linewidth=2,colors='w'

filename = '/group_workspaces/jasmin/hiresgw/mj07/monthly_means/xjanpa.monthlymean.u.nc'
f = Dataset(filename,'r')
u = f.variables['u']
lat = f.variables['latitude']
lon = f.variables['longitude']
t = f.variables['time']
z = f.variables['z_hybrid_height']

file_april = '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj19910411.u.nc'
f_april = Dataset(file_april,'r')
u_april = f_april.variables['u']
t_april = f_april.variables['time']

file_july = '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj19910611.u.nc'
f_july = Dataset(file_july,'r')
u_july = f_july.variables['u']
t_july = f_july.variables['time']

file_oct = '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj19911011.u.nc'
f_oct = Dataset(file_oct,'r')
u_oct = f_oct.variables['u']
t_oct = f_oct.variables['time']

file_jan = '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj19920111.u.nc'
f_jan = Dataset(file_jan,'r')
u_jan = f_jan.variables['u']
t_jan = f_jan.variables['time']

yzannualzonalmean()
