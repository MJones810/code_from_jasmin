########################################################################
# collectionTool
#    - is used to update a collection description held in a simpleIndex
#    which is located at a path which needs to be in an environment
#    variable called SIMPLE_INDEX_PATH
#    - should be run in the directory for which a collection index
#    exists, or should be created.
#    
#
########################################################################

import os, sys

from simpleTools import isomodtime,simpleCollection,collectionIndex,\
                        simpleRegistry,simpleDataFile,simpleChecker,\
                        simpleSerialiser
from cdmsHandler import cdmsHandler


class myObject(object):
    ''' Used to hold key characteristics of an object from the point
    of view of handling the collection parsing, not as a description 
    as such. '''
    def __init__(self,path,collection,index,isFile):
        self.path=path
        self.inCollection=collection
        self.isFile=isFile
        self.index=index
        self.modtime=isomodtime(self.path)
        self.checksum=None
        #self.ok is monkey patched on later in the checker routine
        
def check(filePath,checker):
    return checker(filePath,'size')  #use 'size' for testing, 'sha1' for real.
    
def fileTheSame(f,checker):
    ''' Get a checksum for a file, and compare it with the index copy,
    return (True,checksum) if the same, (False,checksum) if not. '''
    ondiskChecksum=check(f.path,checker)
    indexChecksum=f.checksum
    if str(indexChecksum) != str(ondiskChecksum):
        f.checksum=ondiskChecksum
        f.ok=False
    else: f.ok=True
    f.ok=False
    print 'Forcing failure of fileTheSame for checking purposes!'
    print f.path,ondiskChecksum,indexChecksum,f.ok
    return f

def parseFile(f):
    ''' Get the contents of a file and update it in the index '''
    #FIXME: more elegant method of hardwiring handler for jug needed
    print 'parsing',f.path
    this=simpleDataFile(handler=cdmsHandler)
    print 'initialised ok'
    this.create_from_disk(f.path,f.checksum)
    print 'is done'
    return this
   
def parseCollection(collectionObject,index,toolset):
    ''' Given a collection object, update it's record '''
    # we have all the files in the index now, let's find them:
    files=index.getFilesFor(collectionObject.path)
    # and we have all the subdirectories too? (What order do we do this in?)
    directories=index.getSubCollectionsFor(collectionObject.path)
    s=simpleCollection(index)
    s.create(collectionObject.path,collectionObject.inCollection,files)
    s.extract()
    index.updateCollection(s)

def setupWalk(path,indexpath,toolset,ignoreHidden=True):
    ''' This routine sets up the investigation of a directory path for
    badc collection objects. 
    toolRegistry=simpleRegistry(checker=simpleChecker,
        serialiser=simpleSerialiser,
        handler={'registered':['.nc','.pp'],'handler':cdmsHandler})    
    The issue to be solved here is that we want to set up a bunch
    of tasks for parallelisation, but we want to avoid race conditions
    if the directory is, or the files are, being updated as we go.
    
    So, we do this in a number of passes:
    
    1) Find all the directories and files and directory modification
    dates at a given time. Stick them in a queue.
    
    2) For each directory, parse the file list for that mod date
    and add the files into a checksum queue.
    
    3) For each file in the checksum queue, if it fails, add it to
    a parsing queue. If it's disappeared, then make sure the 
    directory is updated.
    
    4) Update the directory descriptions
    
    '''
    
    index=collectionIndex(indexpath,simpleSerialiser)
    collections={}
    filestocheck=[]
    if path == '.': path=os.getcwd()
    collections[path]=myObject(path,None,index,False)
    for root,dirs,files in os.walk(path):
        filepaths=[os.path.join(root,f) for f in files]
        filestocheck+=[myObject(f,root,None,True) for f in filepaths]
        for d in dirs:
            if not (ignoreHidden or d[0]=='.'):
                path=os.path.join(root,d)
                collections[path]=myObject(path,root,index,False)
    
    # At this point we have a list of collections and a list of files.
    # Begin by dealing with the files, since they'll influence our
    # collections.
    
    fhandler=toolset.handler['handler']
    checkable=[]
    for f in filestocheck:
        # first make sure we can handle it
        details=os.path.splitext(f.path)
        if len(details)<>2: continue
        if details[1] not in toolset.handler['registered']: 
            continue
        # TODO WORKING; this is the fella that causes the problems!
        # we now know it is the use of the index that causes the problem
        # not the assignment.
        #x=index.getChecksumFor(f.path)
        f.checksum=u'123'
        checkable.append(f)
    
    
    checkout=[fileTheSame(f,toolset.checker) for f in checkable]
   
    
    filestoparse=[]  
    for f in checkout:
        if not f.ok: filestoparse.append(f)
        
    print 'b1',filestoparse
    print 'indices',[(f.index,f.checksum,f.checksum.__class__) for f in filestoparse]
    
    fileobjects=[parseFile(f) for f in filestoparse]
        
    print 'b2',fileobjects
    
    #can't pickle (and hence jug) cursor objects
    for this in fileobjects:  index.updateFile(this)
    
    # A collection will need updating, if either files or subcollections
    # have been added since we last looked at it, or the content of 
    # the files has been modified.
    
    collectionsTODO = [collections[c] for c in collections 
                            if index.needsUpdate(collections[c].path)]
    cpaths = [c.path for c in collectionsTODO]
    
    # now get any collections where files have been updated.
    for this in fileobjects:
        path,f=os.path.split(this.properties['path'])
        if path not in cpaths:
            collectionsTODO.append(collections[this.inCollection])
        
    # and now at this point we can go back and rebuild our collections
    for c in collectionsTODO: parseCollection(c,index,toolset)
    return index
    
if __name__=="__main__":

    #using environment variables because I don't know how to get arguments in via jug
    msg='No valid collection index path (SIMPLE_INDEX_PATH) in environment'
    try:
        ipath=os.environ['SIMPLE_INDEX_PATH']
        #ipath='./'
    except KeyError:
        raise ValueError(msg)
    if not os.path.exists: raise ValueError(msg)
       
       
    toolRegistry=simpleRegistry(checker=simpleChecker,
        serialiser=simpleSerialiser,
        handler={'registered':['.nc','.pp'],'handler':cdmsHandler})    
    index=setupWalk(os.curdir,ipath,toolRegistry)
    index=collectionIndex(ipath,simpleSerialiser)
    print str(index)
    
	
