#!/usr/bin/env python2.7

import netCDF4 as nc

def getfromfile(filename,name):
    ''' Return a field variable and it's dimension variables from a netcdf file 
	
	From Bryan's hiresgwBasicTools.py.
	'''
    d=nc.Dataset(filename,'r')
    if name in d.variables:
        v=d.variables[name]
        axes={}
        for dimension in v.dimensions:
            axes[dimension]=d.variables[dimension]
        return v,axes
    else:
        raise ValueError(
        'Variable <%s> not found in file <%s> which contains <%s>'%
        (name,filename,d.variables))

def zonalmean(var,axes):
    ''' Calculates the zonal mean of the variable using the information
        about the axes
        '''


if __name__ == '__main__':

    filename = 'xjanpa.pj19910301.pp.0to3.u.nc'
    varname = 'u'
    var,axes = getfromfile(filename,varname)
    print axes


