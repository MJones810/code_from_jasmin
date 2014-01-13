#!/usr/bin/env python2.7
import netCDF4 as nc
import numpy as np
import cfplot as cfp
import os

def getlonAxis(d,l):
    ''' Helper function to find longitude axis <l> in dimensions tuple <d> '''
    dl=list(d)
    for i in range(len(dl)):
        if dl[i]==l: return i
    raise ValueError('No longitude axis <%s> found in dimensions <%s>'%(l,d))
    
def zonmean(x,axis='longitude0'):
    ''' For a given field, x, assuming it's a standard netcdf4 variable,
    get a zonal mean as a numpy array '''
    maxis=getlonAxis(x.dimensions,axis)
    y=x[:]  # it turns out that a masked array operation on a 
            # netcdf variable doesn't respect the mask.
    r=np.ma.mean(y,axis=maxis)
    return r
    
def getfromfile(filename,name):
    ''' Return a field variable and it's dimension variables from a netcdf file '''
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
        
def lowerPrecision(var,bits):
    ''' Return a reduced precision version of var (in order
    to improve compression when using netcdf4 compressed writing) '''
    scale=pow(2.,bits)
    y=var[:]
    dataout = np.around(scale*y)/scale
    if np.ma.isMA(y):
        datout.set_fill_value(y.fill_value)
    return dataout

def makevar(ncfile,numpyVariable,name,dimensions,complevel=0):
    ''' Given a numpy variable defined over axes, create a netcdf4 variable, 
    with name in ncfile.'''
    zlib=True
    if complevel==0: zlib=False
    x = ncfile.createVariable(name,'f',dimensions=dimensions,
        zlib=zlib,complevel=complevel)
    x[:]=numpyVariable
    return x

def writefld(varname,var,axes,outfilename,keepbits=0,complevel=0):
    ''' Write a netcdf file containing var to outfilename.
    If keepbits is not 0, then keep precision of output to 2**<keepbits>.
    Mimic'ing WGDOS I hope, with a nod to netcdf4's LSD _quantize method.
    If complevel is not 0, compress (it makes no real sense to have
    keepbits non-zero and complevel zero!)
    '''
    print 'Creating ', outfilename
    newd=nc.Dataset(outfilename,'w',format='NETCDF4')
    print 'Basic file created'
    #create dimensions
    dim=[]
    for a in axes:
        n=newd.createDimension(a._name,len(a))
        dim.append(a._name)
        vdim=makevar(newd,a[:],a._name,(a._name,))
    print 'Dimensions written'
    if keepbits<>0:
        data=makevar(newd,lowerPrecision(var,keepbits),varname,tuple(dim),
                     complevel)
        data.comment='Compressed to %s bits precision'%keepbits
    else:
        data=makevar(newd,var,varname,tuple(dim),complevel)
    print 'trying to write',data
    newd.close()

def plotzm(filename,name,
    lonName='longitude0',latName='latitude0',zName='z0_hybrid_height',
    getzm=True):
    ''' Plot zonal mean of variable <name> from <filename> using <ptype> from cfplot '''
    v,axes=getfromfile(filename,name)
    newAxes=[]
    if getzm:
        assert len(v.shape)==3,'Expected a 3D variable'   
        data=zonmean(v,axis=lonName)
        f,p=os.path.splitext(filename)
        newf=f+'-zm'+p
        for k in v.dimensions:
            if k<>lonName: newAxes.append(axes[k])
        writefld(name+'-zm',data,newAxes,newf)
        v=data      
    else:
        assert len(v.shape)==2,'Expect a 2D variable when getzm is False'
    cfp.con(f=v, x=axes[latName], y=axes[zName], title='%s(%s)'%(name,filename))
    
def fcopyvar(oldvar,axes,newfileName,
    keepbits=0, # default, no bit truncation,
    complevel=0, # default, no compression
    ):
    ''' Copy a netcdf variable from one file to a new file, with new compression
    options. Currently used for testing. '''
    newAxes=[]
    for k in oldvar.dimensions: newAxes.append(axes[k])
    writefld(oldvar._name,oldvar,newAxes,newfileName,
        keepbits=keepbits,
        complevel=complevel
        )
    
    
if __name__=="__main__":
    import sys
    name=sys.argv[1]
    filename=sys.argv[2]
    if len(sys.argv)==6: 
        plotzm(filename,name,
            lonName=sys.argv[3],latName=sys.argv[4],zName=sys.argv[5])
    else:
        plotzm(filename,name)
    
    
    
    
