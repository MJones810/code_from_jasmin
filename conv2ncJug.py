#!/usr/bin/env python2.7
''' Assumes that nc file is already created.
'''

import jug
import cdms2
from netCDF4 import Dataset
import time 

@jug.TaskGenerator
def pp2nc(t):
    ''' Converts pp file for u_1 variable at a specific time level to 
        an nc file.
    '''
    timestart = time.time()
    
    print '\nWrite started for ',t
    ppdir = '/group_workspaces/jasmin/hiresgw/xjanp/pp/'
    ppfile = 'xjanpa.pj19910301'
    f = cdms2.open(ppdir+ppfile+'.pp')
    
    
    vars = f.getVariables()
    u = vars[9]
    print 'Variable being saved', u
    ncfile = '/home/users/mjones07/science/'+ppfile+'.u.nc'
    #while True:
	#	try:
    f2 = Dataset(ncfile,'a')
	#	except: 
	#		continue
	#	break
    appendu = f2.variables['u']
    print 'Writing ', ncfile
    #while True:
	#	try: 
    appendu[t:t+1] = u[t:t+1,:,:,:]
	#	except: 
	#		if timestart-time.time() < 300
	#			continue
	#		else: 
	#			print 'timed out in asignment loop'
	#			break
	#	break
    print 'Write done for t = ',t,'\n'
    f.close()
    f2.close()
     
    return 0




m = map(pp2nc,xrange(0,10))
