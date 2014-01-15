#!/usr/bin/env python2.7

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

f = Dataset('xjanpa.pj19910301.u.nc','r')

u = f.variables['u']

print 'u = ',u.shape

# take a small slice for speed
u_slice = u[:,::10,::20,::20]
print 'u_slice = ', u_slice.shape
# Calculate zonal mean
u_zm = np.mean(u_slice,3)

print 'u_zum = ', u_zm.shape

plt.contour(u_zm[:,:,18])
plt.show()
