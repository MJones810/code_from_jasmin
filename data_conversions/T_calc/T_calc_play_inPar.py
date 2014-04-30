#!/usr/bin/env python2.7
''' playin trying to get the temp from pot temp and pressure :- PARALLEL'''

from netCDF4 import Dataset
import numpy as np
activate_this = '/home/users/mjones07/science/venv/bin/activate_this.py'
execfile(activate_this,dict(__file__=activate_this))
import numexpr as ne
import time as timepack
from multiprocessing import Pool
from glob import glob

def hourspassed(date,t):
    ''' Function to work out hours passed since 1991-03-01 00:00:00.

    Asumes 360 day calendar.
    '''
    startyear = 1991
    startmonth = 03
    startday = 01
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[-2:])

    yearspass = year-startyear     
    monthspass = month-startmonth
    dayspass = day-startday
    
    hourspass = ((yearspass*360+monthspass*30)+dayspass)*24 + t
    return hourspass

def createfile(filename):
    ''' Creates the netCDF file to then be opened in field2nc. 
    '''
    
    f = Dataset(filename,'w')

    zres = 180
    latres = 768
    lonres = 1024
    # Create dimensions
    time = f.createDimension('time',None)
    z_hybrid_height = f.createDimension('z_hybrid_height',zres)
    latitude = f.createDimension('latitude',latres)
    longitude = f.createDimension('longitude',lonres)

    # Create variables (added s on the end to differentiate between dimensions
    #                   and variables)
    times = f.createVariable('time','f4',('time',),zlib=True)
    z_hybrid_heights = f.createVariable('z_hybrid_height','f4',
                                        ('z_hybrid_height',),zlib=True)
    latitudes = f.createVariable('latitude','f4',('latitude',),zlib=True)
    longitudes = f.createVariable('longitude','f4',('longitude',),zlib=True)
    v = f.createVariable('T','f4',('time','z_hybrid_height','latitude',
                                   'longitude',),zlib=True)

    # Add in attributes
    f.Conventions = 'CF-1.6'
    times.units = 'hours since 1991-03-01 00:00:00'
    times.standard_name = 'time'
    times.calendar = '360_day'
    times.axis = 'T'
    z_hybrid_heights.positive = 'up'
    z_hybrid_heights.long_name = 'atmosphere hybrid height coordinate'
    z_hybrid_heights.standard_name = 'atmosphere_hybrid_height_coordinate'
    z_hybrid_heights.units = 'm'
    z_hybrid_heights.axis = 'Z'
    latitudes.bounds = 'bounds_latitude'
    latitudes.units = 'degrees_north'
    latitudes.standard_name = 'latitude'
    latitudes.point_spacing = 'even'
    latitudes.axis = 'Y'
    longitudes.bounds = 'bounds_longitude'
    longitudes.modulo = 360.
    longitudes.point_spacing = 'even'
    longitudes.standard_name = 'longitude'
    longitudes.units = 'degrees_east'
    longitudes.axis = 'X'
    longitudes.topology = 'circular'
    v.lookup_source = 'defaults (cdunifpp V0.14pre1)'
    v.standard_name = 'air_temperature'
    v.long_name = 'AIR TEMPERATURE'
    v.units = 'K'
    v.missing_value = -1.073742e+09

    # Add in values of lat, lon and height
    coordsfile = '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pb19910301.theta.nc'
    f2 = Dataset(coordsfile,'r')
    latvals = f2.variables['latitude']
    lonvals = f2.variables['longitude']
    zvals = f2.variables['z_hybrid_height']
    
    latitudes[:] = latvals[:]
    longitudes[:] = lonvals[:]
    z_hybrid_heights[:] = zvals[:]
    f2.close()

    f.close()

def splitfilecalc(filename,n):
    ''' Calculate the mean of the section for individual files , which 
        starts at n and is 40 long.
    '''
    
    f = Dataset(filename,'r')
    time = f.variables['time']
    timelength = len(time)
    u = f.variables['u']

    mean = u[0,:,:,n:n+128]
    
    for t in xrange(1,timelength):
        utemp=u[t,:,:,n:n+128]
        mean = ne.evaluate('(mean+utemp)/2')
    
    f.close()
    return mean

#@profile
def temp_calc(n_lat,n_lon,p_file,pt_file):
    start2 = timepack.time()
    # fake mean for memory test
    mean = np.zeros((180,768,1024))
    stage = timepack.time()-start2
    print 'fake mean made at %f' % stage

    f_pt = Dataset(pt_file,'r')
    pt = f_pt.variables['theta']
    f_p = Dataset(p_file,'r')
    p = f_p.variables['p']
    date = p_file[-13:-5]
    f = Dataset('/group_workspaces/jasmin/hiresgw/mj07/xjanpa.'+date+'.T.nc','a')
    appendtime = f.variables['time']
    appendT = f.variables['T']
    stage = timepack.time()-start2
    print 'opened all netcdf at %f' % stage

    print 'slice starting for %s' % p_file[-13:-5]
    
    for t in xrange(6):
        pt_slice = pt[t,:,:,:]
        p_slice = p[t,:,:,:]


        end2 = timepack.time()-start2
        print 'time taken for slice %d %f for %s' % (t,end2,p_file[-13:-5])
        
        #splitind = range(0,1024,128)
        #pool = Pool(processes=8)
        #TASKS = [(filename,n) for n in splitind]
        #meansection = [pool.apply_async(splitfilecalc, t) for t in TASKS]
            
        #mean = np.concatenate((meansection[0].get(),meansection[1].get(),\
                            #meansection[2].get(),meansection[3].get(),\
                            #meansection[4].get(),meansection[5].get(), \
                            #meansection[6].get(),meansection[7].get()), 2)

        temp = ne.evaluate('pt_slice*(1000/(p_slice/100))**-0.286') # p/100 conv to hPa
        stage = timepack.time()-start2
        print 'temp calc done at %f' % stage
        
        mean = ne.evaluate('(mean+temp)/2')
        stage = timepack.time()-start2
        print 'mean calc done at %f' % stage
        
        appendT[t:t+1,:,:,:] = temp[:]
        appendtime[t] = hourspassed(date,t)
        stage = timepack.time()-start2
        print 'saving done at %f' % stage
    stage = timepack.time()-start2
    print 'file done at %f' % stage

#@profile
def main():

    # get the file list
    #pt_files = glob('/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pb????????.theta.nc')
    #pt_files.sort()
    #p_files = glob('/group_workspaces/jasmin/hiresgw/mj07/xjanpa.ph????????.p.nc')
    #p_files.sort()
    #for i in xrange(len(p_files)-69):
    
    pt_file = '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pb19910301.theta.nc'#pt_files[i]
    p_file = '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.ph19910301.p.nc'#p_files[i]     
    
    date = p_file[-13:-5]
    path = '/group_workspaces/jasmin/hiresgw/mj07/'
    createfile(path+'xjanpa.'+date+'.T.nc')
    # send off calcs
    start1 = timepack.time()
    temp_calc(0,0,p_file,pt_file)
    #temp = ne.evaluate('pt_slice*(1000/(p_slice/100))**-0.286') # p/100 conv to hPa
    end1 = timepack.time()-start1
    print 'time taken : %f' % end1
        

main()
