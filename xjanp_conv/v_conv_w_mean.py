#!/usr/bin/env python2.7
''' Conversion of u from xjlef including the calculation of the monthly
    mean
'''

import cdms2
from netCDF4 import Dataset
import numpy as np
activate_this = '/home/users/mjones07/science/venv/bin/activate_this.py'
execfile(activate_this,dict(__file__=activate_this))
import numexpr as ne
from sys import argv

def hourspassed(fieldfile,t):
    ''' Function to work out hours passed since 1991-03-01 00:00:00.

    Asumes 360 day calendar.

    Needs changing depending on the model run - they have different 
    start dates.
    '''
    startyear = 1991
    startmonth = 3
    startday = 1
    year = int(fieldfile[-8:-4])
    month = int(fieldfile[-4:-2])
    day = int(fieldfile[-2:])

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
    latres = 769 ### 769 for v, 768 for u
    lonres = 1024 #**#
    # Create dimensions
    z_hybrid_height = f.createDimension('z_hybrid_height',zres)
    latitude = f.createDimension('latitude',latres)
    longitude = f.createDimension('longitude',lonres)

    v = f.createVariable('v','f4',('z_hybrid_height','latitude',
                                   'longitude',),zlib=True) #**#
    f.close()

def createfile(filename):
    ''' Creates the netCDF file to then be opened in field2nc. 

        Needs changing when extracting a different field #**# indicate 
        that there is something that needs changing. 
    '''
    print filename
    f = Dataset(filename,'w')

    zres = 180 #**#
    latres = 769 #**#
    lonres = 1024 #**#
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
    v = f.createVariable('v','f4',('time','z_hybrid_height','latitude',
                                   'longitude',),zlib=True) #**#

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
    #**#
    v.lookup_source = 'defaults (cdunifpp V0.13)'
    v.long_name = 'V COMPONENT OF WIND AFTER TIMESTEP'
    v.standard_name = 'northward_wind'
    v.units = 'm s-1'
    v.missing_value = -1.073742e+09
    #**#

    # Add in values of lat, lon and height
    fieldfile = 'xjanpa.pi'+filename[-13:-5] #**#
    f2 = cdms2.open('/group_workspaces/jasmin/hiresgw/xjanp/'+fieldfile)#**#
    var = f2.getVariables()
    if len(var)==4: #**#
        v2 = var[3]
    elif len(var)==11:
        v2 = var[7]

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
        lonvals = np.linspace(0,360-360./1024,1024)
    elif v2.shape[3] == 1024 and v2.shape[2] == 769:
        lonvals = np.linspace(360./(1024*2),360.-360./(1024*2),1024)
    else: raise ValueError('Unhandled longitude dimension')
    
    latitudes[:] = latvals[:]
    longitudes[:] = lonvals[:]
    z_hybrid_heights[:] = zvals[:]
    f2.close()

    f.close()

def var_save(dates):
    ''' Saves the field into netcdf format. Also calculates the mean 
        and saves every month.
        
        Needs changing when extracting a different field #**# indicate 
        that there is something that needs changing.
    '''
    
    # compile list of the 3 files for that month
    v_files = []
    for date in dates: 
        v_files.append('/group_workspaces/jasmin/hiresgw/xjanp/xjanpa.pi'\
                        +date) #**#
        
    ismean = False # checker to see if there is already a mean

    for i in xrange(len(v_files)):
        date = dates[i]
        # Read in the fields file
        f = cdms2.open(v_files[i])
        var = f.getVariables() 
        if len(var)==4: #**#
            v = var[3]
        elif len(var)==11:
            v = var[7]
        else: raise ValueError('lenght check doesnt work') 
                   #**# # (the same variable may not be in the same 
                        #  place in each of the fields files)

        f = Dataset('/group_workspaces/jasmin/hiresgw/mj07/xjanpa.'\
                    +date+'.v.nc','a') #**#                          
        appendtime = f.variables['time']
        appendT = f.variables['v'] #**#
    
        print 'Entering time loop for %s ' % date
        for t in xrange(2):
            v_slice = v[t,:,:,:]
            
            f = Dataset('/group_workspaces/jasmin/hiresgw/mj07/xjanpa.'\
                        +date+'.v.nc','a') #**#                              
            appendtime = f.variables['time']
            appendv = f.variables['v'] #**#

            # check if there is already a mean
            print 'Calculating mean'
            if ismean:
                mean = ne.evaluate('(mean+v_slice)/2')
            else:
                mean = v_slice[:]
                ismean = True
            print 'Saving variable'
            appendv[t:t+1] = v[t:t+1]
            appendtime[t] = hourspassed(date,t)
            # if end of last file save the mean
        if date[-2:] == '21':
            print 'Saving mean'
            meanfile = '/group_workspaces/jasmin/hiresgw/mj07/'+\
                'monthly_means/temp_files/xjanpa.'+str(date[:-2])+\
                '.v.nc' #**#                            
            fmean = Dataset(meanfile,'a')
            appendv_mean = fmean.variables['v']#**#
            appendv_mean[:] = mean[:]

def main():
    ''' Gets the pressure file from command line arg and works 
        everything out from there. Saves hourly and monthly data.
    '''
    test = True
    if test: 
        infile = '/group_workspaces/jasmin/hiresgw/mj07/xjanpa.pi19910301'
    else:
        infiletemp = argv[1:]
        infile = infiletemp[0]

    dates = [str(infile[-8:]),str(infile[-8:-2])+'11',str(infile[-8:-2])+'21']
    print 'dates being done\n',dates    
    path = '/group_workspaces/jasmin/hiresgw/mj07/'
    for date in dates:
        createfile(path+'xjanpa.'+date+'.v.nc')#**#
    path_mean = '/group_workspaces/jasmin/hiresgw/mj07/monthly_means/temp_files/'
    createfile_mean(path_mean+'xjanpa.'+str(infile[-8:-2])+'.v.nc')#**#
    # send off calcs
    var_save(dates)
        
main()
