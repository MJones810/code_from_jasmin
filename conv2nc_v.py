#!/usr/bin/env python2.7
import cdms2
from netCDF4 import Dataset 
from sys import argv
import numpy as np

def hourspassed(fieldfile,t):
    ''' Function to work out days passed since 1970-01-01 00:00:00.

    Asumes 360 day calendar.
    '''
    startyear = 1970
    startmonth = 01
    startday = 01
    year = int(fieldfile[-8:-4])
    month = int(fieldfile[-4:-2])
    day = int(fieldfile[-2:])

    yearspass = year-startyear     
    monthspass = month-startmonth
    #if month>=03: monthspass = month-startmonth
    #elif month==01: 
    #    monthspass = 10
    #elif month==02: 
    #    monthspass = 11
    #else: raise ValueError('Month count does not work')
    dayspass = day-startday
    
    hourspass = ((yearspass*360+monthspass*30)+dayspass) + t/24.
    print hourspass
    return hourspass


def createnetCDF(fieldfile):
    ''' Creates the netCDF file to then be opened in field2nc. 
    '''
    ncfile = '/group_workspaces/jasmin/hiresgw/mj07/'+fieldfile+'.v.nc'
    f = Dataset(ncfile,'w')

    zres = 180
    latres = 769
    lonres = 1024
    # Create dimensions
    time = f.createDimension('time',None)
    z_hybrid_height = f.createDimension('z_hybrid_height',zres)
    latitude = f.createDimension('latitude',latres)
    longitude = f.createDimension('longitude',lonres)
    bound = f.createDimension('bound',2)

    # Create variables (added s on the end to differentiate between dimensions
    #                   and variables)
    times = f.createVariable('time','f4',('time',),zlib=True)
    z_hybrid_heights = f.createVariable('z_hybrid_height','f4',
                                        ('z_hybrid_height',),zlib=True)
    latitudes = f.createVariable('latitude','f4',('latitude',),zlib=True)
    bounds_latitude = f.createVariable('bounds_latitude','f8',
                                       ('latitude','bound',),zlib=True)
    longitudes = f.createVariable('longitude','f4',('longitude',),zlib=True)
    bounds_longitude = f.createVariable('bounds_longitude','f8',
                                        ('longitude','bound',),zlib=True)
    v = f.createVariable('v','f4',('time','z_hybrid_height','latitude',
                                   'longitude',),zlib=True)

    # Add in attributes
    times.units = 'days since 1991-03-01 00:00:00'
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
    v.stash_item = 2
    v.stash_model = 1
    v.lookup_source = 'defaults (cdunifpp V0.13)'
    v.long_name = 'V COMPONENT OF WIND AFTER TIMESTEP'
    v.units = 'm s-1'
    v.stash_section = 0
    v.missing_value = -1.073742e+09

    # Add in values of lat, lon and height
    f2 = cdms2.open('/group_workspaces/jasmin/hiresgw/xjanp/'+fieldfile)
    var = f2.getVariables()

    if len(var)==4:
        v2 = var[3]
    elif len(var)==11:
        v2 = var[7]
    else: raise ValueError('lenght check doesnt work')

     # v cmpt of velocity
    z2 = f2.getVariables()[0]
    zvals = z2.domain[0][0][:]
    # Check the length of the latitude dimension
    if v2.shape[2] == 768:
        latvals = np.linspace(-90+90./768,90-90./768,768)
    elif v2.shape[2] == 769:
        latvals = np.linspace(-90,90,769)
    else: raise ValueError('Unhandled latitude dimension')

    # Check the length of the latitude dimension
    if v2.shape[3] == 1024 and v2.shape[2] == 768:
        lonvals = np.linspace(0,360-306./1024,1024)
    elif v2.shape[3] == 1024 and v2.shape[2] == 769:
        lonvals = np.linspace(360./(1024*2),360.-360./(1024*2),1024)
    else: raise ValueError('Unhandled longitude dimension')
    
    latitudes[:] = latvals[:]
    longitudes[:] = lonvals[:]
    z_hybrid_heights[:] = zvals[:]
    f2.close()

    f.close()

def field2nc(t,fieldfile):
    ''' Converts fileds file for variable at a specific time level to 
        an nc file.
    '''
    print '\nWrite started for ',t
    fielddir = '/group_workspaces/jasmin/hiresgw/xjanp/'
    f = cdms2.open(fielddir+fieldfile)
    var = f.getVariables()   
    if len(var)==4:
        v = var[3]
    elif len(var)==11:
        v = var[7]
    else: raise ValueError('lenght check doesnt work')
    print '\nVariables being saved', v.name_in_file
    
    ncfile = '/group_workspaces/jasmin/hiresgw/mj07/'+fieldfile+'.v.nc'
    f2 = Dataset(ncfile,'a')
    appendv = f2.variables['v']
    appendtime = f2.variables['time']    

    print ' shape of appendv : ',appendv.shape, ':: shape of v : ',v.shape

    appendv[t:t+1,:,:,:] = v[t:t+1,:,:,:]
    appendtime[t] = hourspassed(fieldfile,t)

    f.close()
    f2.close()
    print 'Write done for t = ',t,'\n'

def main():    
    # Get filename from shell argument
    test = False
    if test: 
        fieldfiletemp2 = '/group_workspaces/jasmin/hiresgw/xjanp/xjanpa.pi19910301'
    else:
        fieldfiletemp = argv[1:]
        fieldfiletemp2 = fieldfiletemp[0]
    
    fieldfile = fieldfiletemp2[39:]
    print fieldfile
    createnetCDF(fieldfile)
    for t in xrange(0,240):
        field2nc(t,fieldfile)

if __name__ == '__main__':
    main()
