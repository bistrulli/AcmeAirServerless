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
from multipledispatch import dispatch

script_dir = Path(os.path.realpath(__file__))/".."/".."


#l'idea e di fare un mapping per tipo:
#---> per ogni tipo creo gli stati necessari
#---> creo i jump
#---> creo le propensity
# la differenza rispetto alla precedente implementazione e' che parto sempre dalla lqn, e di volta in volta uso informazioni di basso livello

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
    states = None
    rates = None
    lqn = None
    mapState = None
    genJump = None
    genProp = None
    
    def __init__(self):
        self.Jumps = []
        self.props = []
        self.states = []
        self.mapState = False
        self.genJump = False
        self.genProp = False
        self.rates = {}
        
    def getMPP(self,lqn=None):
        self.lqn = lqn
        
        for t in self.lqn["tasks"]:
            self.mapName(t)
        
        for t in self.lqn["tasks"]:
            self.getJumps(t)
            
    
    def toMatlab(self, outDir=None):
        if(outDir == None):
            outDir = "../model"
                
            
        env = Environment(
            loader=PackageLoader('trasducer', 'templates'),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=False,
            lstrip_blocks=False)
        
        tname = [t.name for t in self.lqn["tasks"]]
        
        probChoices=[d for t in self.lqn["tasks"] for e in t.getEntries() for d in e.getDnodes() if(type(d)==probChoice)];
        
        mprops = []
        for p in self.props:
            np = p
            for tn in tname:
                #devo sostituire replcace con 
                
                
                np = re.sub(r"\bNC\[%s\]\B"%(re.escape(tn)),"p.NC(%d)" % (tname.index(tn) + 1),np)
                np = re.sub(r"\bNT\[%s\]\B"%(re.escape(tn)),"p.NT(%d)" % (tname.index(tn) + 1),np)
                #np = np.replace("NC[%s]" % (tn), "p.NC(%d)" % (tname.index(tn) + 1))
                #np = np.replace("NT[%s]" % (tn), "p.NT(%d)" % (tname.index(tn) + 1))
                
            for vname in self.states:
                #np = np.replace("MU[%s]" % (vname), "p.MU(%d)" % (self.states.index(vname) + 1))
                np = re.sub(r"\bMU\[%s\]\B"%(re.escape(vname)),"p.MU(%d)" % (self.states.index(vname) + 1),np)
            for vname in self.states:
                #np = np.replace(vname, "X(%d)" % (self.states.index(vname) + 1))
                np = re.sub(r"\b%s\b"%(re.escape(vname)),"X(%d)" % (self.states.index(vname) + 1),np)
            for choice in probChoices:
                for p in choice.probs:
                    #np = np.replace(p, "p.%s" % (p))
                    np = re.sub(r"\b%s\b"%(re.escape(p)),"p.%s" % (p),np)
            #np = np.replace("Δ", "p.delta")
            np = re.sub(r"\bΔ\b","p.delta",np)
            mprops.append(np)
        
        mat_tmpl = env.get_template('model-tpl.m')
        model = mat_tmpl.render(task=self.lqn["tasks"], name=self.lqn["name"],
              names=self.states, props=mprops, jumps=self.Jumps,choices=probChoices)
        
        outd = Path(outDir)
        outd = outd / self.lqn["name"]
        outd.mkdir(parents=True, exist_ok=True)
        
        mfid = open("%s/lqn.m" % str(outd.absolute()), "w+")
        mfid.write(model)
        mfid.close()
        
        #++export ODE
        mat_tmpl = env.get_template('modelODE-tpl.m')
        model = mat_tmpl.render(task=self.lqn["tasks"], name=self.lqn["name"],
              names=self.states, props=mprops, jumps=self.Jumps,choices=probChoices)
        
        outd = Path(outDir)
        outd = outd / self.lqn["name"]
        outd.mkdir(parents=True, exist_ok=True)
        
        mfid = open("%s/lqnODE.m" % str(outd.absolute()), "w+")
        mfid.write(model)
        mfid.close()
        
        #matmain 
        mat_min_tmpl = env.get_template('model-main-tpl.m')
        model = mat_min_tmpl.render(task=self.lqn["tasks"], name=self.lqn["name"],
              names=self.states, props=mprops, jumps=self.Jumps,choices=probChoices)
        
        outd = Path(outDir)
        outd = outd / self.lqn["name"]
        outd.mkdir(parents=True, exist_ok=True)
        
        mfid = open("%s/main.m" % str(outd.absolute()), "w+")
        mfid.write(model)
        mfid.close()
    
    
    @dispatch(Task)
    def mapName(self,task):
        #print("mapping task %s"%(task.name))
        for e in task.getEntries():
            self.mapName(e)
        
    @dispatch(Entry)
    def mapName(self,e):
        #per mappare una entry seguo i suoi devision node
        #print("\t mapping entry %s"%(e.name))
        #creo un coda di acquire per ogni entry
        if(not e.parentTask.ref):
            self.states.append("X%s_a"%(e.name))
        for a in e.getActivities():
            self.mapName(a)
        
        for d in e.dNodes:
            if(type(d)==awsActivity):
                self.mapName(d)
    
    @dispatch(Activity)
    def mapName(self,act):
        #per ogni activity costruisco uno stato che traccia il numero di job in esecuzione
        #print("\t\t mapping activity %s"%(act.name))
        self.states.append("X%s_%s"%(act.getParentEntry().name,act.name))
    
    @dispatch(awsActivity)
    def mapName(self,act):
        if(not act.parent.parentTask.ref):
            for inCall in act.activity.parent.calling:
                if(type(inCall)==SynchCall and "X%s_%s"%(act.activity.parent.name,inCall.name) not in self.states):
                    self.states.append("X%s_%s"%(act.activity.parent.name,inCall.name))
        
    
    @dispatch(probChoice)
    def mapName(self,choice):
        #print("\t\t mapping prob choice %s"%(choice.name))
        pass
    
    @dispatch(SynchCall)
    #per ogni chiamata traccio il numero di chiamate da evadere
    def mapName(self,scall):
        self.states.append("X%s_%s"%(scall.getParentEntry().name,scall.name))
        #print("\t\t mapping SynchCall %s"%(scall.name))
    
    @dispatch(AsynchCall)
    #per una chiamata asincrona traccio anche il numero di job in piu sulla entry chiamante (di fatto un fork)
    def mapName(self,ascall):
        self.states.append("X%s_%s"%(ascall.getParentEntry().name,ascall.name))
        self.states.append("X%s_%sFk"%(ascall.getParentEntry().name,ascall.name))
        #print("\t\t mapping AsynchCall choice %s"%(ascall.name))
        
    ###jump mapping 
    @dispatch(Task)
    def getJumps(self,task):
        #print("mapping jump task %s"%(task.name))
        for e in task.getEntries():
            self.getJumps(e)
        
    @dispatch(Entry)
    def getJumps(self,e):
        #print("\t mapping jump entry %s"%(e.name))
        d=e.getNextNode(d=None)
        while d is not None:
            self.getJumps(d)
            d=e.getNextNode(d=d)
            
    def getNextStep(self,jump,b):
        #poaao ristruttare questo metodo per evitare di ripetere lo stesso codice
        if(isinstance(b,Call)):
            jump[self.states.index("X%s_%s"%(b.dest.name,"a"))]=1;
            jump[self.states.index("X%s_%s"%(b.parent.name,b.name))]=1;
            if(type(b)==AsynchCall):
                jump[self.states.index("X%s_%sFk"%(b.parent.name,b.name))]=1;
                
        elif(type(b)==Activity):
            to="X%s_%s"%(b.parent.name,b.name)
            jump[self.states.index(to)]=1
            
        elif(type(b)==probChoice):
            raise ValueError("Not supported yet")
        
        return jump
    
    def getPropAcquie(self,entry):
        gpsAcq="%s/(%s)"%("X%s_a"%(entry.name),"+".join(["X%s_a"%(e.name) for e in entry.parentTask.getEntries()]))
        
        minThread="Δ*min(%s,NT[%s]-(%s))"%("+".join(["X%s_a"%(e.name) for e in entry.parentTask.getEntries()]),entry.parentTask.name,
                                           "+".join(["X%s_%s"%(e.name,a.name) for e in entry.parentTask.getEntries() for a in e.getActivities() if(type(a)!=AsynchCall)]))
        
        return "%s*%s"%(gpsAcq,minThread)

    def getPropAcqureNoInf(self,act):
        
        #mi conviene costruire la propensity da capo
        #per evitare di dover impattare sul rate delle altre activity sarebbe bello fare l'overloading dello stato di questa activity per tracciare il
        #numero di job che hanni acquisito e che stanno eseguento act
        
        #devo ritornare il rate di acquisizione di entry assumendo che sia tutto a carico della prima activityå
        #p.P_Think*X(2)/(X(2))*min(X(4),p.NT(2))/min(X(4),p.NT(2))*p.MU(4)*min(min(X(4),p.NT(2)),p.NC(2));
        
        #devo unire queste due propensity
        #p.P_Think*X(2)/(X(2))*X(4)/(X(4))*p.MU(4)*min(X(4),p.NC(2));
        #p.P_E1Work*X(3)/(X(3))*p.delta*min(X(3),p.NT(2)-(X(4)));
        
        #devo fare una fusuine tra i metodi fatti in precedenza
        
        
        # gpsAcq="%s/(%s)"%("X%s_a"%(entry.name),"+".join(["X%s_a"%(e.name) for e in entry.parentTask.getEntries()]))
        #
        # minThread="Δ*min(%s,NT[%s]-(%s))"%("+".join(["X%s_a"%(e.name) for e in entry.parentTask.getEntries()]),entry.parentTask.name,
        #                                    "+".join(["X%s_%s"%(e.name,a.name) for e in entry.parentTask.getEntries() for a in e.getActivities() if(type(a)!=AsynchCall)]))
        #
        # return "%s*%s"%(gpsAcq,minThread)
        raise ValueError("not Implemented yet")
    
    def getPropActivity(self,act):
        
        #devo prendere tutte le activity di tutte le entry dello stesso task
        #stessa cosa penso sia con i thread 
        gpsAct="%s/(%s)"%("X%s_%s"%(act.parent.name,act.name),"+".join(["X%s_%s"%(a.parent.name,a.name) for e in act.parent.parentTask.getEntries() for a in e.getActivities() if(type(a)==Activity)]))
        minCore="MU[X%s_%s]*min(%s,NC[%s])"%(act.parent.name,act.name,
                                        "+".join(["X%s_%s"%(a.parent.name,a.name) for e in act.parent.parentTask.getEntries() for a in e.getActivities() if(type(a)==Activity)]),
                                        act.parent.parentTask.name)
        return "%s*%s"%(gpsAct,minCore)
    
    def getPropSynch(self,sCall):
        rate="Δ*min(X%s_%s,X%s_%s)"%(sCall.parent.name,sCall.name,
                                     sCall.dest.name,sCall.name)
        return rate
    
    def getPropASynch(self,AsCall):
        rate="Δ*X%s_%sFk"%(AsCall.parent.name,AsCall.name)
        return rate
        
    @dispatch(probChoice)
    def getJumps(self,d):
        if(type(d.origin)==Entry):
            print(d.name,"from entry")
            frm=self.states.index("X%s_a"%(d.parent.name))
            for b in d.branches: 
                #acquire di un thread in in un task
                jump=[0 for i in range(len(self.states))]
                jump[frm]=-1
        
                jump=self.getNextStep(jump, b)
                
                self.Jumps.append(jump)
                self.props.append("%s*%s"%(d.probs[d.branches.index(b)],self.getPropAcquie(d.origin)))
        
        elif(type(d.origin)==Activity):
            #esecuzione di un activity
            frm=self.states.index("X%s_%s"%(d.parent.name,d.origin.name))
            for b in d.branches:
                jump=[0 for i in range(len(self.states))]
                jump[frm]=-1
                
                jump=self.getNextStep(jump, b)
                
                self.Jumps.append(jump)
                self.props.append("%s*%s"%(d.probs[d.branches.index(b)],self.getPropActivity(d.origin)))
                
        elif(type(d.origin)==SynchCall):
            #sincronizzazione di una chiamta sincrona
            print(d.name,"SynchCall")
            
            frm1="X%s_%s"%(d.origin.dest.name,d.origin.name)
            frm2="X%s_%s"%(d.origin.parent.name,d.origin.name)
            print(frm1,frm2)
            for b in d.branches:
                jump=[0 for i in range(len(self.states))]    
                jump[self.states.index(frm1)]=-1
                jump[self.states.index(frm2)]=-1
                
                jump=self.getNextStep(jump, b)
                
                self.Jumps.append(jump)
                self.props.append("%s*%s"%(d.probs[d.branches.index(b)],self.getPropSynch(d.origin)))
        elif(type(d.origin)==AsynchCall):
            #movimento di una chiamta asincrona
            jump=[0 for i in range(len(self.states))] 
            frm="X%s_%sFk"%(d.origin.parent.name,d.origin.name)
            jump[self.states.index(frm)]=-1
            
            for b in d.branches:
                jump=self.getNextStep(jump, b)
                    
            self.Jumps.append(jump)
            self.props.append(self.getPropASynch(d.origin))
        
    @dispatch(awsActivity)
    def getJumps(self,anwAct):
        if(not anwAct.parent.parentTask.ref):
            actfrm=self.states.index("X%s_%s"%(anwAct.activity.parent.name,anwAct.activity.name))
            for call in anwAct.activity.parent.calling:    
                #esecuzione di un activity
                jump=[0 for i in range(len(self.states))]
                jump[actfrm]=-1
                
                if(type(call)==SynchCall):
                    jump[self.states.index("X%s_%s"%(anwAct.activity.parent.name,call.name))]=+1;
                elif(type(call)==AsynchCall):
                    jump[self.states.index("X%s_%s"%(call.parent.name,call.name))]=-1
                
                self.Jumps.append(jump)
                prop=self.getPropActivity(anwAct.activity)
                prop="%s/(%s)*%s"%("X%s_%s"%(call.parent.name,call.name),
                                   "+".join(["X%s_%s"%(c.parent.name,c.name) for c in anwAct.activity.parent.calling]),
                                   prop)
                self.props.append(prop)
    
    def toLqns(self, outDir=None,LQN=None):
        if(outDir == None):
            outDir = "../model"
                
            
        env = Environment(
            loader=PackageLoader('trasducer', 'templates'),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=False)
        
        tname = [t.name for t in LQN["tasks"]]
        
        lqns_tmpl = env.get_template('model-tpl2.lqn')
        model = lqns_tmpl.render(task=LQN["tasks"], name=LQN["name"],names=self.states)
        
        outd = Path(outDir)
        outd = outd / LQN["name"]
        outd.mkdir(parents=True, exist_ok=True)
        
        mfid = open("%s/model.lqn" % str(outd.absolute()), "w+")
        mfid.write(model)
        mfid.close()
    
    def debugMPP(self):
        for t in self.lqn["tasks"]:
            print(t.name)
            for e in t.getEntries():
                print("\t"+e.name)
                for a in e.getActivities():
                    print("\t\t"+a.name)
                
                for d in e.getDnodes():
                    print("\t\t"+str(d))
                    
    def removeInfSynch(self):
        #per ogni chiamata sincrona, sostituisco il jump della sincronizzazione con la somma dei jump del completamento e quello dell'avanzamento dell'struzione
        #metto come propensiti la propensity del completamento moltiplicata per la probabilita della sincronizzazione
        
        #prima cerco tutte le chiamate sincrone poi faccio la funzione dei join e delle propensity
        for t in self.lqn["tasks"]:
            for e in t.getEntries():
                for a in e.getActivities():
                    if(type(a)==SynchCall):
                        synchState="X%s_%s"%(a.dest.name,a.name)#questo dovrebbe essere solo uno stato
                        synchIdx=self.states.index(synchState)
                        #recupero i jump della sincronizzazione
                        mask = (np.array(self.Jumps)[:, synchIdx] == -1)
                        #recupero la propensity della sincronizzazione
                        maskIdx=np.where(mask==True)[0]
                        #recupero tutti jump che identificano sincronizzazione
                        #print("##jump e prop sych###")
                        #recupero la probabilita di fare la sincronizzazione
                        prob=[]
                        for d in e.getDnodes():
                            if(type(d)==probChoice and d.origin==a):
                                prob=d.probs
                        #print(np.array(self.Jumps)[mask,:],np.array(self.props)[maskIdx.tolist()],prob)
                                
                        
                        #recupero 
                        mask1 = (np.array(self.Jumps)[:, synchIdx] == 1)
                        #recupero la propensity della sincronizzazione
                        mask1Idx=np.where(mask1==True)[0]
                        #recupero tutti jump che identificano sincronizzazione
                        #print("jump e prop sych")
                        print(np.array(self.Jumps)[mask1,:],np.array(self.props)[mask1Idx.tolist()])
                        
                        pIdx=0;
                        for idx,j1 in enumerate(maskIdx.tolist()):
                            for idx2,j2 in enumerate(mask1Idx.tolist()):
                                new_j=np.array(self.Jumps)[j1,:]+np.array(self.Jumps)[j2,:]
                                #non devo solo sostituire ma dovrei aggiungere e duplicare jump e propensity
                                #attualmente funziona solo se c'e una sola activity che risponde e se la sincronizzazione non genera scelte probabilistiche
                                #quello che dovrei fare e aggiungere un nuovo jump alla fine e anche le rispettive propensity, mette a Nonce quelle vechie e successivmente le rimuovo
                                self.Jumps[j1]=new_j.tolist()
                                self.props[j1]="%s*%s"%(prob[pIdx],self.props[j2])
                                
                                self.Jumps[j2]=[0 for k in range(len(self.states))]
                                self.props[j2]="0"
                            pIdx+=1
                            
    def removeInfAsynch(self):
            for t in self.lqn["tasks"]:
                for e in t.getEntries():
                    for a in e.getActivities():
                        if(type(a)==AsynchCall):
                            #so che metto un job nell'activity chiamante ma devo accorpare il jump che fanno avanzare lem istruzioni
                            sname="X%s_%sFk"%(a.parent.name,a.name)
                            print(sname)
                            sIdx=self.states.index(sname)
                            mask = (np.array(self.Jumps)[:, sIdx] == 1)
                            #recupero la propensity della sincronizzazione
                            maskIdx=np.where(mask==True)[0]
                            
                            #print(maskIdx)
                            
                            mask1 = (np.array(self.Jumps)[:, sIdx] == -1)
                            #recupero la propensity della sincronizzazione
                            mask1Idx=np.where(mask1==True)[0]
                            
                            #print(mask1Idx)
                            
                            prob=[]
                            for d in e.getDnodes():
                                if(type(d)==probChoice and d.origin==a):
                                    prob=d.probs
                            print(prob)
                            #stessa cosa per il caso delle chiamate sincrone. Devo fare un doppio ciclo. Nel paper lo scrivo bene
                            #nel tool lo implemento nel caso facile. Forse nel caso asyncrono e' piu complesso perche ci possono essere molte path e quindi molti jump
                            
                            pIdx=0;
                            for idx,j1 in enumerate(maskIdx.tolist()):
                                for idx2,j2 in enumerate(mask1Idx.tolist()):
                                    new_j=np.array(self.Jumps)[j1,:]+np.array(self.Jumps)[j2,:]
                                    #non devo solo sostituire ma dovrei aggiungere e duplicare jump e propensity
                                    #attualmente funziona solo se c'e una sola activity che risponde e se la sincronizzazione non genera scelte probabilistiche
                                    #quello che dovrei fare e aggiungere un nuovo jump alla fine e anche le rispettive propensity, mette a Nonce quelle vechie e successivmente le rimuovo
                                    self.Jumps[j1]=new_j.tolist()
                                    self.props[j1]="%s"%(self.props[j1])
                                    
                                    self.Jumps[j2]=[0 for k in range(len(self.states))]
                                    self.props[j2]="0"
                                pIdx+=1
                            
    def removeInfAcquire(self):
        for t in self.lqn["tasks"]:
                for e in t.getEntries():
                    for d in e.getDnodes():
                        if(type(d)==probChoice and type(d.origin)==Entry):
                            #ridireziono tutti quelli che mandano ad X_A nella coda della prima isttuzione di questa entry
                            sname="X%s_a"%(d.origin.name)
                            print(sname)
                            sIdx=self.states.index(sname)
                            maskIn = (np.array(self.Jumps)[:, sIdx] == 1)
                            maskOut = (np.array(self.Jumps)[:, sIdx] == -1)
                            
                            #recupero la propensity e i jump coinvolti nell'acquire
                            maskIdxIn=np.where(maskIn==True)[0]
                            maskIdxOut=np.where(maskOut==True)[0]
                            
                            prob=d.probs
                            
                            pIdx=0;
                            for idx,j1 in enumerate(maskIdxIn.tolist()):
                                for idx2,j2 in enumerate(maskIdxOut.tolist()): 
                                    
                                    new_j=np.array(self.Jumps)[j1,:]+np.array(self.Jumps)[j2,:]
                                    self.Jumps[j1]=[0 for i in range(len(new_j))]
                                    self.Jumps[j2]=[0 for i in range(len(new_j))]
                                    
                                    #definisco la nuova propensity come modifica di quella precedetemente posseduta dalla prima activity
                                    if(type(d.branches[pIdx])!=Activity):
                                        raise ValueError("For now the first action of an acquire should be an activity")
                                    
                                    actState="X%s_%s"%(d.branches[pIdx].parent.name,d.branches[pIdx].name);
                                    actStateIdx=self.states.index(actState)
                                    
                                    maskOut = (np.array(self.Jumps)[:, actStateIdx] == -1)
                                    maskIdxOut=np.where(maskOut==True)[0]
                                    #prop=np.array(self.props)[maskIdxOut]
                                    
                                    
                                    self.Jumps.append(new_j)
                                    
                                    #self.props.append(self.getPropAcqureNoInf(d.branches[pIdx]))
                                    
                                    #self.props[j1]="0"
                                    #self.props[j2]="0"
                                    
                                    
                                pIdx+=1
    
    def getConGraph(self):
        conMatrix=np.array([[0.0 for t in self.lqn["tasks"] for e in t.getEntries()] for t in self.lqn["tasks"] for e in t.getEntries()])
        entriesIdx=[e.name for t in self.lqn["tasks"] for e in t.getEntries()]
        for t in self.lqn["tasks"]:
                for e in t.getEntries():
                    for a in e.getActivities():
                        if(isinstance(a, SynchCall)):
                            #print(f"{a.getParentEntry().name}->{a.dest.name}")
                            sourceIdx=entriesIdx.index(a.getParentEntry().name)
                            destIdx=entriesIdx.index(a.dest.name)
                            #recuero la probabilita'con cui questa chiamata viene fatta guardando il decision node che la contiene
                            nodes=e.getDnodes()
                            prob=0
                            for n in nodes:
                                try:
                                    bidx=n.branches.index(a)
                                    prob=1.0/len(n.probs)
                                    break
                                    #print(f"###### {bidx}{prob}")
                                except:
                                    pass
                            conMatrix[sourceIdx,destIdx]+=(1.0*prob)
        
        return {"con":conMatrix,"idx":np.array(entriesIdx)}
        
                                    
if __name__ == '__main__':
    
    lqn2mpp=Lqn2MPP()
    
    nusers=10
    T0=Task(name="T0",proc=entity.Processor(name="P0",mult=nusers,sched="f"),tsize=nusers,ref=True)
    T1=Task(name="T1",proc=entity.Processor(name="P1",mult=nusers,sched="f"),tsize=nusers)
    #T2=Task(name="T2",proc=entity.Processor(name="P2",mult=nusers,sched="f"),tsize=nusers)
    #T3=Task(name="T3",proc=entity.Processor(name="P3",mult=nusers,sched="f"),tsize=nusers)
    # T4=Task(name="T4",proc=entity.Processor(name="P4",mult=nusers,sched="f"),tsize=nusers)
    # T5=Task(name="T5",proc=entity.Processor(name="P5",mult=nusers,sched="f"),tsize=nusers)
    
    e0 = Entry("E0")
    e1 = Entry("E1")
    e2 = Entry("E2")
    #e3 = Entry("E3")
    # e4 = Entry("E4")
    # e5 = Entry("E5")
    # e6 = Entry("E6")
    
    T0.addEntry(e0)
    T1.addEntry(e1)
    T1.addEntry(e2)
    #T3.addEntry(e3)
    # T4.addEntry(e4)
    # T4.addEntry(e5)
    # T5.addEntry(e6)
    
    e0A1=Activity(stime=1.0, parent=e0, name="Browse")
    e0A2=SynchCall(dest=e1, parent=e0, name="E0toE1")
    e0A3=SynchCall(dest=e2, parent=e0, name="E0toE2")
    
    e0D1=probChoice(parent=e0, name="e0I1", probs=["P_E0E1","P_E0E2"], branches=[e0A2,e0A3], origin=e0A1)
    e0D2=probChoice(parent=e0, name="e0I2", probs=["P_Think"], branches=[e0A1], origin=e0A2)
    e0D3=probChoice(parent=e0, name="e0I3", probs=["P_Think2"], branches=[e0A1], origin=e0A3)
    
    
    e0.getActivities().append(e0A1)
    e0.getActivities().append(e0A2)
    e0.getActivities().append(e0A3)
    e0.getDnodes().append(e0D1)
    e0.getDnodes().append(e0D2)
    e0.getDnodes().append(e0D3)
    
    
    # e1A1=AsynchCall(dest=e2, parent=e1, name="E1toE2")
    # e1A2=AsynchCall(dest=e3, parent=e1, name="E1toE3")
    e1A2=Activity(stime=1.0, parent=e1, name="e1Work")
    #e1A3=Activity(stime=1.0, parent=e1, name="e1Work2")
    # e1.getActivities().append(e1A1)
    e1.getActivities().append(e1A2)
    #e1.getActivities().append(e1A3)
    
    # e1D1=probChoice(parent=e1, name="e1I1", probs=["P_E1toE2"], branches=[e1A1], origin=e1)
    # e1D2=probChoice(parent=e1, name="e1I2", probs=["P_E1toE3"], branches=[e1A2], origin=e1A1)
    e1D2=probChoice(parent=e1, name="e1I3", probs=["P_E1Work"], branches=[e1A2], origin=e1)#anche per la sincronizzazione posso avere scelte prob
    #e1D3=probChoice(parent=e1, name="e1I4", probs=["P_E1Work2"], branches=[e1A3], origin=e1A2)#anche per la sincronizzazione posso avere scelte prob
    e1D4=awsActivity(parent=e1, name="e1I5",activity=e1A2)
    # e1.getDnodes().append(e1D1)
    e1.getDnodes().append(e1D2)
    #e1.getDnodes().append(e1D3)
    e1.getDnodes().append(e1D4)
    
    #e2A1=SynchCall(dest=e3, parent=e2, name="E2toE3")
    e2A2=Activity(stime=1.0, parent=e2, name="e2Work")
    #e2A3=Activity(stime=1.0, parent=e2, name="e2Work2")
    #e2.getActivities().append(e2A1)
    e2.getActivities().append(e2A2)
    #e2.getActivities().append(e2A3)
    
    # e2D1=probChoice(parent=e2, name="e2I1", probs=["P_E2toE3"], branches=[e2A1], origin=e2)
    e2D2=probChoice(parent=e2, name="e2I2", probs=["P_E2Work"], branches=[e2A2], origin=e2)
    e2D3=awsActivity(parent=e2, name="e2I3",activity=e2A2)
    #e2D4=awsActivity(parent=e2, name="e2I4",activity=e2A3)
    # e2.getDnodes().append(e2D1)
    e2.getDnodes().append(e2D2)
    e2.getDnodes().append(e2D3)
    #e2.getDnodes().append(e2D4)
    
    #e3A1=SynchCall(dest=e4, parent=e3, name="E3toE4")
    #e3A2=SynchCall(dest=e5, parent=e3, name="E3toE5")
    # e3A3=Activity(stime=1.0, parent=e3, name="e3Work")
    #e3.getActivities().append(e3A1)
    #e3.getActivities().append(e3A2)
    # e3.getActivities().append(e3A3)
    #e3D1=probChoice(parent=e3, name="e3I1", probs=["P_E3toE4"], branches=[e3A1], origin=e3)
    #e3D2=probChoice(parent=e3, name="e3I2", probs=["P_E3toE5"], branches=[e3A2], origin=e3A1)
    # e3D3=probChoice(parent=e3, name="e3I3", probs=["P_E3Work"], branches=[e3A3], origin=e3)
    # e3D4=awsActivity(parent=e3, name="e3I4",activity=e3A3)
    #e3.getDnodes().append(e3D1)
    #e3.getDnodes().append(e3D2)
    # e3.getDnodes().append(e3D3)
    # e3.getDnodes().append(e3D4)
    #
    # e4A1=Activity(stime=1.0, parent=e4, name="e4Work")
    # e4.getActivities().append(e4A1)
    # e4D1=probChoice(parent=e4, name="e4I1", probs=["P_E4Work"], branches=[e4A1], origin=e4)
    # e4D2=awsActivity(parent=e4, name="e4I2",activity=e4A1)
    # e4.getDnodes().append(e4D1)
    # e4.getDnodes().append(e4D2)
    #
    # e5A1=SynchCall(dest=e6, parent=e5, name="E5toE6")
    # e5A2=Activity(stime=1.0, parent=e5, name="e5Work")
    # e5.getActivities().append(e5A1)
    # e5.getActivities().append(e5A2)
    # e5D1=probChoice(parent=e5, name="e5I1", probs=["P_E5toE6"], branches=[e5A1], origin=e5)
    # e5D2=probChoice(parent=e5, name="e5I1", probs=["P_E5Work"], branches=[e5A2], origin=e5A1)
    # e5D3=awsActivity(parent=e5, name="e5I2",activity=e5A2)
    # e5.getDnodes().append(e5D1)
    # e5.getDnodes().append(e5D2)
    # e5.getDnodes().append(e5D3)
    #
    # e6A1=Activity(stime=1.0, parent=e6, name="e6Work")
    # e6.getActivities().append(e6A1)
    # e6D1=probChoice(parent=e6, name="e6I1", probs=["P_E6Work"], branches=[e6A1], origin=e6)
    # e6D2=awsActivity(parent=e6, name="e6I2",activity=e6A1)
    # e6.getDnodes().append(e6D1)
    # e6.getDnodes().append(e6D2)
    
    LQN={"tasks":[T0,T1], "name":"simpleModelV2"}
    lqn2mpp.getMPP(lqn=LQN)
    lqn2mpp.removeInfSynch()
    lqn2mpp.removeInfAsynch()
    #lqn2mpp.removeInfAcquire()
    lqn2mpp.toMatlab()
    lqn2mpp.toLqns(LQN=LQN)
    
    
    #print(np.array(lqn2mpp.Jumps))
    # idx=0
    # for j in np.array(lqn2mpp.Jumps):
    #     frm=np.where(j<0)[0]
    #     to=np.where(j>0)[0]
    #     print(np.array(lqn2mpp.states)[frm],"->",np.array(lqn2mpp.states)[to])
    #     print(lqn2mpp.props[idx])
    #     print("######")
    #     idx+=1