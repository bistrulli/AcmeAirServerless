import traceback
from entity import *
import numpy as np
import json
from jinja2 import Environment, PackageLoader, select_autoescape
from pathlib import Path
import sys
import entity
import os
import re
import copy

script_dir = Path(os.path.realpath(__file__))/".."/".."


def hilite(string, status, bold):
    attr = []
    if status:
        # green
        attr.append('32')
    else:
        # red
        attr.append('31')
    if bold:
        attr.append('1')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)


class Lqn2MPP():
    
    Jumps = None
    props = None
    names = None
    rates = None
    lqn = None
    mapState = None
    genJump = None
    genProp = None
    
    def __init__(self):
        self.Jumps = []
        self.props = []
        self.names = []
        self.mapState = False
        self.genJump = False
        self.genProp = False
        self.rates = {}
    
    def findAct(self, aname, parent, ename=None):
        a_tgt = None
        for a in parent.getActivities():
            if((ename == a.getParentEntry().name and a.name == aname) or (a.name == aname and ename is None) 
               or (ename == a.getParentEntry().name and aname == "a")):
                a_tgt = a
            else:
                if(isinstance(a, Call)):
                    a_tgt = self.findAct(aname, a.dest, ename)
                else:
                    a_tgt = self.findAct(aname, a, ename)
            if(a_tgt is not None):
                break
            
        return a_tgt
    
    # mapp ogni activity nell'opportuno stato
    # la filosofia e di fare una visita in profondita
    # a seconda del tipo di activity recupero la prossima activity da visitare
    def mapStateName(self, act):
        # print("activity:" + act.name, "Entry:" + act.getParentEntry().name,
        #       "Task:" + act.getParentTask().name)
        
        # se e' la prima activity della sua parentEntry aggiunfo l'activity che mi rappresenta 
        # le variabili in coda di acquisizione in una data entry
        if(act.getParentEntry().getActivities()[0] == act and not act.getParentTask().ref):
            if("X%s_a" % (act.getParentEntry().name) not in self.names):
                self.names.append("X%s_a" % (act.getParentEntry().name))
        
        if("X%s_%s" % (act.getParentEntry().name, act.name) not in self.names):
            self.names.append("X%s_%s" % (act.getParentEntry().name, act.name))
            
        if(isinstance(act, Call)):
            for a in act.dest.getActivities():
                self.mapStateName(a)
        elif(isinstance(act, probChoice)):
            for a in act.getActivities():
                self.mapStateName(a)
        elif(isinstance(act, actBlock)):
            #print(act.name,len(act.getActivities()))
            for a in act.getActivities():
                #print("\t"+a.name,a.dest.name,a.getParentEntry().name)
                self.mapStateName(a)
    
    def createJump(self, sndName, lrcvName, rrcvName, rsyncName):
        
        #print(sndName,lrcvName,rrcvName,rsyncName)
        
        jump = [0 for i in range(len(self.names))]
        
        if(sndName is not None):
            if(type(sndName) is list):
                for snd in sndName:
                    jump[self.names.index(snd)] = -1
            else:
                jump[self.names.index(sndName)] = -1
        
        if(lrcvName is not None):
            if(type(lrcvName) is list):
                for lrcv in lrcvName:
                    jump[self.names.index(lrcv)] = 1
            else:
                jump[self.names.index(lrcvName)] = 1
        
        if(rrcvName is not None):
            if(type(rrcvName) is list):
                for rrcv in rrcvName:
                    jump[self.names.index(rrcv)] = +1
            else:
                jump[self.names.index(rrcvName)] = +1
        
        if(rsyncName is not None):
            if(type(rsyncName) is list):
                for rsync in rsyncName:
                    jump[self.names.index(rsync)] = -1
            else:
                jump[self.names.index(rsyncName)] = -1
        
        #verifico che il jump non esiste gia nella matrice
        if(jump not in self.Jumps):
            self.Jumps.append(jump)
    
    def createPropensity(self, jump):
        # per semplicita cerco di determinare la propensita a partire dal jump
        # e le assunzione che ho fatto sul modello
        frm = []
        to = []
        for i in range(len(jump)):
            if(jump[i] != 0):
                # parto sempre dall'unica entry del client task
                #act = self.findAct(aname, self.lqn["task"][0].getEntries()[0], ename)
                if(jump[i] > 0):
                    to.append(self.names[i])
                else:
                    frm.append(self.names[i])
        
        print(",".join(frm),"->",",".join(to))
        
        syncall=None
        asyncall=None
        for f in frm:
            ename=f.split("_")[0][1:]
            aname=f.split("_")[1]
            act = self.findAct(aname, self.lqn["task"][0].getEntries()[0], ename)
            if(isinstance(act,SynchCall)):
                syncall=act
                break
            elif(isinstance(act,AsynchCall)):
                asyncall=act
                break
        
        for f in frm:
            act=None
            ename=f.split("_")[0][1:]
            aname=f.split("_")[1]
            if(f.endswith("_a")):
                #caso in cui vengo da un acquire (in questo caso posso andare solo in un'azione locale)
                act = self.findAct(aname, self.lqn["task"][0].getEntries()[0], ename)
                
                #recupero tutti gli statia che contribuiscono all'occupazione di un thread, fondamentalmente gli devo sottrarre tutte le activity che
                #rappresentano chiamte asincrone
                syncActivity=["X%s_%s" % (a.getParentEntry().name, a.name) for e in act.getParentTask().getEntries() for a in e.getAllActivities() if(not type(a)==AsynchCall)]
                
                # TBD propensity delle reazioni che si sincronizzano con un thread libero#
                prop = "X%s_a/(%s)" % (act.getParentEntry().name,
                                        "+".join(["X%s_a" % (e.name) for e in act.getParentTask().getEntries()]))
                prop += "*D*min(%s,NT[\"%s\"]-(%s))" % ("+".join(["X%s_a" % (e.name) for e in act.getParentTask().getEntries()]),
                                       act.getParentTask().name,
                                       "+".join(syncActivity))
                self.props.append(prop)
                break
            else:
                #caso in cui vengo da una qualsiasi altra istruzione
                #devo distinguere due casi
                #il caso di una scelta probabilistica
                #   probChoice->actBlock
                #   actBlock->activity
                act  = self.findAct(aname, self.lqn["task"][0].getEntries()[0], ename)
                prop="-"
                #per sicurezza dovrei analizzare queste condizioni sull'intero jump e non solo sul primo che incontro anche se cosi 
                #dovrebbe funzionare per via dell'ordinamento che la visita in profondita da agli stati della CRN
                if(isinstance(act,probChoice)):
                    act1 = self.findAct(to[0].split("_")[1], self.lqn["task"][0].getEntries()[0], to[0].split("_")[0][1:])  
                    prop="D*X%s_%s*%s"%(act.getParentEntry().name,act.name,act.probs[act.getActivities().index(act1)])
                elif(isinstance(act,actBlock)):
                    prop="D*X%s_%s"%(act.getParentEntry().name,act.name)
                #elif(isinstance(act,SynchCall)):
                elif(syncall is not None):
                    #prop=hilite("SynchCall", False, True)
                    act=syncall
                    J = np.matrix(self.Jumps)
                    #recupero la enty destizaione di questa chimata
                    inIdx = np.where(J[:, self.names.index("X%s_a" % act.dest.name)] == 1)
        
                    #vado alla ricerca di tutte le activity  (synchCall) che si sono sincronizzate con questa entry
                    callingAct = []
                    for idx in inIdx[0]:
                        for n in np.where(J[idx,:] == 1)[1].tolist():
                            a = self.findAct(aname=self.names[n].split("_")[-1],parent=self.lqn["task"][0].getEntries()[0])
                            if(isinstance(a, Call) and a.dest.name==act.dest.name):
                                callingAct.append("X%s_%s" % (a.getParentEntry().name, a.name))
        
                    sndName="X%s_%s" %(act.getParentEntry().name,act.name)
                    rsyncName=None
                    synA=None
                    for rsyncName in frm:
                        synA=self.findAct(aname=rsyncName.split("_")[1],parent=self.lqn["task"][0].getEntries()[0],ename=rsyncName.split("_")[0][1:])
                        if(isinstance(synA,entity.Call) or isinstance(synA,entity.probChoice) or 
                           isinstance(synA,entity.actBlock)):
                            continue
                        else:
                            break
        
                    #print(jump)
                    #print("cc",rsyncName,synA.getParentTask().name)
        
        
                    prop = "%s/(%s)*%s/(%s)*min(%s,NC[\"%s\"])*MU[\"%s\"]" % (sndName,
                                                                "+".join(callingAct),
                                                                rsyncName,
                                                                "+".join(["X%s_e" % (e.name) for e  in synA.getParentTask().entries]),
                                                                "+".join(["X%s_e" % (e.name) for e  in synA.getParentTask().entries]),
                                                                synA.getParentTask().name
                                                                , rsyncName)
                elif(asyncall is not None):
                    #prop=hilite("SynchCall", False, True)
                    act=asyncall
                    J = np.matrix(self.Jumps)
                    
                    #recupero la entry destizaione di questa chimata
                    inIdx = np.where(J[:, self.names.index("X%s_a" % act.dest.name)] == 1) 
                    
                    #print("###",act.dest.name,inIdx[0],inIdx[1])
        
                    #vado alla ricerca di tutte le activity (Call) che si sono sincronizzate con questa entry
                    callingAct = []
                    for idx in inIdx[0]:
                        for n in np.where(J[idx,:] == 1)[1].tolist():
                            a = self.findAct(aname=self.names[n].split("_")[-1],parent=self.lqn["task"][0].getEntries()[0])
                            if(isinstance(a, Call) and a.dest.name==act.dest.name):
                                #print("####","X%s_%s" % (a.getParentEntry().name, a.name))
                                callingAct.append("X%s_%s" % (a.getParentEntry().name, a.name))
        
                    sndName="X%s_%s" %(act.getParentEntry().name,act.name)
                    rsyncName=None
                    synA=None
                    for rsyncName in frm:
                        synA=self.findAct(aname=rsyncName.split("_")[1],parent=self.lqn["task"][0].getEntries()[0],ename=rsyncName.split("_")[0][1:])
                        if(isinstance(synA,entity.Call) or isinstance(synA,entity.probChoice) or 
                           isinstance(synA,entity.actBlock)):
                            continue
                        else:
                            break
                        
                    #print("####",a,rsyncName)
        
                    #print("##",callingAct)
                    prop = "%s/(%s)*%s/(%s)*min(%s,NC[\"%s\"])*MU[\"%s\"]" % (sndName,
                                                                "+".join(callingAct),
                                                                rsyncName,
                                                                "+".join(["X%s_e" % (e.name) for e  in synA.getParentTask().entries]),
                                                                "+".join(["X%s_e" % (e.name) for e  in synA.getParentTask().entries]),
                                                                synA.getParentTask().name
                                                                , rsyncName)
        
                elif(isinstance(act,entity.Activity)):
                    #if(not act.getParentTask().ref):
                        #raise ValueError("Problem with the model, there is an activity that is not part of the client")
        
                    #devo implementare il gps per tutte le actiity
                    if(act.getParentTask().ref):
                        prop = "MU[\"X%s_%s\"]*X%s_%s" % (act.getParentEntry().name, act.name,
                                                  act.getParentEntry().name, act.name)
                    else:
                        #devo trovare tutte le activity della stessa entry
                        gpsAct=["X%s_%s" %(gps_i.getParentEntry().name,gps_i.name) for gps_i in act.getParentEntry().getAllActivities() if(type(gps_i)==Activity)]
        
                        actName="X%s_%s"%(act.getParentEntry().name,act.name)
        
                        prop = "%s/(%s)*min(%s,NC[\"%s\"])*MU[\"%s\"]"%(actName,
                                                                        "+".join(gpsAct),
                                                                        "+".join(gpsAct),
                                                                        act.getParentTask().name,
                                                                        actName)
        
        
                self.props.append(prop)    
                break         
    
    def mapJump(self, act):
        # print("activity:"+act.name, "Entry:"+act.getParentEntry().name, 
        #       "Task:"+act.getParentTask().name,"Type:"+str(type(act)))
        
        # GUARDO L'ISTRUZIONE PRECEDENTE (SICCOME NON HO L'ACQUIRE ESPLICITO L'ISTRUZIONE PRECEDENTE e per forza locale)
        
        #il problema che vedo di questo approccio e' che ci potrebbero essere actibity che influenzano piu di unn stato comtemporaneamente
        idx = act.getParent().getActivities().index(act) #indice di questa activity all'interno della entry padre
        sndName = []  # id dello stato locale da cui sottrarre (instruzione precedente)
        lrcvName = []  # id dello stato da locale a cui aggiungere (istruzione successiva)
        rrcvName = []  # id dello stato remoto a cui aggiungere (istruzione eseguita sul server remoto)
        rsyncName = []  # id dello stato remoto con cui mi sincronizzo (istruzione con cui mi sincronizzo)
        
        prvact = act.prev()
        
        if(len(prvact)>0 and isinstance(prvact[0], AsynchCall)):
            #faccio scattare la transizione della chiamata asincrona e quindi la metto come sender
            sndName.append("X%s_%s" % (act.prev()[0].dest.name, "e"))
        else:
            lrcvName.append("X%s_%s" % (act.getParentEntry().name, act.name))
        
        #print("---",act.name,lrcvName,act.prev())
        
        if(len(prvact) > 1):
            #questo succede nel caso della sceta probabilistica
            #print(act.getParentEntry().name,prvact)
            # il caso in cui il numero di azioni senders e maggiore di uno
            for a in prvact:
                #qui devo creare jump diversi
                sndName2 = []  
                rrcvName2 = [] 
                rsyncName2 = []
                lrcvName2 = []
                
                if(isinstance(a, AsynchCall)):
                    #faccio scattare la transizione della chiamata asincrona e quindi la metto come sender
                    sndName2.append("X%s_%s" % (act.prev()[0].dest.name, "e"))
                else:
                    lrcvName2.append("X%s_%s" % (act.getParentEntry().name, act.name))
                
                #sndName2.append("X%s_%s" % (a.getParentEntry().name, a.name))
    
                if(isinstance(act, Call)):
                    rrcvName2.append("X%s_a" % (act.dest.name))
                if(isinstance(a, SynchCall)):
                    sndName2.append("X%s_%s" % (a.getParentEntry().name, a.name))
                    rsyncName2.append("X%s_e" % (a.dest.name))
                if(isinstance(a, AsynchCall)):
                    sndName2.append("X%s_%s" % (a.getParentEntry().name, a.name))
                    sndName2.append("X%s_%s" % (a.dest.name, "e"))#invece di e dovrei prendere l'ultima activity della entry
                if(isinstance(a, Activity)):
                    sndName2.append("X%s_%s" % (a.getParentEntry().name, a.name))
                    
                
                #print(sndName2,lrcvName2,rrcvName2,rsyncName2)
                self.createJump(sndName2, lrcvName2, rrcvName2, rsyncName2)
                
        else:
            if(len(prvact) == 1):
                sndName.append("X%s_%s" % (prvact[0].getParentEntry().name, prvact[0].name))
            else:
                sndName.append("X%s_a" % ((act.getParentEntry().name)))
            
            if(isinstance(act, Call)):
                if(isinstance(act, SynchCall)):
                    rrcvName.append("X%s_a" % (act.dest.name))
                else:
                    #nel caso in cui la chimata e' asincrona potrei avere piu rrcv
                    act_tmp=act
                    #print(act_tmp.name)
                    while(isinstance(act_tmp, AsynchCall) and not (len(prvact) > 0 and type(prvact[0]==AsynchCall)) ): #non vado in profondita se sono stato chiamato da una asynch call
                        rrcvName.append("X%s_a" % (act_tmp.dest.name)) # se e' una chiamata sicuramente finisco in una coda di acquire
                       
                        nextAct=None
                        if(len(act_tmp.getParent().getActivities())>idx+1):
                            nextAct=act_tmp.getParent().getActivities()[idx+1]
                            idx+=1
                        else:
                            if(isinstance(act_tmp.getParent(),actBlock)): #caso in cui l'activity e l'ultima del suo blocco
                                nextAct=act_tmp.getParent().getParent().getJoinAct()#posso usare uno stesso schema anche per il forkjoin
                            
                        #print("---",act.getParentEntry().name,act.getParent().getActivities(),idx)
                        if("X%s_%s"%(act_tmp.getParentEntry().name,nextAct.name) not in lrcvName):
                            lrcvName.append("X%s_%s"%(act_tmp.getParentEntry().name,nextAct.name))
                        
                        #print("####",act_tmp.name,nextAct.name)
                        if(act_tmp==nextAct):
                            break
                        else:
                            act_tmp=nextAct
                    
            if(len(prvact) == 1 and isinstance(prvact[0], SynchCall)):
                rsyncName.append("X%s_e" % (prvact[0].dest.name))
            
            #print(sndName,lrcvName,rrcvName,rsyncName,act.name,type(act),prvact)
            self.createJump(sndName, lrcvName, rrcvName, rsyncName)
            
        if(isinstance(act, SynchCall)):
            for a in act.dest.getActivities():
                self.mapJump(a)
        elif(isinstance(act, AsynchCall)):
            for a in act.dest.getActivities():
                self.mapJump(a)
        elif(isinstance(act, probChoice)):
            for a in act.getActivities():
                self.mapJump(a)
        elif(isinstance(act, actBlock)):
            for a in act.getActivities():
                self.mapJump(a)
                
    def mapProp(self):
        for j in self.Jumps:
            self.createPropensity(j)
        
    def getCrn(self, lqn):
        self.lqn = lqn
        try:
            #assumo che il primo task sia quello dei client
            ref = self.lqn["task"][0].getEntries()[0]
            for a in ref.getActivities():
                self.mapStateName(a)
            
            for a in ref.getActivities():
                self.mapJump(a)
            
            self.mapProp()
            
            
        except:
            traceback.print_exc()
    
    def dumpToFile(self):
        crn = {"Jump":self.Jumps, "Prop":self.props, "State":self.names}
        y = json.dumps(crn)
        print(y)
    
    def toMatlab(self, outDir=None):
        if(outDir == None):
            outDir = "../model"
                
            
        env = Environment(
            loader=PackageLoader('trasducer', 'templates'),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=False,
            lstrip_blocks=False)
        
        tname = [t.name for t in self.lqn["task"]]
        
        probChoices=[a for t in self.lqn["task"] for e in t.getEntries() for a in e.getAllActivities() if(type(a)==probChoice)];
        
        mprops = []
        for p in self.props:
            np = p
            for tn in tname:
                np = np.replace("NC[\"%s\"]" % (tn), "p.NC(%d)" % (tname.index(tn) + 1))
                np = np.replace("NT[\"%s\"]" % (tn), "p.NT(%d)" % (tname.index(tn) + 1))
            for vname in self.names:
                np = np.replace("MU[\"%s\"]" % (vname), "p.MU(%d)" % (self.names.index(vname) + 1))
            for vname in self.names:
                np = np.replace(vname, "X(%d)" % (self.names.index(vname) + 1))
            for choice in probChoices:
                for p in choice.probs:
                    np = np.replace(p, "p.%s" % (p))
            np = np.replace("D", "p.delta")
            mprops.append(np)
        
        mat_tmpl = env.get_template('model-tpl.m')
        model = mat_tmpl.render(task=self.lqn["task"], name=self.lqn["name"],
              names=self.names, props=mprops, jumps=self.Jumps,choices=probChoices)
        
        outd = Path(outDir)
        outd = outd / self.lqn["name"]
        outd.mkdir(parents=True, exist_ok=True)
        
        mfid = open("%s/lqn.m" % str(outd.absolute()), "w+")
        mfid.write(model)
        mfid.close()
        
        #++export ODE
        mat_tmpl = env.get_template('modelODE-tpl.m')
        model = mat_tmpl.render(task=self.lqn["task"], name=self.lqn["name"],
              names=self.names, props=mprops, jumps=self.Jumps,choices=probChoices)
        
        outd = Path(outDir)
        outd = outd / self.lqn["name"]
        outd.mkdir(parents=True, exist_ok=True)
        
        mfid = open("%s/lqnODE.m" % str(outd.absolute()), "w+")
        mfid.write(model)
        mfid.close()
        
        #matmain 
        mat_min_tmpl = env.get_template('model-main-tpl.m')
        model = mat_min_tmpl.render(task=self.lqn["task"], name=self.lqn["name"],
              names=self.names, props=mprops, jumps=self.Jumps,choices=probChoices)
        
        outd = Path(outDir)
        outd = outd / self.lqn["name"]
        outd.mkdir(parents=True, exist_ok=True)
        
        mfid = open("%s/main.m" % str(outd.absolute()), "w+")
        mfid.write(model)
        mfid.close()
        
    
    def toPython(self, outDir=None):
        if(outDir == None):
            outDir = "../model"
            
        env = Environment(
            loader=PackageLoader('trasducer', 'templates'),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=False,
            lstrip_blocks=False)
        
        tname = [t.name for t in self.lqn["task"]]
        
        mprops = []
        for p in self.props:
            np = p
            for tn in tname:
                np = np.replace("NC[\"%s\"]" % (tn), "p[\"NC\"][0,%d]" % (tname.index(tn)))
                np = np.replace("NT[\"%s\"]" % (tn), "p[\"NT\"][0,%d]" % (tname.index(tn)))
                np = np.replace("min(", "np.minimum(")
                np = np.replace("D", "p[\"delta\"]")
            for vname in self.names:
                np = np.replace("MU[\"%s\"]" % (vname), "p[\"MU\"][0,%d]" % (self.names.index(vname)))
            for vname in self.names:
                np = np.replace(vname, "X[%d]" % (self.names.index(vname)))
            mprops.append(np)
        
        mat_tmpl = env.get_template('pyCRN-tpl.py')
        model = mat_tmpl.render(task=self.lqn["task"], name=self.lqn["name"],
              names=self.names, props=mprops, jumps=self.Jumps)
        
        outd = Path(outDir)
        outd = outd / self.lqn["name"]
        outd.mkdir(parents=True, exist_ok=True)
        mfid = open("%s/lqn.py" % str(outd.absolute()), "w+")
        mfid.write(model)
        mfid.close()
        
        mfid = open("%s/__init__.py" % str(outd.absolute()), "w+")
        mfid.write("from .lqn import *\n")
        mfid.close()
        
    def toCasadiCtrl(self, outDir=None):
        if(outDir == None):
            outDir = "."
            
        env = Environment(
            loader=PackageLoader('trasducer', 'templates'),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=False,
            lstrip_blocks=False)
        
        tname = [t.name for t in self.lqn["task"]]
        
        mprops = []
        for p in self.props:
            np = p
            for tn in tname:
                np = np.replace("NC[\"%s\"]" % (tn), "NC[0,%d]" % (tname.index(tn)))
                np = np.replace("NT[\"%s\"]" % (tn), "NT[0,%d]" % (tname.index(tn)))
            for vname in self.names:
                np = np.replace("MU[\"%s\"]" % (vname), "MU[0,%d]" % (self.names.index(vname)))
            for vname in self.names:
                np = np.replace(vname, "X[%d]" % (self.names.index(vname)))
            np = np.replace("*min(", "*casadi.fmin(")
            if("D" in np):
                np = np.replace("D", "F*delta")
            else:
                np="(1-F)*%s"%(np)
            mprops.append(np)
        
        mat_tmpl = env.get_template('casadiCtrl-tpl.py')
        model = mat_tmpl.render(task=self.lqn["task"], name=self.lqn["name"],
              names=self.names, props=mprops, jumps=self.Jumps)
        
        outd = Path(outDir)
        outd = outd / self.lqn["name"]
        outd.mkdir(parents=True, exist_ok=True)
        mfid = open("%s/lqnCtrl.py" % str(outd.absolute()), "w+")
        mfid.write(model)
        mfid.close()
        
        mfid = open("%s/__init__.py" % str(outd.absolute()), "w+")
        mfid.write("from .lqnCtrl import *\n")
        mfid.close()
        
    def toJuliaCtrl(self,outDir=None):
        
        if(outDir == None):
            outDir = "."
            
        env = Environment(
            loader=PackageLoader('trasducer', 'templates'),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=False,
            lstrip_blocks=False)
        
        print(self.names)
        
        #creo il controllore con le assunzioni per velocizzare l'ottimizazione
        #riformulo la matricedei jump
        cJumps=self.Jumps.copy()
        cProp=self.props.copy()
        for idx,val in enumerate(self.Jumps):
            p=self.props[idx]
            res=re.search(r"D", p, re.MULTILINE)
            if(res is not None):
                #print("infinite jump")
                fromIdx=np.where(np.array(val)==-1)
                toIdx=np.where(np.array(val)==1)
                for i in toIdx[0]:
                    if("_e" in self.names[i]):
                        #da qui devo risalire a ritroso e fare il merge dei jump
                        print("from",[self.names[i] for i in fromIdx[0]],"to",[self.names[i] for i in toIdx[0]])
                        #toSum=[idx]+np.where(np.array(self.Jumps)[:,fromIdx[0]]==1)[0].tolist()
                        for inState in np.where(np.array(self.Jumps)[:,fromIdx[0]]==1)[0].tolist():
                            toSum=[idx,inState]
                            toSum+=self._mergeInfJumps([inState])
                            print(toSum)
                            
                            #sommo le righe individuate e le elimino dalla matrice
                            #aggiorno anche le propensity
                            nProp=None
                            for j in toSum:
                                try:
                                    if self.Jumps[j] in cJumps:
                                        cJumps.remove(self.Jumps[j])
                                        
                                    #elimino la vecchia propensity   
                                    if(self.props[j] in cProp): 
                                        cProp.remove(self.props[j])
                                        
                                    #massaggio la nuova propensity
                                    pToRmv=self.props[j]
                                    isInfpToRmv=re.search(r"D",pToRmv, re.MULTILINE)
                                    if(isInfpToRmv is not None):
                                        probMatches = re.finditer(r"(P_[a-zA-Z]+)",pToRmv, re.MULTILINE | re.UNICODE)
                                        for matchNum, match in enumerate(probMatches, start=1):
                                            if(nProp is not None):
                                                nProp="%s*%s"%(match.group(),nProp)
                                            else:
                                                nProp=match.group()
                                    else:
                                        if(nProp is not None):
                                            nProp="%s*%s"%(self.props[j],nProp)
                                        else:
                                            nProp=self.props[j]
                                    
                                except:
                                    traceback.print_exc()
                                    raise ValueError()
            
                            cJumps.append(np.array(self.Jumps)[toSum,:].sum(axis=0).tolist())
                            cProp.append(nProp)
                            
            
        print(np.array(cJumps))
        
        tname = [t.name for t in self.lqn["task"]]
        mprops = []
        for p in cProp:
            npr = p
            for tn in tname:
                npr = npr.replace("NC[\"%s\"]" % (tn), "NC[%d]" % (tname.index(tn) + 1))
                npr = npr.replace("NT[\"%s\"]" % (tn), "NT[%d]" % (tname.index(tn) + 1))
            for vname in self.names:
                npr = npr.replace("MU[\"%s\"]" % (vname), "MU[%d]" % (self.names.index(vname) + 1))
            for vname in self.names:
                npr = npr.replace(vname, "X[%d-sum(toZero[1,1:%d])]" % (self.names.index(vname) + 1,self.names.index(vname) + 1))
            npr = npr.replace("D", "p.delta")
            mprops.append(npr)
        
        for p in mprops:
            print(p)
    
    def _mergeInfJumps(self,fromJ):  
        for idx in fromJ:
            toSum=[]
            #chiamo la ricorsione se serve
            p=self.props[idx]
            res=re.search(r"D", p, re.MULTILINE)
            if(res is not None and idx!=0):
                fromIdx=np.where(np.array(self.Jumps[idx])==-1) 
                toIdx=np.where(np.array(self.Jumps[idx])==1)
                for inState in np.where(np.array(self.Jumps)[:,fromIdx[0]]==1)[0].tolist():
                    toSum=[inState]
                    toSum+=self._mergeInfJumps([inState])
        return toSum
    
    def toLqns(self, outDir=None,LQN=None):
        if(outDir == None):
            outDir = "../model"
                
            
        env = Environment(
            loader=PackageLoader('trasducer', 'templates'),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=False)
        
        tname = [t.name for t in LQN["task"]]
        
        lqns_tmpl = env.get_template('model-tpl.lqn')
        model = lqns_tmpl.render(task=LQN["task"], name=LQN["name"],names=self.names)
        
        outd = Path(outDir)
        outd = outd / LQN["name"]
        outd.mkdir(parents=True, exist_ok=True)
        
        mfid = open("%s/model.lqn" % str(outd.absolute()), "w+")
        mfid.write(model)
        mfid.close()
