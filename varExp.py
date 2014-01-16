#!/usr/bin/env python2.7
import cdms2
ppdir = "/group_workspaces/jasmin/hiresgw/xjanp/pp/"
ppfile = "xjanpa.pf19910301.pp"
f=cdms2.open(ppdir+ppfile)
vars=f.getVariables()
print vars
f.close()
