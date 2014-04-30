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
from sys import argv

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

def createfile_mean(filename):
    ''' Creates the temp netCDF file to save montly mean in.
    '''
    
    f = Dataset(filename,'w')

    zres = 180
    latres = 768
    lonres = 1024
    # Create dimensions
    z_hybrid_height = f.createDimension('z_hybrid_height',zres)
    latitude = f.createDimension('latitude',latres)
    longitude = f.createDimension('longitude',lonres)

    v = f.createVariable('T','f4',('z_hybrid_height','latitude',
                                   'longitude',),zlib=True)
    f.close()

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
    coordsfile = '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.19910301.theta.nc'
    f2 = Dataset(coordsfile,'r')
    latvals = f2.variables['latitude']
    lonvals = f2.variables['longitude']
    zvals = f2.variables['z_hybrid_height']
    
    latitudes[:] = latvals[:]
    longitudes[:] = lonvals[:]
    z_hybrid_heights[:] = zvals[:]
    f2.close()

    f.close()

def temp_calc(dates):
    ''' Calculates the temperature at each timesteps and saves. Also 
        calculates the mean and saves every month.
    '''
    
    pt_files = []
    p_files = []
    for date in dates:
        pt_files.append('/group_workspaces/jasmin/hiresgw/mj07/xjanpa.'\
                        +date+'.theta.nc')
        p_files.append('/group_workspaces/jasmin/hiresgw/mj07/xjanpa.'\
                        +date+'.p.nc' )
    
    start2 = timepack.time()
    stage = timepack.time()-start2
    print 'loop started at %f' % stage
    
    ismean = False # checker to see if there is already a mean

    for i in xrange(len(pt_files)):
        date = dates[i]
        f_pt = Dataset(pt_files[i],'r')
        pt = f_pt.variables['theta']
        f_p = Dataset(p_files[i],'r')
        p = f_p.variables['p']
        date = p_files[i][-13:-5]
        f = Dataset('/group_workspaces/jasmin/hiresgw/mj07/xjanpa.'+date+'.T.nc','a')
        appendtime = f.variables['time']
        appendT = f.variables['T']
        stage = timepack.time()-start2

        for t in xrange(240):
            pt_slice = pt[t,:,:,:]
            p_slice = p[t,:,:,:]
            end2 = timepack.time()-start2
                        
            temp = ne.evaluate('pt_slice*(1000/(p_slice/100))**-0.286') # p/100 conv to hPa
            stage = timepack.time()-start2
                        
            # check if there is already a mean, if not have i as the first of T
            if ismean:
                mean = ne.evaluate('(mean+temp)/2')
            else:
                mean = temp[:]
                ismean = True
            stage = timepack.time()-start2
                  
            appendT[t:t+1,:,:,:] = temp[:]
            appendtime[t] = hourspassed(date,t)
            stage = timepack.time()-start2
            # if end of last file save the mean
        if date[-2:] == '21':
            meanfile = '/group_workspaces/jasmin/hiresgw/mj07/monthly_means/temp_files/xjanpa.'+str(date[:-2])+'.T.nc'
            fmean = Dataset(meanfile,'a')
            appendT = fmean.variables['T']
            appendT[:] = mean[:]
    stage = timepack.time()-start2
    
    
def main():
    ''' Gets the pressure file from command line arg and works 
        everything out from there. Saves hourly and monthly data.
    '''
    test = False
    if test: 
        infile = '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.19910301.p.nc'
    else:
        infiletemp = argv[1:]
        infile = infiletemp[0]

    dates = [str(infile[-13:-5]),str(infile[-13:-7])+'11',str(infile[-13:-7])+'21']
    print 'dates being done\n',dates    
    path = '/group_workspaces/jasmin/hiresgw/mj07/'
    for date in dates:
        createfile(path+'xjanpa.'+date+'.T.nc')
    path_mean = '/group_workspaces/jasmin/hiresgw/mj07/monthly_means/temp_files/'
    createfile_mean(path_mean+'xjanpa.'+str(infile[-13:-7])+'.T.nc')
    # send off calcs
    start1 = timepack.time()
    temp_calc(dates)
    end1 = timepack.time()-start1
    print 'time taken : %f' % end1
        
main()
