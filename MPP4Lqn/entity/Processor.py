
class Processor():

    mult=None
    bTaks=None
    name=None
    sched=None

    def __init__(self, mult=None,name=name,sched=sched):
        self.mult=mult
        self.bTaks=[]
        self.name=name
        self.sched=sched
    
    def bindTask(self,task=None):
        self.bTaks.append(task)