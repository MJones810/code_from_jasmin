#!/bin/bash

runfile=/home/users/mjones07/science/conv2pyRun_v.sh
errfile=/home/users/mjones07/science/bsubErrConv_v

rm -f $errfile
#rm -f /group_workspaces/jasmin/hiresgw/mj07/xjanpa.pi*

for fieldfile in /group_workspaces/jasmin/hiresgw/xjanp/xjanpa.pi????????; do
    
    bsub -q lotus -o $errfile $runfile $fieldfile

done
