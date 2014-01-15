#!/bin/bash

jugfile=/home/users/mjones07/science/jugrun.sh
errfile=/home/users/mjones07/science/bsubErr

rm -rf conv2ncJug.jugdata/
rm -f xjanpa.pj19910301.u.nc
rm -f $errfile

python2.7 createNC.py


for i in 1 2 3 4; do
    
    echo $i
    bsub -q lotus -o $errfile $jugfile 

done
