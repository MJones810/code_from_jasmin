#!/bin/bash

runfile=/home/users/mjones07/science/conv2pyRun_p.sh
errfile=/home/users/mjones07/science/bsubErrConv_p

rm -f $errfile
#rm -f /group_workspaces/jasmin/hiresgw/mj07/xjanpa.ph*

for fieldfile in /group_workspaces/jasmin/hiresgw/xjanp/xjanpa.ph????????; do
    
    bsub -q lotus -o $errfile $runfile $fieldfile

done
