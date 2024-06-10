from .DecisionNode import DecisionNode

class awsActivityRef(DecisionNode):
    activity = None 
    
    def __init__(self, parent=None, name=None,activity=None):
        super().__init__(parent=parent, name=None)
        self.activity=activity
    
    def __str__(self):
        return str(type(self))+" "+self.activity.name+" "+self.parent.name
