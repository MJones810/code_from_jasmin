#!/bin/bash

runfile=/home/users/mjones07/science/xjanp_conv/u_calc_run.sh
errfile=/home/users/mjones07/science/xjanp_conv/log_u

rm -f $errfile

for fieldfile in /group_workspaces/jasmin/hiresgw/xjanp/xjanpa.pj??????01; do
    
    bsub -q lotus -o $errfile $runfile $fieldfile

done
