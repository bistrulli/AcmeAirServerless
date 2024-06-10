from .Activity import Activity


class Call(Activity):
    
    dest = None

    def __init__(self, dest, parent=None, name=None):
        super().__init__(dest, parent=parent, name=name)
        self.dest = dest
        self.dest.addCalling(self)
    
    def getConAct(self):
        raise NotImplementedError 
    
    def getActivities(self):
        return []
