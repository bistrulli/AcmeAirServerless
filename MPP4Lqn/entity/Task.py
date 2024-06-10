class Task(object):
    '''
    classdocs
    '''
    
    name = None
    tsize = None
    entries = None
    proc = None
    ref=None

    def __init__(self, name=None, tsize=None, entries=None, proc=None,ref=False):
        self.name = name
        self.tsize = tsize
        if(entries==None):
            self.entries = []
        else:
            self.entries = entries
        self.proc = proc
        self.ref=ref

    def addEntry(self,entry):
        entry.parentTask=self
        self.entries.append(entry)
    
    def getEntries(self):
        return self.entries
    
    def bindProc(self,proc):
        proc.bindTask(self)
        self.proc=proc