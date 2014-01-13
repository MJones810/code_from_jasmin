
# 
#  Copyright 2013 Bryan Lawrence <b.n.lawrence@reading.ac.uk>

import cdtime
import cdms2
import os
import numpy as np

#
# The simple data model that this exposes is that
# files consist of properties, variables and grids

# The method needs to return a dictionary with these
# three items.

# The properties are expected to be a dictionary of key:value pairs

# The variables list is a list of dictionary items, with
# meaningful keys and values. It is allowed for values
# themslves to be dictionaries, but only one level of nesting.

# The grid list is targeted at supporting minimal description
# via extent and resolution (number of grid points) (and what
# sort of coordinates are involved).
#

def cdmsHandler(path):
    ''' Provides a view of a netcdf or pp file using the cdat interface.
    '''
    f,e=os.path.splitext(path)
    if e not in ['.pp','.nc']: raise ValueError('cdmsHandler cannot handle %s'%e)
    ncf=cdms2.open(path)
    fileMetadata={}
    for k in ['tracking_id','history','input_file_format']:
        print k
        if hasattr(ncf,k): 
            print 'hello'
            print getattr(ncf,k)
            fileMetadata[k]=getattr(ncf,k)
    
    fvars=ncf.getVariables()
    return parseCDMSvars(fvars,fileMetadata,e)
   
def parseCDMSvars(fvars,fileMetadata,e):    
    ''' Does the actual parsing of variables '''
    grids=[]
    results={'variables':[],'grids':grids,'properties':{}}
    for k in fileMetadata: results['properties'][k]=fileMetadata[k]
    ftime=None
    for v in fvars:
        detail={}
        for k,vv in [('name_in_file','name_in_file'),
                ('long_name','long_name'),
                ('standard_name','standard_name'),
                ('units','units'),
                ('cell_methods','cell_methods')]:
            if hasattr(v,vv): detail[k]=getattr(v,vv)
        for n in ['standard_name','_fixed_name','long_name','name_in_file']:
            if n in detail: 
                detail['name']=detail[n]
                break
        print n,detail['name']
        if 'cell_methods' not in detail: detail['cell_methods']='unknown'
        if e in ['.pp','.xml']:
            stash={}
            for k,vv in [ ('item','stash_item'),
                         ('model','stash_model'),
                         ('section','stash_section')]:
                if hasattr(v,vv):
                    if e=='.pp':
                        stash[k]=getattr(v,vv)[0]
                    elif e== '.xml':
                        stash[k]=getattr(v,vv)
            if stash<>{}: detail['stash']=stash
        grid,time=cdmsExtentHandler(v)
        detail['size']=grid['size']
        detail['grid']=grid['name']
        results['variables'].append(detail)
        
        if grid not in grids: 
            grids.append(grid)
        if ftime is None: 
            ftime=None
        elif time <> ftime:
            print ftime,time 
            raise ValueError('Multiple time ranges in file')
    results['properties']['timeAxis']=time        
    return results


def cdmsExtentHandler(v):
    ''' Takes a cdms2 variable and grabs what we need for extent definitions '''
    
    # first get the temporal bits:
    
    ta=v.getAxisList(['time'])
    if len(ta)>0:
        ta=ta[0]
        tdata=ta.asComponentTime()
        daterange=[str(tdata[0]),str(tdata[-1])]
        if hasattr(ta,'calendar'):
            calendar=str(ta.calendar)
        else: calendar=None
        time={'daterange':daterange,'calendar':calendar,'nt':len(ta)}
    else: time=None
    
    # now xy
    xa=v.getAxisList(['lon'])
    ya=v.getAxisList(['lat'])
    za=v.getAxisList(['lev'])
    nxa,nya,nza=len(xa),len(ya),len(za)
    
    extent={}
    
    if nxa>0:
        x=xa[0]
        extent['lonmin'],extent['lonmax'],extent['xunits']=x[0],x[-1],x.units
        nx=len(x)
    else: nx=0
   
    if nya>0:
        y=ya[0]
        extent['latmin'],extent['latmax'],extent['yunits']=y[0],y[-1],y.units
        ny=len(y)
    else: ny=0
    
    if nza>0:
        z=za[0]
        nz=len(z)
        if hasattr(z,'positive'):
            if z.positive=='up': 
                i,j=0,-1
            else: i,j=-1,0
        else: i,j=0,-1
        extent['zmin'],extent['zmax'],extent['zunits']=z[i],z[j],z.units
        extent['zid']=z.id
        if hasattr(z,'long_name'): extent['zlong_name']=z.long_name
    else: nz=0
    result={'name':'G_%s_%s_%s'%(nx,ny,nz),'extent':extent,'size':v.size()}
    if time is not None: 
        assert time['nt']<>0,'Unexpected zero length time axis'
        result['size']=result['size']/time['nt']
    return result,time

    
if __name__=="__main__":
    #test with a real file
    import sys
    f= sys.argv[1]
    r=cdmsHandler(f)
    print r
    
 

