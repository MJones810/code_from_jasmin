#!/usr/bin/env python2.7
import cdms2

def pp2nc(ppdir,ppfile,t):
	""" Converts pp file for u_1 variable at a specific time level to 
	    an nc file.
	"""
	f = cdms2.open(ppdir+ppfile)
	vars = f.getVariables()
	u_1 = vars[4]
	print 'Variable being saved', u_1
	ncfile = ppfile+"."+str(t)+".u"+".nc"
	f2 = cdms2.open(ncfile,'w')
	u_t = u_1[t,:,:,:]
	print 'Writing ', ncfile
	f2.write(u_t)
	f.close()
	f2.close()
	

if __name__ == '__main__':
	ppdir = "/group_workspaces/jasmin/hiresgw/xjanp/pp/"
	ppfile = "xjanpa.pj19910301.pp"
	timelevel = 1 
	pp2nc(ppdir,ppfile,timelevel)
