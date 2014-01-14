#!/usr/bin/env python2.7
import cdms2

def pp2nc(ppdir,ppfile,t,t1):
	""" Converts pp file for u_1 variable at a specific time level to 
	    an nc file.
	"""
	f = cdms2.open(ppdir+ppfile)
	vars = f.getVariables()
	u_1 = vars[9]
	print 'Variable being saved', u_1
	ncfile = ppfile+"."+str(t)+"to"+str(t1)+".u"+".nc"
	f2 = cdms2.open(ncfile,'w')
	u_t = u_1[t:t1,:,:,:]
	print 'Writing ', ncfile
	f2.write(u_t)
	f.close()
	f2.close()
	

if __name__ == '__main__':
	ppdir = "/group_workspaces/jasmin/hiresgw/xjanp/pp/"
	ppfile = "xjanpa.pj19910301.pp"
	timelevelmin = 0
	timelevelmax = 3 
	pp2nc(ppdir,ppfile,timelevelmin,timelevelmax)
