#!/usr/bin/env python2.7
import cdms2
from netCDF4 import Dataset 
from sys import argv

def hourspassed(ppfile,t):
    ''' Function to work out hours passed since start o=f the model.

    Asumes 360 day calendar.
    '''
    
    startyear = 1991
    startmonth = 03
    startday = 01
    year = int(ppfile[-8:-4])
    month = int(ppfile[-4:-2])
    day = int(ppfile[-2:])

    yearspass = year-startyear     
    if month>=03: monthspass = month-startmonth
    elif month==01: 
        monthspass = 10
    elif month==02: 
        monthspass = 11
    dayspass = day-startday
    
    hourspass = ((yearspass*360+monthspass*30)+dayspass)*24 + t

    return hourspass

def createnetCDF(ppfile):
    ''' Creates the netCDF file to then be opened in pp2nc. 
    '''
    print '\n\n',ppfile, '\n\n\n'
    ncfile = '/group_workspaces/jasmin/hiresgw/mj07/'+ppfile+'.u.nc'
    f = Dataset(ncfile,'w')

    # Create dimensions
    time = f.createDimension('time',None)
    z_hybrid_height = f.createDimension('z_hybrid_height',180)
    latitude = f.createDimension('latitude',768)
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
    u = f.createVariable('u','f4',('time','z_hybrid_height','latitude',
                                   'longitude',))
    
    # Add in attributes
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
    u.stash_item = 2
    u.stash_model = 1
    u.lookup_source = 'defaults (cdunifpp V0.13)'
    u.long_name = 'U COMPONENT OF WIND AFTER TIMESTEP'
    u.units = 'm s-1'
    u.stash_section = 0
    u.missing_value = -1.073742e+09
    
    # need to add in a bit that saves the values of time, lat and lon
    ppdir = '/group_workspaces/jasmin/hiresgw/xjanp/pp/'
    f2 = Dataset('/home/users/mjones07/science/xjanpa.19920111.uutest1.nc')
    
    lat = f2.variables['latitude0']
    lon = f2.variables['longitude0']
    height = f2.variables['z0_hybrid_height']

    latitudes[:] = lat[:]
    longitudes[:] = lon[:]
    z_hybrid_heights[:] = height[:]

    

	
    f.close()

def pp2nc(t,ppfile):
    ''' Converts pp file for u_1 variable at a specific time level to 
        an nc file.
    '''

    print '\nWrite started for ',t
    ppdir = '/group_workspaces/jasmin/hiresgw/xjanp/pp/'
    f = cdms2.open(ppdir+ppfile+'.pp')
    vars = f.getVariables()   
    u = vars[9]

    print 'Variables being saved', u

    ncfile = '/group_workspaces/jasmin/hiresgw/mj07/'+ppfile+'.u.nc'
    f2 = Dataset(ncfile,'a')
    appendu = f2.variables['u']
    appendtime = f2.variables['time']

    print 'Writing ', ncfile
    appendu[t:t+1] = u[t:t+1,:,:,:]
    appendtime[t:t+1] = hourspassed(ppfile,t)

    f.close()
    f2.close()
    print 'Write done for t = ',t,'\n'



def main():    
    ppdir = '/group_workspaces/jasmin/hiresgw/xjanp/pp/'
    # Get filename from shell argument
    ppfiletemp = argv[1:]
    ppfiletemp2 = ppfiletemp[0]
    ppfile = ppfiletemp2[42:-3]
    print ppfile
    createnetCDF(ppfile)
    for t in xrange(0,240):
        print t
        pp2nc(t,ppfile)

if __name__ == '__main__':
    main()
