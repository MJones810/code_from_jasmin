#!/bin/bash

jugfile=/home/users/mjones07/science/jugrun_theta.sh
errfile=/home/users/mjones07/science/logs/bsubErr_theta

rm -rf par_mon_mean_theta.jugdata/
rm -f $errfile
rm -f /group_workspaces/jasmin/hiresgw/mj07/monthly_means/xjanpa.monthlymean.theta.nc
rm -f /group_workspaces/jasmin/hiresgw/mj07/monthly_means/temp_files/*.theta.*

/usr/bin/jug status /home/users/mjones07/science/par_mon_mean_theta.py &


#for i in 1 2 3 4 5 6 7 8 9 10 11 12; do
    
bsub -q lotus -n 36  -o $errfile $jugfile 

#done
