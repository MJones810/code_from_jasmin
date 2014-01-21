#!/bin/bash

jugfile=/home/users/mjones07/science/jugrun.sh
errfile=/home/users/mjones07/science/bsubErr

rm -rf par_mon_mean.jugdata/
rm -f $errfile

for i in 1 2 3 4 5 6 7 8 9 10 11 12; do
    
    bsub -q lotus -o $errfile $jugfile 

done
