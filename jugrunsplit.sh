#!/bin/bash

for i in {1..180}; do

    /usr/bin/jug_py27 execute /home/users/mjones07/science/par_mon_mean_split.py &

done
