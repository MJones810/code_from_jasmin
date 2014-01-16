#!/usr/bin/env python2.7
''' Assumes that nc file is already created.
'''

import jug
import cdms2
from netCDF4 import Dataset

@jug.TaskGenerator
def pp2nc(t):
    ''' Converts pp file for u_1 variable at a specific time level to 
        an nc file.
    '''
    
    print '\nWrite started for ',t
    ppdir = '/group_workspaces/jasmin/hiresgw/xjanp/pp/'
    ppfile = 'xjanpa.pj19910301'
    f = cdms2.open(ppdir+ppfile+'.pp')    
    vars = f.getVariables()
    
    u = vars[9]
    print 'Variable being saved', u

    # saved timestep in nc file
    timeSave = f2.variables['time']
    timeSave[t] = t

	
    appendu = f2.variables['u']
    print 'Writing ', ncfile

    #try:
    appendu[t:t+1] = u[t:t+1,:,:,:]
    #except: 
    #    RuntimeError
    #    print 'RUNTIMEERROR: did not write'

    print 'Write done for t = ',t,'\n'
    f.close()
     
    return 0


ppfile = 'xjanpa.pj19910301'
ncfile = '/home/users/mjones07/science/'+ppfile+'.u.nc'
f2 = Dataset(ncfile,'a')

jug.barrier()

m = map(pp2nc,xrange(0,10))

jug.barrier()

f2.close()
