#!/usr/bin/env python2.7
# simple code to play with netcdf compression
import hiresgwBasicTools as hbt
import sys

if __name__=="__main__":

    if len(sys.argv)<>6:
        print 'Usage: compressionPlay varName, inFile, outFile, keepbits, compLevel'
    
    name,infilename,outfilename=sys.argv[1],sys.argv[2],sys.argv[3]
    keepbits,compLevel=int(sys.argv[4]),int(sys.argv[5])


    v,axes=hbt.getfromfile(infilename,name)
    hbt.fcopyvar(v,axes,outfilename,keepbits=keepbits,complevel=compLevel)
