#!/bin/bash

runfile=/home/users/mjones07/science/conv2pyRun.sh
errfile=/home/users/mjones07/science/bsubErr

rm -f $errfile


for ppfile in /group_workspaces/jasmin/hiresgw/xjanp/pp/xjanpa.pj*; do
    
    bsub -q lotus -o $errfile $runfile $ppfile

done
