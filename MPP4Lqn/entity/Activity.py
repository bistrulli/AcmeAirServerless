from .Entry import Entry
import entity


class Activity():
    
    succ = None
    stime = None
    parentEntry = None
    visited = False
    name = None
    parent = None

    def __init__(self, stime=None, parent=None, name=None):
        self.stime = stime
        self.parent = parent
        self.succ = None
        self.name = name
    
    def addNext(self, succ):
        self.succ = succ
    
    def getNext(self):
        return self.succ
    
    def getConAct(self):
        return []
    
    def getActivities(self):
        return []
    
    def setPEntry(self, parentEntry):
        self.parentEntry = parentEntry
        
    def isVisited(self):
        return self.visited
    
    def getParentEntry(self):
        pEntry = self.parent
        while(not isinstance(pEntry, Entry)):
            pEntry = pEntry.getParentEntry()
            
        return pEntry
    
    def getParentTask(self):
        return self.getParentEntry().parentTask
    
    def getParent(self):
        return self.parent
    
    def prev(self):
        idx=self.getParent().getActivities().index(self)
        pAct=[]
        if(idx==0):
            if(self.getParentTask().ref):
                pAct.append(self.getParent().getActivities()[idx-1])
            else:
                if(not isinstance(self.getParent(),Entry)):
                    pAct.append(self.getParent())
        else:
            if(not isinstance(self,entity.actBlock)):
                pAct.append(self.getParent().getActivities()[idx-1])
            else:
                pAct.append(self.getParent())
        
        #se l'istruzione precedente e una scelta probabilistica devo tornare la lista
        #di tutte le ultime activity di tutti i blocchi
        if(len(pAct) >0 and isinstance(pAct[0],entity.probChoice) and pAct[0].getJoinAct()==self):
            pAct=[blk.getActivities()[-1] for blk in pAct[0].getActivities()]
            
        return pAct
        
