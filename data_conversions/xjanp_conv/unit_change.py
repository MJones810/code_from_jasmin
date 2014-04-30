#!/usr/bin/env python2.7
''' code to change the units of time for u '''

from glob import glob
from netCDF4 import Dataset

files = glob('/group_workspaces/jasmin/hiresgw/mj07/monthly_means/xjanpa.*.nc')
print 'number of files', len(files)

for filename in files:
    f = Dataset(filename,'a')
    print filename
    time = f.variables['time']
    print time.units
    time.units = 'hours since 1991-03-01 00:00:00'
    print time.units

