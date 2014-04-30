#!/bin/bash

runfile=/home/users/mjones07/science/T_calc/T_calc_run.sh
errfile=/home/users/mjones07/science/T_calc/log

rm -f $errfile

for fieldfile in /group_workspaces/jasmin/hiresgw/mj07/xjanpa.??????01.p.nc; do
    
    bsub -q lotus -o $errfile $runfile $fieldfile

done
