#!/usr/bin/env python2.7
''' Same as par_mon_mean.py but splits the initial average between 
    tasks to try and increase speed.
'''
import numpy as np
from glob import glob
from netCDF4 import Dataset
import jug

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
    filename = filein[-22:-16]+'.monthlymean.usingsplit.u.nc'
    f = Dataset(filedir+filename,'w')

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
                                   'longitude',),zlib=True)
    
    # Add in attributes
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
    u.long_name = 'U COMPONENT OF WIND AFTER TIMESTEP'
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
    ''' Creates a temporary NetCDF file to store u between
        tasks.
    '''
    
    f = Dataset(filename,'w')    
    
    # Create dimensions
    z_hybrid_height = f.createDimension('z_hybrid_height',180)
    latitude = f.createDimension('latitude',768)
    longitude = f.createDimension('longitude',1024)
    bound = f.createDimension('bound',2)

    # Create u variable
    u = f.createVariable('u','f4',('z_hybrid_height','latitude',
                                   'longitude',),zlib=True)
    f.close()

def avg_mult_files(files,directory,tempfile):
    f = Dataset(files[0],'r')
    u = f.variables['u']
    mean = u[:]
    f.close()
    
    for filename in files[1:]:
        f = Dataset(filename,'r')
        u = f.variables['u']
        mean = (mean+u[:])/2
        f.close()

    # Save mean in file
    f = Dataset(directory+tempfile+'.nc','a')
    u = f.variables['u']
    u[:] = mean[:]
    
    f.close()

def file_avg(mean,filename,index_range):
    ''' Averages the current netCDF file, 'filename', and returns 
        the result.
    '''
    favg = Dataset(filename,'r')
    time = favg.variables['time']
    timelength = len(time)
    u = favg.variables['u']

    mean = u[index_range[0],:,:,:]
    
    for t in xrange(index_range[0]+1,index_range[1]):
        
        mean = (mean+u[t,:,:,:])/2
    
    favg.close()
    return mean

def take_avg(filename,index_range):
    ''' Takes the average of the file within the time index range given.
        Then saves to a netCDF file.
        
        Input file format 
        /group_workspaces/jasmin/hiresgw/mj07/xjanpa.*
    '''
    f = Dataset(filename,'r')
    z = f.variables['z_hybrid_height']
    lat = f.variables['latitude']
    lon = f.variables['longitude']
    # Initialize the mean with the size from the file
    mean = np.zeros([len(z),len(lat),len(lon)])
    f.close()
    mean = file_avg(mean,filename,index_range)

    tempdir = filename[:-22]+'monthly_means/temp_files_test/'
    tempfile = (filename[-22:-5]+'.temp.'+str(index_range[0])+
               '-'+str(index_range[1])+'.nc')
    create_temp_nc(tempdir+tempfile)
    f2 = Dataset(tempdir+tempfile,'a')
    u = f2.variables['u']
    u[:] = mean[:]
    f2.close()

#########################
#------ Jug tasks ------#
#########################

@jug.TaskGenerator
def final_average(n):
    ''' Saves all the monthly averages into a single NetCDF
        file.

        Creates a file to save into.
    '''
    # get list of monthly means
    directory = '/group_workspaces/jasmin/hiresgw/mj07/'
    months = glob(directory+'monthly_means/temp_files_test/xjanpa.pj??????.nc')
    months.sort()
    # Example file to take lat, lon and height vals from
    filename = directory+'xjanpa.pj19910301.u.nc'
    # Create netCDF file to save data to
    print '\nCreating final netcdf file using : ', filename
    create_nc(filename)
    createdfile = directory+'monthly_means/xjanpa.monthlymean.usingsplit.u.nc'

    ffin = Dataset(createdfile,'a')
    u = ffin.variables['u']
    t = ffin.variables['time']

    for i,monthfile in enumerate(months) :
        ffin2 = Dataset(monthfile,'r')
        uappend = ffin2.variables['u']
        u[i,:,:,:] = uappend[:]
        # Work out months passed since start of model run
        tappend = monthspassed(monthfile)
        t[i] = tappend
        ffin2.close()

    ffin.close()

    return 0

@jug.TaskGenerator
def avg_to_month(filein):
    ''' Averages down so there is only one file per month.
    
        Input file format
        /group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj??????01.u.nc
    '''

    directory = '/group_workspaces/jasmin/hiresgw/mj07/' + \
            'monthly_means/temp_files_test/'
    # Filename
    tempfile = filein[38:53]
    create_temp_nc(directory+tempfile+'.nc')

    # Get files to average
    files = glob(directory+tempfile+'??.nc')
    files.sort()

    avg_mult_files(files,directory,tempfile)

@jug.TaskGenerator
def avg_to_3permonth(filein) :
    ''' Averages down so there are only 3 netcdf files per month.

        Input file format 
        /group_workspaces/jasmin/hiresgw/mj07/
            monthly_means/temp_files_test/xjanpa.pj????????.temp.0-48.nc
    '''

    directory = '/group_workspaces/jasmin/hiresgw/mj07/' + \
            'monthly_means/temp_files_test/'
    # Filename
    tempfile = filein[68:85]
    create_temp_nc(directory+tempfile+'.nc')

    # Get files to average
    files = glob(directory+tempfile+'.*.nc')
    files.sort()

    avg_mult_files(files,directory,tempfile)
    
@jug.TaskGenerator
def avg_fifth_fifth(filename):
    ''' Takes an average of the fourth quarter of the file and saves 
        the result.
    '''
    index_range = [192,240]
    take_avg(filename,index_range)

@jug.TaskGenerator
def avg_fourth_fifth(filename):
    ''' Takes an average of the fourth quarter of the file and saves 
        the result.
    '''
    index_range = [144,192]
    take_avg(filename,index_range)

@jug.TaskGenerator
def avg_third_fifth(filename):
    ''' Takes an average of the third quarter of the file and saves 
        the result.
    '''
    index_range = [96,144]
    take_avg(filename,index_range)

@jug.TaskGenerator
def avg_second_fifth(filename):
    ''' Takes an average of the second quarter of the file and saves 
        the result.
    '''
    index_range = [48,96]    
    take_avg(filename,index_range)

@jug.TaskGenerator
def avg_first_fifth(filename):
    ''' Takes an average of the first quarter of the file and saves 
        the result.
    '''
    index_range = [0,48]
    take_avg(filename,index_range)



# Get lists of the files and months to average
files = glob('/group_workspaces/jasmin/hiresgw/mj07/xjanpa.*')
files.sort()
rank2_files = glob('/group_workspaces/jasmin/hiresgw/mj07/'+
            'monthly_means/temp_files_test/xjanpa.pj????????.temp.0-48.nc')
rank2_files.sort()
months = glob('/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj??????01.u.nc')
months.sort()

# First reduce the number of timesteps on each file by
# averaging them.
map(avg_first_fifth,files) #36 tasks
map(avg_second_fifth,files) #36 tasks
map(avg_third_fifth,files) #36 tas
map(avg_fourth_fifth,files) #36 tasks
map(avg_fifth_fifth,files) #36 tasks
jug.barrier()
# Next average down so that there are only 3 files per month
map(avg_to_3permonth,rank2_files) #36 tasks
jug.barrier()
# Next average down to one file per month
map(avg_to_month,months) #12 tasks
jug.barrier()
# Finally reduce all months to a single file containg 
# all the averages
n = [1]
map(final_average,n) #1 task
