#!/usr/bin/env python
''' Adds my name, date and filename to plots
'''

import matplotlib.pyplot as plt
import os
import time


def addInfo(figref,name=True,email=True,date=True,time_=False,filename=False,model=False):
    ''' Adds my name, the date and the filname produced
        
        Defaults: name, email, date
        options: time, filename, model
    '''
    if name:
        figref.text(0.01,0.04,'Matthew Jones',fontsize=8)
    if email:
        figref.text(0.01,0.02,'m.jones3@pgr.reading.ac.uk',fontsize=7)
    if date:
        datestr = time.strftime("%x")
        figref.text(0.92,0.02,datestr,fontsize=8)
    if time_:
        timestr = time.strftime("%H:%M:%S")
        figref.text(0.92,0.04,timestr,fontsize=8)
    if filename!=False:
        filestr = filename
        figref.text(0.3,0.02,'figure produced with %s' % filestr,fontsize=7)
    if model!=False:
        figref.text(0.92,0.07,'model : \n%s' % model,fontsize=8)
        

if __name__ == '__main__':
    ''' testing of function '''
    import numpy as np
    x = np.arange(10)
    y = x*x
    
    figref = plt.figure()
    plt.plot(x,y)
    addInfo(figref,email=True,time_=True,filename=False)
    plt.xlabel('ksuydghklsiugloairgalirgualriggalrgiarlgiglrgiua')
    plt.show()
