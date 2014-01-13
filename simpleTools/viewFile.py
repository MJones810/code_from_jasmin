#!/usr/bin/env python2.7
# simple tool to produce a json view of the contents of a pp or netcdf file.
from simpleDataFile import simpleDataFile
from cdmsHandler import parseCDMSvars
from upscale_domains import stashify
import sys,os
import cdms2

def UPSCALEcdmsHandler(path):
    ''' Provides a view of a netcdf or pp file using the cdat interface, but
    using upscale metadata '''
    path=os.path.abspath(path)
    f,e=os.path.splitext(path)
    ncf=cdms2.open(path)
    fvars=ncf.getVariables()
    fileMetadata={}
    for k in ['tracking_id','history','input_file_format']:
        if hasattr(ncf,k): fileMetadata[k]=getattr(ncf,k)
    basepath=os.path.basename(path)
    s=stashify()
    ffvars=s.fix(fvars,basepath)
    return parseCDMSvars(ffvars,fileMetadata,'.pp')

if __name__=="__main__":
    if len(sys.argv) < 2:
        print 'Usage: python viewFile.py filename'
        exit()
    fname=sys.argv[1]
    sdf=simpleDataFile(handler=UPSCALEcdmsHandler,debug=False)
    r=sdf.create_from_disk(fname,'unknown checksum')
    # do it again, just for the sake of wondering about repeated invocations
    #sdg=simpleDataFile(handler=cdmsHandler,debug=False)
    #rr=sdg.create_from_disk(fname,'unknown checksum')
    print sdf.properties
    #print sdf.contents['variables']
    
    #data=[(v['name'],v['cell_methods'],v['grid'],) for v in sdf.contents['variables']]
    #for d in data: print '%s (%s): %s'%d 
    #print 'Grids ',[g['name'] for g in sdf.contents['grids']]
    #print sdf.contents['variables']
    print 'bnl'
    print sdf.view()
