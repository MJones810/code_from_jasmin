#!/usr/bin/env python2.7
import cdms2
ppdir = "/group_workspaces/jasmin/hiresgw/xjlef/"
ppfile = "xjlefa.pi19810901"
f=cdms2.open(ppdir+ppfile)
vars=f.getVariables()
print vars

