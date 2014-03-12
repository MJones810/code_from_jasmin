#!/usr/bin/env python2.7
import cdms2
from glob import glob

path = '/group_workspaces/jasmin/hiresgw/xjlef/'
filenames = glob(path+'xjlefa.pj19810901')
filenames.sort()

for filename in filenames:
    f=cdms2.open(filename)
    var=f.getVariables()
    #print '\n'
    for i in xrange(len(var)):
        print i,'  :  ',var[i].name_in_file,var[i].shape
    #print var[9].name_in_file
    f.close()
