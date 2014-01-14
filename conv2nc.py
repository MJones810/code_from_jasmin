#!/usr/bin/env python2.7
import cdms2
import time
from netCDF4 import Dataset

def pp2nc(ppdir,ppfile,t,t1):
    ''' Converts pp file for u_1 variable at a specific time level to 
        an nc file.
    '''
    f = cdms2.open(ppdir+ppfile+'.pp')
    vars = f.getVariables()
    u = vars[9]
    print 'Variable being saved', u
    ncfile = ppfile+'.u.nc'
    f2 = Dataset(ncfile,'a')
    appendu = f2.variables['u']
    print 'Writing ', ncfile
    appendu[t:t1] = u[t:t1,:,:,:]
    print appendu
    f.close()
    f2.close()
	
def createnetCDF(ppfile):
    ''' Creates the netCDF file to then be opened in pp2nc. 
    '''
    ncfile = ppfile+'.u.nc'
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
    times.units = 'days since 1970-01-01 00:00:00'
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

    f.close()


if __name__ == '__main__':
	ppdir = '/group_workspaces/jasmin/hiresgw/xjanp/pp/'
	ppfile = 'xjanpa.pj19910301'
	timelevelmin = 6
	timelevelmax = 10 
        createnetCDF(ppfile)
	pp2nc(ppdir,ppfile,timelevelmin,timelevelmax)


