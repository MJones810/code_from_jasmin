#!/bin/bash 

logfile=/home/users/mjones07/science/fft_work/log

#rm $logfile

bsub -q lotus-smp -o $logfile /home/users/mjones07/science/fft_work/mean_ffts_run.sh 
