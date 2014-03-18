#!/usr/bin/env python2.7
import numpy as np
from glob import glob
from netCDF4 import Dataset
import jug
activate_this = '/home/users/mjones07/science/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import numexpr as ne

def monthspassed(filename):
    ''' Function to work out months passed since start of the model.

    Asumes 360 day calendar.
    '''    
    startyear = 1991
    startmonth = 03
    year = int(filename[-14:-10])
    month = int(filename[-10:-8])
    yearspass = year-startyear     

    if month>=03: monthspass = month-startmonth
    elif month==01: 
        monthspass = -2
    elif month==02: 
        monthspass = -1
    
    monthspass = yearspass*12+monthspass
    return monthspass

def create_nc(filein):
    ''' Creates the NetCDF file to save the final averages
        in.
    '''
    filedir = filein[:-22]+'monthly_means/'
    filename = filein[-22:-16]+'.monthlymean.v.nc'
    f = Dataset(filedir+filename,'w')

    # Create dimensions
    time = f.createDimension('time',None)
    z_hybrid_height = f.createDimension('z_hybrid_height',180)
    latitude = f.createDimension('latitude',769)
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
    u = f.createVariable('v','f4',('time','z_hybrid_height','latitude',
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
    u.stash_item = 2
    u.stash_model = 1
    u.lookup_source = 'defaults (cdunifpp V0.13)'
    u.long_name = 'V COMPONENT OF WIND AFTER TIMESTEP'
    u.standard_name = 'nortward_wind'
    u.units = 'm s-1'
    u.stash_section = 0
    u.missing_value = -1.073742e+09

    # need to add in a bit that saves the values of time, lat and lon
    f2 = Dataset(filein)
    
    lat = f2.variables['latitude']
    lon = f2.variables['longitude']
    height = f2.variables['z_hybrid_height']

    latitudes[:] = lat[:]
    longitudes[:] = lon[:]
    z_hybrid_heights[:] = height[:]

    f.close()
    f2.close()

def create_temp_nc(filename):
    ''' Creates a temporary NetCDF file to store v between
        tasks.
    '''
    # If .nc on end of filename assume from 'average_files'
    if filename[-3:] == '.nc' :
        tempdir = filename[:-22]+'monthly_means/temp_files/'
        tempfile = filename[-22:-5]+'.temp.nc'
    
    else : # Else from monthly average
        tempdir = filename[:-15]+'monthly_means/temp_files/'
        tempfile = filename[-15:]+'.temp.nc'

    f = Dataset(tempdir+tempfile,'w')    
    
    # Create dimensions
    z_hybrid_height = f.createDimension('z_hybrid_height',180)
    latitude = f.createDimension('latitude',769)
    longitude = f.createDimension('longitude',1024)
    bound = f.createDimension('bound',2)

    # Create u variable
    u = f.createVariable('v','f4',('z_hybrid_height','latitude',
                                   'longitude',),zlib=True)
    f.close()

def file_avg(mean,filename):
    ''' Averages the current netCDF file, 'filename', and returns 
        the result.
    '''
    favg = Dataset(filename,'r')
    time = favg.variables['time']
    timelength = len(time)
    u = favg.variables['v']

    mean = u[0,:,:,:]
    
    for t in xrange(1,timelength):
        
        mean = (mean+u[t,:,:,:])/2
    
    favg.close()
    return mean

@jug.TaskGenerator
def final_average(n):
    ''' Saves all the monthly averages into a single NetCDF
        file.

        Creates a file to save into.
    '''
    # get list of monthly means
    directory = '/group_workspaces/jasmin/hiresgw/mj07/'
    months = glob(directory+'monthly_means/temp_files/xjanpa.pi??????.temp.nc')
    months.sort()
    # Example file to take lat, lon and height vals from
    filename = directory+'xjanpa.pi19910301.v.nc'
    # Create netCDF file to save data to
    print '\nCreating final netcdf file using : ', filename
    create_nc(filename)
    createdfile = directory+'monthly_means/xjanpa.monthlymean.v.nc'

    ffin = Dataset(createdfile,'a')
    u = ffin.variables['v']
    t = ffin.variables['time']

    for i,monthfile in enumerate(months) :
        ffin2 = Dataset(monthfile,'r')
        uappend = ffin2.variables['v']
        u[i,:,:,:] = uappend[:]
        # Work out months passed since start of model run
        tappend = monthspassed(monthfile)
        t[i] = tappend
        ffin2.close()

    ffin.close()

    return 0
        

    

@jug.TaskGenerator
def average_to_month(filein):
    ''' Averages the files down to a month.
        
        Creates a new temporary file per month.
    '''
    directory = '/group_workspaces/jasmin/hiresgw/mj07/monthly_means/'
    month = filein[:-7]
    print '\nCreating temp netcdf for month using : ', month
    create_temp_nc(month)
    # Get the 3 files for each month
    files = glob(directory+'temp_files/'+filein[-22:-7]+'??.temp.nc')
    fmon = Dataset(files[0],'r')
    u = fmon.variables['v']
    mean = u[:]
    fmon.close()
    
    for filename in files[1:]:
        fmon2 = Dataset(filename,'r')
        u = fmon2.variables['v']
        mean = (mean+u[:])/2
        fmon2.close()

    # Save mean in file
    filename = directory+'temp_files/'+filein[-22:-7]+'.temp.nc'
    fmon3 = Dataset(filename,'a')
    u = fmon3.variables['v']
    u[:] = mean[:]
    
    fmon3.close()

    return 0
        
 
@jug.TaskGenerator
def average_files(filename):
    ''' Averages each file down to 6 timesteps per file.
    
        Creates a new temporary file per originl file.
    '''
    
    f = Dataset(filename,'r')
    z = f.variables['z_hybrid_height']
    lat = f.variables['latitude']
    lon = f.variables['longitude']
    # Initialize the mean with the size from the file
    mean = np.zeros([len(z),len(lat),len(lon)])
    f.close()
    mean = file_avg(mean,filename)
    
    tempdir = filename[:-22]+'monthly_means/temp_files/'
    tempfile = filename[-22:-5]+'.temp.nc'
    create_temp_nc(filename)
    f2 = Dataset(tempdir+tempfile,'a')
    u = f2.variables['v']
    'v.shape : ',u.shape,'\nSaving v'
    u[:] = mean[:]
    f2.close()

    return 0

# Get lists of the files and months to average
files = glob('/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pi*')
files.sort()
months = glob('/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pi??????01.v.nc')
months.sort()

# First reduce the number of timesteps on each file by
# averaging them.
map(average_files,files) #36 tasks
jug.barrier()
# Next reduce each month to one file by avergaing them
map(average_to_month,months) #12 tasks
jug.barrier()
# Finally reduce all months to a single file containg 
# all the averages
n = [1]
map(final_average,n) #1 task
