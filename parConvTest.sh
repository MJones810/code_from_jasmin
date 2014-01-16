#!/bin/bash

runfile=/home/users/mjones07/science/conv2pyRun.sh
errfile=/home/users/mjones07/science/bsubErr

rm -f $errfile


for ppfile in xjanpa.pj19910301 xjanpa.pj19910311 xjanpa.pj19910321; do
    
    bsub -q lotus -o $errfile $runfile $ppfile

done
