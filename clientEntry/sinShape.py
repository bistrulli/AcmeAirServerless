from locust import  LoadTestShape
import subprocess
import math
import numpy as np
from matplotlib.backend_bases import DrawEvent

class StagesShapeWithCustomUsers(LoadTestShape):
    
    lastStage = None
    mod = 200
    shift = 10
    period = 1200 / (2*math.pi)
    
    def __init__(self):
        super().__init__()
        self.mod=100;
        self.shift = 10
        self.period = 1200 / (2*math.pi)
        self.users=(self.shift,1)

    def tick(self):
        run_time = self.get_run_time()
        if run_time <= 600:
            #self.updateCrtl(stage)
            if(int(run_time) % 30==0):
                self.users=(self.f(int(run_time)), 1)
            return self.users

        return None
    
    def f(self,x):
        return max(math.sin(x/self.period)*self.mod,0)+self.shift
    
    def updateCrtl(self, stage):
        if(stage != StagesShapeWithCustomUsers.lastStage):
            R = stage["Rep"]
            C = stage["Conc"]
            F = stage["functions"]
            for i in range(len(R)):
                ufile = open("../%s/update.sh" % (F[i]), "r")
                filestr = ufile.read()
                ufile.close()
                
                updatecmd=None
                
                if( StagesShapeWithCustomUsers.lastStage!=None and stage["users"]>StagesShapeWithCustomUsers.lastStage["users"] or StagesShapeWithCustomUsers.lastStage==None):
                    updatecmd = filestr.replace("$NT", "%d" % (C[i]))
                    updatecmd = updatecmd.replace("$REP_max", "%d" % (R[i]))
                    updatecmd = updatecmd.replace("$REP_min", "%d" % (R[i]))
                elif(stage["users"]<=StagesShapeWithCustomUsers.lastStage["users"]):
                    updatecmd = filestr.replace("$NT", "%d" % (C[i]))
                    updatecmd = updatecmd.replace("$REP_max", "%d" % (R[i]))
                    updatecmd = updatecmd.replace("$REP_min", "%d" % (0)) #nel caso scendono gli utenti faccio scendere il numero di isntanze in modo graduale
                    
                    
                
                ufile = open("../%s/update_cmd.sh" % (F[i]), "w+")
                filestr = ufile.write(updatecmd)
                ufile.close()
                
                subprocess.Popen(["sh", "../%s/update_cmd.sh" % (F[i])])
        
            StagesShapeWithCustomUsers.lastStage = stage