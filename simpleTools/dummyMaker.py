
#
# Make some dummy data for use in testing these routines
#

import cdtime
import cdms2
import os
import numpy as np

def makeDummyNC(filename):
    ''' This makes some dummy data for use in test routines '''
    f=cdms2.open(filename,'w')
    nx,ny,nz,nt=30,12,4,12
    lat=np.linspace(-30,30,ny)
    lon=np.linspace(0,330,nx)
    z=np.linspace(1,4,nz)
    t=np.linspace(1,14,nt)
    tb=np.array([[ti,ti+1] for ti in t])
    tax=cdms2.createAxis(t)
    tax.id='time'
    tax.units='days since 2013-1-1'
    tax.setBounds(tb)
    xax=cdms2.createAxis(lon)
    xax.id='longitude'
    xax.units='degrees_east'
    yax=cdms2.createAxis(lat)
    yax.id='latitude'
    yax.units='degrees_north'
    zax=cdms2.createAxis(z)
    zax.id='levels'
    d=np.outer(np.sin(lon),np.cos(lat))
    data=np.resize(d,(nx,ny,nz,nt))
    dv=cdms2.createVariable(data,axes=[xax,yax,zax,tax],fill_value=-999.)
    dv.long_name='Dummy Data'
    dv.units='Kelvin'
    shape=dv.shape
    f.write(dv)
    f.close()
    return shape
