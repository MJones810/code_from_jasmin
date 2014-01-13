#  Copyright 2013 Bryan Lawrence <b.n.lawrence@reading.ac.uk>

import cf
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

#~~~~~~ THIS VERSION IS NOT IN USE, IT'S SIMPLY A COPY OF CDMSHANDLER
# READY FOR REWRITING INTO THE SAME API ...
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def cfExtentHandler(v):
    ''' Takes a cf field and grabs what we need for extent definitions '''
    d=v.domain   # cf domain
    coords={}
    for c in d.values():
        name=c.name()
        coords[name]={'length':len(c.shape[0])}
        for u in ['calendar','units']:
            if hasattr(c,u):coords[name][u]=getattr(c,u)
        
    # first get the temporal bits:
    if 'time' in coords:
      
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

def cfHandler(path):
    ''' Provides a view of a netcdf or pp file using the cf python interface '''
    f,e=os.path.splitext(path)
    if e not in ['.pp','.nc']: raise ValueError('cfHandler cannot handle %s'%e)
    print 'opening [%s]'%path
    print path.__class__
    ncf=cf.read(path)
    print 'opened %s'%path
    grids=[]
    results={'variables':[],'grids':grids,'properties':{}}
    ####### This next needs to be modified
    for k in ['tracking_id','history','input_file_format']:
        if hasattr(ncf,k): results['properties'][k]=getattr(ncf,k)
    # 
    # now we need to find the CF fields in the file
    #
    print 'moving on'
    for v in ncf:
        detail={}
        for k,vv in [('name','name_in_file'),
                ('long_name','long_name'),
                ('units','units'),
                ('cell_methods','cell_methods')]:
            if hasattr(v,vv): detail[k]=getattr(v,vv)
        if e:
            stash={}
            for k,vv in [ ('item','stash_code'),
                         ('model','source'),
                         ('runid','runid')]:
                if hasattr(v,vv):stash[k]=getattr(v,vv)[0]
            if stash<>{}: detail['stash']=stash
        grid,time=cfExtentHandler(v)
        detail['size']=grid['size']
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
    
if __name__=="__main__":
    #test with a real file
    import sys
    f= sys.argv[1]
    r=cfHandler(f)
    print r
    
 

