#!/bin/bash

runfile=/home/users/mjones07/science/xjanp_conv/theta_calc_run.sh
errfile=/home/users/mjones07/science/xjanp_conv/log_theta

rm -f $errfile

for fieldfile in /group_workspaces/jasmin/hiresgw/xjanp/xjanpa.pb??????01; do
    
    bsub -q lotus -o $errfile $runfile $fieldfile

done
