#!/bin/bash

jugfile=/home/users/mjones07/science/jugrunsplit.sh
errfile=/home/users/mjones07/science/bsubErrSplit

rm -rf par_mon_mean_split.jugdata/
rm -f $errfile
rm -f /group_workspaces/jasmin/hiresgw/mj07/monthly_means/xjanpa.monthlymean.usingsplit.u.nc
rm -f /group_workspaces/jasmin/hiresgw/mj07/monthly_means/temp_files_test/*

/usr/bin/jug_py27 status /home/users/mjones07/science/par_mon_mean_split.py &


#for i in 1 2 3 4 5 6 7 8 9 10 11 12; do
    
bsub -q lotus -n 90 -o $errfile $jugfile 

#done
