from entity.probChoice import probChoice
from entity.awsActivity import awsActivity


class Entry():
    '''
    classdocs
    '''
    
    name = None
    activities = None
    parentTask = None
    calling = None
    dNodes = None

    def __init__(self, name, activities=None, pTask=None,dNodes=None):
        self.name = name
        if(activities is not None):
            self.activities = activities
        else:
            self.activities = []
            
        if(dNodes is None):
            self.dNodes=[]
        else:
            self.dNodes=dNodes
        
        self.parentTask = pTask
        self.calling=[]
        
    
    def setTask(self, pTask):
        self.parentTask = pTask
    
    def getActivities(self):
        return self.activities
    
    def addCalling(self,a):
        if(a  not in self.calling):
            self.calling.append(a)
    
    def getDnodes(self):
        return self.dNodes
    
    def getNextNode(self,d=None):
        #ritorno il prossimo devision node da eseguire a partire da dnode
        nextD=None
        if(d is None):
            if len(self.dNodes)==0: # se la entry non ha un call graph associato
                nextD=probChoice(parent=self, name="%sAcq"%(self.name), probs=[1.0], branches=[self.activities[0]], origin=self)
                final=awsActivity(parent=self, name="%sAnsw"%(self.activities[0].name),activity=self.activities[0])
                self.dNodes.append(nextD)
                self.dNodes.append(final)
            else: 
                nextD=self.dNodes[0]
        else:
            idx=self.dNodes.index(d)
            if((len(self.dNodes)-1)-idx>0):
                nextD=self.dNodes[idx+1]
        
                
        return nextD
    
    def getDecNodeByCall(self,call):
        dNode=None
        for d in self.dNodes:
            if(d.origin==call):
                dNode=d 
        return dNode
        
        