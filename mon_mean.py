#!/usr/bin/env python2.7
''' Calculates the monthly mean one timestep at a time in serial '''

from netCDF4 import Dataset
import numpy as np

def file_avg(mean,filename):
    ''' Averages the current netCDF file, 'filename', and returns 
        the result.
    '''
    
    f = Dataset(filename,'r')
    time = f.variables['time']
    timelength = len(time)
    u = f.variables['u']
    
    for t in xrange(12):
        print t
        mean = (mean+u[t,:,:,:])/2
    
    f.close()
    print mean.shape
    return mean

def main():
    
    direct = '/group_workspaces/jasmin/hiresgw/mj07/'
    files = ['xjanpa.pj19910301.u.nc']
    f = Dataset(direct+files[0],'r')
    z = f.variables['z_hybrid_height']
    lat = f.variables['latitude']
    lon = f.variables['longitude']
    mean = np.zeros([len(z),len(lat),len(lon)])

    for filename in files:
        mean += file_avg(mean,direct+filename)

if __name__ == '__main__':
    import time
    starttime = time.time()
    main()
    print 'Run time: ',time.time()-starttime
