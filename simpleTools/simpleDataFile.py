import os
from simpleTools import isomodtime
class simpleDataFile(object):
    
    ''' A minimal implementation of the "A" metadata for a file object. 
    Can be subclassed to provide extended implementations. '''
    
    def __init__(self,handler=None,debug=True,fixer=None):
        ''' Initialise empty, and populate from index or from on disk.
        If populated by disk, need a handler, passed as a class
        definition. If populated by a serialiser, it should use the 
        modify and add methods rather than directly molesting properties 
        and contents.'''
        
        # file attributes (in the UML sense of attributes):
        self.properties={'modificationDate':None,'checksum':None,'name':'','path':'',
        'previousVersion':None,'history':None,'filesize':0,'input_file_format':'',
        'tracking_id':None,'notes':'','timeAxis':None}
        
        # these are the formal schema keys, users can overload properties by
        # adding key value pairs to the property dictionary, but we can always
        # recover the schema keys by using this keyset:
        self.schemakeys=self.properties.keys()
        
        # file contents (composed classes in the UML sense)
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
        path=os.path.abspath(path)
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
        self.modify('path',f)
        self.modify('modificationDate',isomodtime(path))
        self.modify('checksum',checksum)
        if self.debug: print 'finished creating from disk in simpleDataFile'
    
    def modify(self,key,value):
        if key in self.properties:
            self.properties[key]=value
        else:
            raise ValueError(
            '%s is not a pre-defined file property (try usermodify)'%key)
    def usermodify(self,key,value):
        ''' Used to add/modify user key,value attributes of the files
        (as opposed to the pre-defined attributes) '''
        self.properties[key]=value
    def add(self,key,value):
        self.contents[key].append(value)
    def __eq__(self,other):
        return self.properties==other.properties
    def __ne__(self,other):
        return not self==other
    def __repr__(self):
        return 'dataFile %s'%self.properties['path']
    def view(self,fmt='txt'):
        ''' Provides a pretty printed view of file contents.
            If fmt is 
                html, then it's an html view
                txt, then ia text view 
            '''
        assert fmt in ['txt','html']
        # start by grabbing all variables on the same grid
        vlist={}
        for g in self.contents['grids']:
            gname=g['name']
            vlist[gname]=[]
            for v in self.contents['variables']:
                if v['grid']==gname:
                    vlist[gname].append(v)
        #now write it all out
        if fmt=='txt':
            for g in vlist:
                print 'Grid %s'%g
                for v in vlist[g]:
                    print '    %s'%v['name']
        else:
            raise NotImplementedError('html format not supported yet')
        
