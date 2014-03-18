#!/bin/bash

runfile=/home/users/mjones07/science/conv2pyRun_theta.sh
errfile=/home/users/mjones07/science/bsubErrConv_theta

rm -f $errfile
#rm -f /group_workspaces/jasmin/hiresgw/mj07/xjanpa.ph*

for fieldfile in /group_workspaces/jasmin/hiresgw/xjanp/xjanpa.pb????????; do
    
    bsub -q lotus -o $errfile $runfile $fieldfile

done
