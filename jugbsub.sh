#!/bin/bash

jugfile=/home/users/mjones07/science/jugrun.sh
errfile=/home/users/mjones07/science/bsubErr
jugsave=xjanpa.pj19910301.u.nc

rm -rf conv2ncJug.jugdata/
rm -f $jugsave
rm -f $errfile

python2.7 createNC.py
chmod 757 $jugsave

for i in 1 2 3 4 ; do
    
    bsub -q lotus -o $errfile $jugfile 

done
