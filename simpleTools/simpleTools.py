import os
import uuid
from cdmsHandler import cdmsHandler
import sqlite3
import subprocess
import datetime
import json

def isomodtime(path):
    ''' Returns the modification time of a file in isoformat '''
    t=os.path.getmtime(path)
    dt=datetime.datetime.fromtimestamp(t)
    return dt.isoformat()
    
class badcFileHandler(object):
    ''' Defines a file handling API '''
    def __init__(self):
        pass
    def register(self,ext,handler):
        ''' Register a handler for a specific extension. A
        handler must return properties as defined in the
        cdmsHandler example. '''
        return NotImplementedError
    def handle(self,path):
        ''' Find and return the properties for a specific
        file (must be recognised by the class) or return
        a ValueError). '''
        return NotImplementedError
    
class simpleFileHandler(badcFileHandler):
    ''' Class to register and execute file handlers'''
    def __init__(self):
        # these can be overridden by the user
        self.registered={'.nc':cdmsHandler,'.pp':cdmsHandler}
    def register(self,ext,handler):
        self.registered[ext]=handler
    def handle(self,path):
        f,e=os.path.splitext(path)
        if e not in self.registered:
            raise ValueError('%s has unrecognised filetype '%path)
        f,name=os.path.split(path)
        return self.registered[e](path)   

class simpleCollection(object):
    ''' A minimal implementation of a collection object. 
    
    Can be subclassed to provide extended implementations. 
    
    Normal usage would be to initialise empty, and either populate it 
    using the create_from_disk method, or 
    and then register the various tools necessary, then update it..
    e.g.
        s=simpleCollection()
        s.pathOndisk,parentCollection,filesInDirectory)
        s.register(checker,serialiser,index)
        s.update()
    '''
    
    def __init__(self,index):
        ''' Initialise empty, with index'''
        #empty attributes follow
        self.properties={'modificationDate':None,
                        'path':'',
                        'dataVolume':0,
                        'fileVolume':0,
                        'parent':''}
        self.contents={'subCollections':[],
                         'dataFiles':[],
                         'mygrids':[],
                         'mytrackingids':[],
                         'myvariables':[]}
        self.index=index
    
    def create(self,path,parent,fileList,indexedSubcollections=True):
        ''' Create from disk without populating file contents etc.
        '''
        isdir=os.path.isdir(path)
        assert os.path.isdir(path),'%s is not a directory'%path
        self.modify('path',path)
        self.modify('parent',parent)
        self.modify('modificationDate',isomodtime(path))
        for f in fileList: self.add('dataFiles',f)
        if indexedSubcollections:
            subcollections=self.index.getSubCollectionsFor(path)
            self.contents['subCollections']=subcollections
        else:
            #just need to look to the disk, and then add to index
            raise NotImplementedError
            
            
            
        
    def extract(self):
        ''' Extract properties and contents from files and
        aggregate into collection contents. '''
        # the list of contents we aggregate over:
        aglist='mygrids','myvariables','mytrackingids'
        #start by resetting to zero:
        for i in aglist: self.contents[i]=[]
        datav=0
        #now get the datafiles from the index
        for f in self.contents['dataFiles']:
            df=self.index.getFile(f)
            datav+=df.properties['filesize']
            for g in df.contents['grids']:
                if g not in self.contents['mygrids']:
                    self.add('mygrids',g)
            for v in df.contents['variables']:
                #have to do a piecewise comparison
                got=False
                for a in self.contents['myvariables']:
                    if self._samevariable(a,v):
                        got=True
                        break
                if not got:  self.add('myvariables',v)
            if 'tracking_id' in df.properties:  
                self.add('mytrackingids',df.properties['tracking_id'])
        self.modify('fileVolume',datav)
        # at which point we know the volume of the files, we
        # now need to add the volumes known from the subcollections
        v=self.getscvolume() 
        
    def getscvolume(self):
        ''' Return the volume of the subcollections (and
        update the value held in the collection). '''
        datav=0
        for c in self.contents['subCollections']:
            dc=self.index.getCollection(c)
            datav+=dc.properties['dataVolume']
        self.modify('dataVolume',self.properties['fileVolume']+datav)
        return datav
            
    def _samevariable(self,a,b):
        ''' Test if two variables (expressed as dictionaries) are
        the same '''
        # if present, the following need to be the same 
        have2bethesame=[
            'long_name','cf_name','units','cell_methods','stash']
        for k in have2bethesame:
            if k in a:
                if k not in b: return 0
                if a[k]<>b[k]: return 0
        return 1
        
    def modify(self,key,value):
        if key in self.properties:
            self.properties[key]=value
        else:
            raise ValueError('%s is not a collection property'%key)
            
    def add(self,key,value):
        if key in self.contents:
            if value not in self.contents[key]:
                self.contents[key].append(value)
        else:
            raise ValueError ('%s is not in the collection contents'%key)
            
    def remove (self,key,path):
        ''' Remove an item from a content set via it's path '''
        if key in self.contents:
            raise NotImplementedError
        else:
            raise ValueError ('%s is not in the collection contents'%key)  
        
    def __eq__(self,other):
        ''' Slightly complicated by required depth of comparison '''
        equal=True
        if self.properties!=other.properties: equal=False
        if not equal: return False
        if self.contents!=other.contents: equal=False
        return equal
            
    def diff(self,other):
        ''' Difference self with another '''
        return NotImplementedError
        
    def __ne__(self,other):
        return not self==other 
   
    def __repr__(self):
        return 'Collection %s'%self.properties['path']

def fileSize(path):
    '''Used for checker testing - simply returns file size in bytes '''
    assert os.path.isfile(path),'Expect a file as a path to this message'
    return os.path.getsize(path)

def simpleChecker(path,a='sha1'):
    ''' Method for getting checksums for a file at path '''
    methods={'sha1':'sha1sum'}   # use shell process name for external subprocesses
    pymethods={'size':fileSize}    # for internal python calls
    if a not in methods and a not in pymethods:
        raise ValueError('Unknown algorithm for checksum %s'%a)
    if os.path.isfile(path):
	if a in methods:
            r=subprocess.check_output([methods[a],path]).split()
            return r[0]
        else: return pymethods[a](path)
    else:
        raise ValueError('Can only checksum regular files')

class simpleDataFile(object):
    ''' A minimal implementation of a file object. Can be subclassed
    to provide extended implementations. '''
    def __init__(self,handler=None,debug=True):
        ''' Initialise empty, and populate from index or from on disk.
        If populated by disk, need a handler, passed as a class
        definition. If populated by a serialiser,
        it should use the modify and add methods rather than
        directly molesting properties and contents.'''
        
        self.properties={'modificationDate':None,'checksum':None,'name':'','path':'',
        'previousVersion':None,'history':None,'filesize':0,'input_file_format':'',
        'tracking_id':None,'notes':'','timeAxis':None}
        self.contents={'variables':[],'grids':[]}
       
        self.handler=handler
        self.debug=debug
        
    def create_from_disk(self,path, checksum):
        ''' Create a file instance by examining the file on disk.
        Assume that the checksum is provided. '''
        isfile=os.path.isfile(path)
        if not isfile:
            raise ValueError('%s is not a file'%path)
        self.modify('filesize',os.path.getsize(path))
        if self.debug: print '===> simpleDataFile: ',self.properties
        if self.debug: print 'going to handler'
        if self.debug: print self.handler,self.handler.__class__
        internal_properties=self.handler(path)
        if self.debug: print 'handled ok'
        for k in internal_properties['properties']:
            self.modify(k,internal_properties['properties'][k])
        for k in internal_properties['variables']:
            self.contents['variables'].append(k)
        for k in internal_properties['grids']:
            self.contents['grids'].append(k)
        f,name=os.path.split(path)
        self.modify('name',name)
        self.modify('path',os.path.abspath(path))
        self.modify('modificationDate',isomodtime(path))
        self.modify('checksum',checksum)
        if self.debug: print 'finished creating from disk in simpleDataFile'
    
    def modify(self,key,value):
        if key in self.properties:
            self.properties[key]=value
        else:
            raise ValueError('%s is not a file property'%key)
    def add(self,key,value):
        self.contents[key].append(value)
    def __eq__(self,other):
        return self.properties==other.properties
    def __ne__(self,other):
        return not self==other
    def __repr__(self):
        return 'dataFile %s'%self.properties['path']
        
class simpleRegistry(object):
    ''' Used to bag together the toolset needed by the tools '''
    def __init__(self,**kw):
        expected=['checker','serialiser','handler']
        for k in expected:
            if k not in kw:
                raise ValueError('Not all members of tool registry instantiated')
            setattr(self,k,kw[k])
                
class collectionIndex(object):
    ''' Provides the API needed by the collectionTool code '''
    
    class dbRecord(object):
        ''' Used to manipulate a database row '''
        def __init__(self,r):
            ''' Initialise with a tuple from a databse query '''
            self.p=['path','parent','uid','version','modtime',
                    'content','checksum']
            if r == []: 
                for a in self.p: setattr(self,a,None)
            else:
                (self.path,self.parent,self.uid,self.version,
                    self.modtime,self.content,self.checksum) = r
        def __eq__(self,other):
            ''' Same document but may be different version '''
            for a in ['path','parent','uid']:
                if getattr(self,a)!=getattr(other,a): return False
            return True
        def __ne__(self,other):
            return not self==other
        def __iter__(self):
            return iter([getattr(self,i) for i in self.p])
        def __str__(self):
            return '-->%s\n%s\n'%(
                str([(i,getattr(self,i)) for i in 'path','parent','uid']),
                str([(i,getattr(self,i)) for i in 'version','modtime','checksum']))
    
    def __init__(self,path2index,serialiser):
        ''' Location of path to the index file on disk '''
        self.basepath=path2index
        self.indexName='simple_index.db'
        if not(os.path.exists(self.basepath) and os.path.isdir(self.basepath)):
            raise ValueError('Directory %s does not exist'%self.basepath)
        self.indexfile=os.path.join(self.basepath,self.indexName)
        createIt=False
        if not os.path.exists(self.indexfile):
            createIt=True
        self.conn = sqlite3.connect(self.indexfile)
        self.cursor=self.conn.cursor()
        if createIt: 
            self.cursor.execute(
            '''CREATE TABLE documents
             (path text, parent text, uid text, version integer, 
              modtime text, content text, checksum text)''')
            # files and collections only differ in that
            # checksum will be "None" for collections.
        self.serialiser=serialiser(self)   
        
    def updateFile(self,dataFile):
        ''' Update a data file instance in the index '''
        sdf=self.serialiser.serialise(dataFile)
        parent,df=os.path.split(dataFile.properties['path'])
        self._insert(dataFile.properties['path'],
                    parent,
                    dataFile.properties['modificationDate'],
                    sdf,
                    dataFile.properties['checksum'])
                    
    def updateCollection(self,collection):
        ''' Update collection in index '''
        sdf=self.serialiser.serialise(collection)
        self._insert(collection.properties['path'],
                    collection.properties['parent'],
                    collection.properties['modificationDate'],
                    sdf,
                    None)           
        
    def _insert(self,path,parent,modtime,content,checksum):
        ''' Insert document for a specific path. If it exists,
        increment the version number and replace. '''
        r=self.dbRecord(self._getby('path',path))
        if r.path is None:
            v=1
            u=str(uuid.uuid1())
            r=self.dbRecord([path,parent,u,v,modtime,content,checksum])
        else:
            #leave r.uid
            r.parent=parent
            r.version=r.version+1
            r.content=content
            r.modtime=modtime
            r.checksum=checksum
      
        self.cursor.execute(
            "INSERT INTO documents values (?,?,?,?,?,?,?)",tuple(r))
        self.conn.commit()
        return r.uid  
      
    def _delete(self,path):
        ''' Best be careful with this, all the versions gone,
        just like that '''
        cquery='DELETE from documents where path = ?'
        self.cursor.execute(cquery,(path,))     
        self.conn.commit()
        
    def _getall(self,query,value):
        ''' The issue to handle here is where we want multiple
        documents, but we don't want all the versions of all the 
        documents, and we want to exclude documents with a version
        zero.'''
        if value is None:
            self.cursor.execute(query)
        else: self.cursor.execute(query,value)
        results=self.cursor.fetchall()
        if results==[]: return []
        records=[self.dbRecord(r) for r in results]
        unique=[]
        # following depends on definition of equal in record
        # as not including version, and also depends on results
        # being ordered by version
        for i in range(len(records))[:-1]:
            if records[i]!=records[i+1]:
                unique.append(records[i])
        unique.append(records[-1])
        return unique
        
    def __getlatest(self,query,value,vwanted=None):
        ''' Issue query with value and return latest version '''
        self.cursor.execute(query,value)
        results=self.cursor.fetchall()
        if results == []:
            return []
        elif results[0][3]==0:
            if vwanted is None:
                raise ValueError('path [%s] has been deleted'%value[0])
            else: return results[0]
        else:
            return results[-1]  
        
    def _getby(self,key,value,vwanted=None):
        ''' Return a string given a particular type of key,value '''
       
        assert key in ('uid','path'),'Invalid key to database'
        k={'uid':'SELECT * FROM documents WHERE uid=? ORDER BY version',
           'path':'SELECT * FROM documents WHERE path=? ORDER BY version',}[key]
        if vwanted is None:
            v = ('%s'%value,)
        else:
            k.replace('ORDER by version','AND version=?')
            v = ('%s'%value,'%s'%vwanted,)
        return self.__getlatest(k,v,vwanted)
        
    def getFile(self,path):
        r=self.dbRecord(self._getby('path',path))
        #make sure we haven't got a collection by mistake:
        if r.path is None:
            return None
        else: 
            assert r.checksum != None,\
                'Woops, got a collection, wanted a file %s'%path
            return self.serialiser.deserialise(r.content)
        
    def getCollection(self,path):
        r=self.dbRecord(self._getby('path',path))
        #make sure we haven't got a file by mistake:
        if r.path is None:
            return None
        else: 
            assert r.checksum == None,\
                'Woops, got a file, wanted a collection %s'%path
            return self.serialiser.deserialise(r.content)
        
         
    def getSubCollectionsFor(self,path):
        ''' Get a set of subcollection paths for a given collection '''
        s= 'SELECT * FROM documents where parent = ? and checksum is null order by version'
        v=(path,)
        return [c.path for c in self._getall(s,v) if c.checksum is None]
        
    def getFilesFor(self,path):
        ''' Get the files in a given collection path '''
        s= 'SELECT * FROM documents where parent = ? order by version'
        v=(path,)
        return [c.path for c in self._getall(s,v) if c.checksum is not None]
        
    def needsUpdate(self,path):
        ''' Check to see if path on disk is newer than in index '''
        r=self.dbRecord(self._getby('path',path))
        if r.path is None: return True
        m=isomodtime(path)
        r=self.dbRecord(self._getby('path',path))
        n=r.modtime
        if m>n:
            return True
        else: return False
        
    def getChecksumFor(self,dataFilePath):
        ''' Get a file checksum out of the index '''
        r=self.dbRecord(self._getby('path',dataFilePath))
        print 'got ',r
        return r.checksum
        
    def validateIndex(self):
        ''' tests index for self consistency: are all data files in
        collections? Are all datafiles known by collections registered?
        Note that it is possible for a state of inconsistency to exist
        while transactions are underway. Validation only applies to
        latest versions '''
        #cquery="SELECT * FROM documents WHERE checksum is null"
        #fquery="SELECT * FROM documents Where checksum is not null"
        return NotImplementedError
        
    def getObjVersion(self,path):
        ''' Return the version for a specific document '''
        r=self.dbRecord(self._getby('path',path))
        return r.version
        
    def summary(self):
        ''' Produce a string to use as a printable summary '''
        records=self._getall(
                'SELECT * from documents where parent is null and checksum is null',None)
        return iter([i.path for i in records])
        
    def __str__(self):
        return 'Collections: %s'%list(self.summary())
        
    def __iter__(self):
        ''' Provides an iterative view of all collections '''
        records=self._getall(
                'SELECT * from documents where checksum is null',None)
        return iter([r.path for r in records])
        
        
class simpleSerialiser(object):
    ''' Provides a simple serialisation of the simple collections,
    as an exemplar. It's likely that this is only going to be
    used for demonstration. Real life will use a standard
    serialisation. '''
    def __init__(self,index):
    
        self.IknowAbout=['properties','contents'] # and lists and dictionaries
        self.options={'simpleTools.simpleCollection':simpleCollection,
                      'simpleTools.simpleDataFile':simpleDataFile}
        self.args={'simpleTools.simpleCollection':index,
                      'simpleTools.simpleDataFile':None}
                      
    def _toDict(self,o):
        ''' Takes a simple class and makes it look like a dicionary for serialisation '''
        klass=str(o.__class__)
        #do the easy ones first
        if klass in ["<type 'str'>","<type 'int'>","<type 'NoneType'>",
        "<type 'unicode'>","<type 'float'>"]:
            return o
        # then the construction ones
        if klass in ["<type 'dict'>","<type 'list'>"]:
            if klass=="<type 'dict'>":
                r={}
                for item in o: r[item]=self._toDict(o[item])
                return r
            else:
                r=[]
                for item in o: r.append(self._toDict(item))
                return r
        #now the stranger ones
        conversions={"<type 'numpy.int32'>":int,
                    "<type 'numpy.float32'>":float,
                    "<type 'numpy.float64'>":float}
        if klass in conversions: return conversions[klass](o)
        #now handle our classes
        myklass=str(o.__class__)[8:-2]
        if myklass not in self.options:
            raise ValueError(
                "Don't know how to serialise %s (value %s)"%(klass,o))
        result={myklass:{}}
        for item in self.IknowAbout:
            if hasattr(o,item):
                a=getattr(o,item)
                result[myklass][item]=self._toDict(a)
        return result
                      
    def serialise(self,o):
        ''' Serialise o by converting to something json can handle '''
        # should probably extend json, and add methods to objects ...
        serialDict=self._toDict(o)
        s=json.dumps(serialDict,indent=2)
        return s

    def deserialise(self,s):
        ''' Deserialise json'''
        r=json.loads(s)
        return self._undict(r)
        
    def _undict(self,o):
        ''' Given an object in dict format, see if it's one of our classes, and
        if so instantiate it properly via unpicking it '''
        klass=str(o.__class__)
        
        if klass=="<type 'dict'>":
            keys=o.keys()
            if len(keys)==1: 
                key=o.keys()[0]
                if key in self.options:
                    payload=o[key]
                    return self._unpick(key,payload)
        return o
        
    def _unpick(self,klass,payload):
        ''' Unpicks specific content '''
        obj=self.options[klass](self.args[klass])
        if 'properties' in payload:
            for k in payload['properties']:
                obj.modify(k,payload['properties'][k])
        if 'contents' in payload:
            for k in payload['contents']:
                for item in payload['contents'][k]:
                    obj.add(k,self._undict(item))
        return obj
                       

