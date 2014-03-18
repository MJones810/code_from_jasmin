#!/bin/bash

runfile=/home/users/mjones07/science/conv2pyRun_u.sh
errfile=/home/users/mjones07/science/bsubErrConv_u

rm -f $errfile
#rm -f /group_workspaces/jasmin/hiresgw/mj07/xjanpa.pj*

for fieldfile in /group_workspaces/jasmin/hiresgw/xjanp/xjanpa.pj????????; do
    
    bsub -q lotus -o $errfile $runfile $fieldfile

done
