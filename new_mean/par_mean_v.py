#!/usr/bin/env python2.7
''' Calculate the monthly mean of v. '''
from glob import glob
import jug
import numpy as np
from multiprocessing import Pool
from netCDF4 import Dataset
activate_this = '/home/users/mjones07/science/venv/bin/activate_this.py'
execfile(activate_this,dict(__file__=activate_this))
import numexpr as ne

def monthspassed(filename):
    ''' Function to work out how many months have passed since the start 
        of the model.

        Assumes a 360 day calendar.
    '''
    startyear = 1991
    startmonth = 03
    year = int(filename[-16:-12])
    month = int(filename[-12:-10])
    monthpassed = month-startmonth
    yearspassed = year-startyear
    monthspassed = yearspassed*12+monthpassed
    return monthspassed

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
    v = f.createVariable('v','f4',('time','z_hybrid_height','latitude',
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
    v.stash_item = 2
    v.stash_model = 1
    v.lookup_source = 'defaults (cdunifpp V0.13)'
    v.standard_name = 'northward_wind'
    v.long_name = 'V COMPONENT OF WIND AFTER TIMESTEP'
    v.units = 'm s-1'
    v.stash_section = 0
    v.missing_value = -1.073742e+09

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
    
    # If .nc on end of filename assume from 'filepsplit'
    if filename[-3:] == '.nc' :
        tempdir = filename[:-22]+'monthly_means/temp_files/'
        tempfile = filename[-22:-5]+'.temp.v.nc'
    
    else : # Else from monthly average
        tempdir = filename[:-15]+'monthly_means/temp_files/'
        tempfile = filename[-15:]+'.temp.v.nc'
    

    f = Dataset(tempdir+tempfile,'w')    
    
    # Create dimensions
    z_hybrid_height = f.createDimension('z_hybrid_height',180)
    latitude = f.createDimension('latitude',768)
    longitude = f.createDimension('longitude',1024)
    bound = f.createDimension('bound',2)

    # Create u variable
    u = f.createVariable('v','f4',('z_hybrid_height','latitude',
                                   'longitude',),zlib=True)
    f.close()

def splitmonthcalc(fileblob,n):
    ''' Calculate the mean of the section to reduce to a single month,
        which starts at n and is 128 long.
    '''
    files = fileblob.split(',')
    del files[-1] # get rid off empty string at end
    f = Dataset(files[0],'r')
    u = f.variables['v']
    mean = u[:,:,n:n+128]
    f.close()
    for filename in files[1:]:
        f = Dataset(filename,'r')
        u = f.variables['v']
        utemp = u[:,:,n:n+128]
        mean = ne.evaluate('(mean+utemp)/2')
        f.close()
    return mean

def splitfilecalc(filename,n):
    ''' Calculate the mean of the section for individual files , which 
        starts at n and is 40 long.
    '''
    
    f = Dataset(filename,'r')
    time = f.variables['time']
    timelength = len(time)
    u = f.variables['v']

    mean = u[0,:,:,n:n+128]
    
    for t in xrange(1,timelength):
        utemp=u[t,:,:,n:n+128]
        mean = ne.evaluate('(mean+utemp)/2')
    
    f.close()
    return mean

@jug.TaskGenerator
def finalreduce(debug=False):
    ''' Saves all the monthly averages into a single NetCDF
        file.

        Creates a file to save into.
    '''
    # get list of monthly means
    directory = '/group_workspaces/jasmin/hiresgw/mj07/'
    months = glob(directory+'monthly_means/temp_files/xjanpa.pj??????.temp.v.nc')
    months.sort()
    # Example file to take lat, lon and height vals from
    filename = directory+'xjanpa.pj19910301.v.nc'
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
    
    print 'Finished!'
@jug.TaskGenerator
def monreduce(filein):
    ''' Averages the files down to a month.
        
        Creates a new temporary file per month.
    '''
    directory = '/group_workspaces/jasmin/hiresgw/mj07/monthly_means/'
    month = filein[:-7]
    create_temp_nc(month)
    # Get the 3 files for each month
    files = glob(directory+'temp_files/'+filein[-22:-7]+'??.temp.v.nc')
    fileblob = ''
    for filename in files:
        fileblob+=filename+','
    splitind = range(0,1024,128)
    pool = Pool(processes=8)
    TASKS = [(fileblob,n) for n in splitind]
    meansection = [pool.apply_async(splitmonthcalc, t) for t in TASKS]
    mean = np.concatenate((meansection[0].get(),meansection[1].get(),\
                        meansection[2].get(),meansection[3].get(),\
                        meansection[4].get(),meansection[5].get(), \
                        meansection[6].get(),meansection[7].get()), 2)
    print 'done for %s' % (month)    
    # Save mean in file
    filename = directory+'temp_files/'+filein[-22:-7]+'.temp.v.nc'
    f = Dataset(filename,'a')
    u = f.variables['v']
    u[:] = mean[:]
    
    f.close()

@jug.TaskGenerator
def filesplit(filename):
    ''' Takes the individual files and splits them to calculate sections 
        of the mean, brings them back together then saves.
    '''
    create_temp_nc(filename)
    
    splitind = range(0,1024,128)
    pool = Pool(processes=8)
    TASKS = [(filename,n) for n in splitind]
    meansection = [pool.apply_async(splitfilecalc, t) for t in TASKS]
        
    mean = np.concatenate((meansection[0].get(),meansection[1].get(),\
                        meansection[2].get(),meansection[3].get(),\
                        meansection[4].get(),meansection[5].get(), \
                        meansection[6].get(),meansection[7].get()), 2)
    print 'done for %s' % (filename)
    tempdir = filename[:-22]+'monthly_means/temp_files/'
    tempfile = filename[-22:-5]+'.temp.v.nc'
    f = Dataset(tempdir+tempfile,'a')
    u = f.variables['v']
    u[:] = mean[:]
    f.close()


#------------#
debug=False   #
#------------#

if debug:
    filenames = ['/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj19910301.u.nc',\
                 '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj19910311.u.nc',\
                 '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj19910321.u.nc',\
                 '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj19910401.u.nc',\
                 '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj19910411.u.nc',\
                 '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj19910421.u.nc']
        
else: #glob bit
    filenames = glob('/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pi*')
    filenames.sort()
        
map(filesplit,filenames)
jug.barrier()    

if debug:
    filenames = ['/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj19910301.u.nc',\
                 '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj19910401.u.nc']
        
else: #glob month bit
    filenames = glob('/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pi??????01.v.nc')
    filenames.sort()
        
map(monreduce,filenames)
jug.barrier()
map(finalreduce,[False])

