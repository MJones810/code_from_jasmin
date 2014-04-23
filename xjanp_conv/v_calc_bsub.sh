#!/bin/bash

runfile=/home/users/mjones07/science/xjanp_conv/v_calc_run.sh
errfile=/home/users/mjones07/science/xjanp_conv/log_v

rm -f $errfile

for fieldfile in /group_workspaces/jasmin/hiresgw/xjanp/xjanpa.pi??????01; do
    
    bsub -q lotus -o $errfile $runfile $fieldfile

done
