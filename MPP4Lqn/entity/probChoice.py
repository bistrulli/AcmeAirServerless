from .DecisionNode import DecisionNode

class probChoice(DecisionNode):
    probs = None 
    branches = None
    origin = None
    
    def __init__(self, parent=None, name=None, probs=None,origin=None ,branches=None):
        super().__init__(parent=parent, name=name)
        if(branches is None):
            self.branches = []
        else:
            self.branches=branches
        if(probs is None):
            self.probs = []
        else:
            self.probs= probs
            
        self.origin=origin
    
    def getBranches(self):
        return self.branches
    
    def __str__(self):
        strRep="";
        for i in range(len(self.probs)):
            strRep+="%s-%s->%s"%(self.probs[i],self.origin.name,self.branches[i].name)
        
        return strRep
