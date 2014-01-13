#!/usr/bin/env python2.7
import cdms2
ppdir = "/group_workspaces/jasmin/hiresgw/xjanp/pp"
ppfile = "xjanpa.pf19910301.pp"
f=cdms2.open(ppdir+ppfile)
vars=f.getVariables()
print vars
swhr=vars[9]
f2=cdms2.open('xjanpa.19920111.uutest1.nc','w')
s0=swhr[0,:,:,:]
f2.write(s0)
f2.close()
