#!/usr/bin/env python2.7
''' merges the mean files together fot u and saves them into a single
'''

from netCDF4 import Dataset
from glob import glob

def monthspassed(filename):
    ''' Function to work out months passed since start of the model.

    Asumes 360 day calendar.
    '''    
    startyear = 1991
    startmonth = 3
    year = int(filename[-15:-11])
    month = int(filename[-11:-9])
    yearspass = year-startyear     

    if month>=03: monthspass = month-startmonth
    elif month==01: 
        monthspass = -2
    elif month==02: 
        monthspass = -1
    
    monthspass = yearspass*12+monthspass
    return monthspass

def create_nc(var):
    ''' Creates the NetCDF file to save the final averages
        in.
    '''
    filedir = '/group_workspaces/jasmin/hiresgw/mj07/monthly_means/'
    filename = 'xjanpa.monthlymean.'+var+'.nc' #**#
    f = Dataset(filedir+filename,'w')

    # Create dimensions
    time = f.createDimension('time',None)
    z_hybrid_height = f.createDimension('z_hybrid_height',180)
    latitude = f.createDimension('latitude',768)#**#
    longitude = f.createDimension('longitude',1024)
    bound = f.createDimension('bound',2)

    # Create variables (added s on the end to differentiate between dimensions
    #                   and variables)
    times = f.createVariable('time','f4',('time',))
    z_hybrid_heights = f.createVariable('z_hybrid_height','f4',
                                        ('z_hybrid_height',))
    latitudes = f.createVariable('latitude','f4',('latitude',))
    bounds_latitude = f.createVariable('bounds_latitude','f8',
                                       ('latitude','bound',))
    longitudes = f.createVariable('longitude','f4',('longitude',))
    bounds_longitude = f.createVariable('bounds_longitude','f8',
                                        ('longitude','bound',))
    v = f.createVariable(var,'f4',('time','z_hybrid_height','latitude',
                                   'longitude',),zlib=True)
    
    # Add in attributes
    f.Conventions = 'CF-1.6'
    times.units = 'months since 1991-03-01 00:00:00'
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
    #**#
    v.long_name = 'THETA'
    v.standard_name = 'air_potential_temperature'
    v.units = 'K'
    v.missing_value = -1.073742e+09
    #**#

    # need to add in a bit that saves the values of time, lat and lon
    f2 = Dataset('/group_workspaces/jasmin/hiresgw/mj07/xjanpa.19910301.'+var+'.nc') #**#
    
    lat = f2.variables['latitude']
    lon = f2.variables['longitude']
    height = f2.variables['z_hybrid_height']

    latitudes[:] = lat[:]
    longitudes[:] = lon[:]
    z_hybrid_heights[:] = height[:]

    f.close()
    f2.close()

def main():
    var = 'theta'
    path = '/group_workspaces/jasmin/hiresgw/mj07/monthly_means/temp_files/'
    files = glob(path+'xjanpa.??????.'+var+'.nc')
    files.sort()

    create_nc(var) 
    fmon = Dataset('/group_workspaces/jasmin/hiresgw/mj07/monthly_means/xjanpa.monthlymean.'+var+'.nc','a')
    vappend = fmon.variables[var]
    tappend = fmon.variables['time']
    for i,file in enumerate(files):
        print i,file
        f = Dataset(file,'r')
        v = f.variables[var]
        tappend[i] = monthspassed(file)
        vappend[i,:,:,:] = v[:]
        f.close()
    fmon.close()

main()
