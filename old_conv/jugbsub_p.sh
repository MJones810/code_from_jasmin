#!/bin/bash

jugfile=/home/users/mjones07/science/jugrun_p.sh
errfile=/home/users/mjones07/science/logs/bsubErr_p

rm -rf par_mon_mean_p.jugdata/
rm -f $errfile
rm -f /group_workspaces/jasmin/hiresgw/mj07/monthly_means/xjanpa.monthlymean.p.nc
rm -f /group_workspaces/jasmin/hiresgw/mj07/monthly_means/temp_files/*.p.*

/usr/bin/jug status /home/users/mjones07/science/par_mon_mean_p.py &


#for i in 1 2 3 4 5 6 7 8 9 10 11 12; do
    
bsub -q lotus -n 36  -o $errfile $jugfile 

#done
