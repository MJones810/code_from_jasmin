upscale_timedomains={
'T6HMN':'Mean over 30 days sampled every 6 hours',
'T24H0Z':'Instantaneous values at 0Z every 24 hours',
'T6H':'Instantaneous values at 6 hourly intervals starting at 0Z',
'T6HDAYM':'Daily mean of values sampled every 6 hours',
'TDAYM':'Daily mean, sampled each timestep',
'TDAYMAX':'Daily maximum of timestep data',
'TDAYMIN':'Daily minimum of timestep data',
'TMONMN':'Monthly mean data sampled every timestep',
'T30DAY':'Instantaneous values output once every 30 days',
'TMPMN00':'Monthly mean of values at 0Z (for diurnal cycle)',
'TMPMN03':'Monthly mean of values at 3Z',
'TMPMN06':'Monthly mean of values at 6Z',
'TMPMN09':'Monthly mean of values at 9Z',
'TMPMN12':'Monthly mean of values at 12Z',
'TMPMN15':'Monthly mean of values at 15Z',
'TMPMN18':'Monthly mean of values at 18Z',
'TMPMN21':'Monthly mean of values at 21Z',
'T3HDAYM':'Daily mean sampled every 3 hours',
'T6HRMAX':'Maximum value of timestep data in each 6 hour period',
'T3H':'Instantaneous values every 3 hours from 0Z',
'T3HMN':'3 hourly means of timestep data',
}
domain_definitions={
'DIAG':'Standard 2D diagnostic field',
'DALLTH':'All theta levels',
'DALLRH':'All rho levels',
'D52TH':'Bottom 52 theta levels',
'D1TH':'Bottom theta level',
'D52RH':'Bottom 52 rho levels',
'DA7ISSCP':'ISCCP',
'DIAGAOT':'SW radiation bands 1-6',
'DPBLTH':'Boundary layer theta levels (bottom 50 levels)',
'DSOIL':'Soil levels',
'DTOPSOIL':'Surface soil level',
'DTILE':'Land and vegetation surface types 1-9 (on 1 degree grid?)',
'DTILEURB':'Land and vegetation surface types 3 & 6 (on 1 degree grid?)',
'DPFTS':'Land and vegetation surface types 1-5 (on 1 degree grid?)',
'DP31CCM':'Pressure levels (hPa): 1000, 850, 700, 500, 400, 300, 250, 200, 170, 150, 130, 115, 100, 90, 80, 70, 50, 30, 20, 15, 10, 7, 5, 3, 2, 1.5, 1, 0.5, 0.3, 0.2, 0.1',
'DP31CCMZ':'Zonal mean of pressure levels in DP31CCM',
'DP500':'Pressure levels (hPa): 500',
'DP17':'Pressure levels (hPa): 1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10',
'DP8':'	 Pressure levels (hPa): 925, 850, 600, 500, 400, 300, 200, 100',
'DP3':'Pressure levels (hPa): 850, 500, 250, 200',
'DP7':'Pressure levels (hPa): 1000, 850, 700, 500, 250, 100, 10',
'DP_HEAVI':	'Pressure levels (hPa):1000, 925, 850, 700, 600. This profile is only used by the Heaviside function fields (30-301) for pressure levels above 600 you will need to assume that the fields are 1 everywhere. This assumption has been checked and this profile is used to reduce the volume of unnecessary high temporal resolution data being generated.'
}

import cdms2

def cdmetacopy(v):
    ''' Take a cdms2 file variable,v, and copy the relevant metadata into a new 
    transient variable '''
    # ->
    #nv=cdms2.createVariable(v,copy=0)
    #failed with IOError
    #File "/usr/lib64/python2.6/site-packages/cdms2/fvariable.py", line 83, in expertSlice
    #result = apply(self._obj_.getitem,slist)
    # ->
    #nv = v.clone(copyData=0)
    #AttributeError, 'FileVariable' object has no attribute 'clone'
    return nv
    

class stashify(object):
    ''' Given an opened CDMS file, get further attributes from the 
    stash text file and patch the variable attributes appropriately '''
    def __init__(self,stashtxt='upscale_raw_stash.txt'):
        '''The stash text file is expected to consist of lines each of which contain
        two integers, three 'delimetered strings', and one final string without
        delimiters. All seperated by spaces, e.g.:
        16	 203	 'TEMPERATURE ON P LEV/P GRID '	 'TMONMN '	 'DP17 '	 apj
        where the integers are the stash section and id respectively, the first
        string is a "cf_long_name" candidate, the next two strings are from the
        domains defined above, and the final string is a stream (directory) 
        identifier.'''
        f=open(stashtxt,'r')
        stashview={}
        streamview={}
        for l in f.readlines():
            chunks=l.split("'")
            st=chunks[0].split('\t')
            section,stashid=int(st[0]),int(st[1])
            name,meaning,domain,stream=chunks[1],chunks[3],chunks[5],chunks[6]
            stashCode=1000*section+stashid
            stashview[stashCode]={'name':name,
                                  'meaning':meaning,
                                  'domain':domain,
                                  'stream':stream}
            if stream not in streamview:
                streamview[stream]={}
            streamview[stream][stashCode]={'name':name,
                                  'meaning':meaning,
                                  'domain':domain}
        self.stashV=stashview
        self.streamV=streamview
        
    def fix(self,variables,basepath=''):
        ''' Fix each and every variable in a list of
        variables by adding stash attributes '''
        streamOK=0
        if basepath <> '':
            stream=basepath[-3:]
            if  stream in self.streamV:
                streamOK=1
        if not streamOK: print 'Unable to utilise stream based information'
        for v in variables:
            if not hasattr(v,'stash_item'):
                msg='variable %s has no stash data (coordinate?)'%v
                #raise ValueError(msg)
                print msg 
            else:
                #turns out the xml version has these as integers;
                if type(v.stash_section)==int:
                     stashCode=1000*v.stash_section+v.stash_item
                else:
                    stashCode=1000*v.stash_section[0]+v.stash_item[0]
                #newv=cdmetacopy(v)
                if stashCode in self.stashV:
                    setattr(v,'_fixed_name',self.stashV[stashCode]['name'])
                if streamOK:
                    for i in ['meaning','domain']:
                        setattr(v,
                            '_fixed_%s'%i,self.streamV[stream][stashCode][i])
            for k in ['_fixed_name','_fixed_meaning','_fixed_domain']:
                if hasattr(v,k): print 'Fixed %s %s'%(k,getattr(v,k))
        return variables
            
         
