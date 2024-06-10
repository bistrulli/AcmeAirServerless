import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.joinpath("MPP4Lqn")))

from entity import *
from Lqn2MPP import Lqn2MPP
		
if __name__ == '__main__':
	
	lqn2mpp=Lqn2MPP()
	nusers=1
	
	T_clientEntry=Task(name="T_clientEntry",proc=Processor(name="T_clientEntry",mult=nusers,sched="f"),tsize=nusers,ref=True)
	T_MSauthEntry=Task(name="T_MSauthEntry",proc=Processor(name="T_MSauthEntry",mult=nusers,sched="f"),tsize=nusers)
	T_MSvalidateidEntry=Task(name="T_MSvalidateidEntry",proc=Processor(name="T_MSvalidateidEntry",mult=nusers,sched="f"),tsize=nusers)
	T_MSviewprofileEntry=Task(name="T_MSviewprofileEntry",proc=Processor(name="T_MSviewprofileEntry",mult=nusers,sched="f"),tsize=nusers)
	T_MSupdateprofileEntry=Task(name="T_MSupdateprofileEntry",proc=Processor(name="T_MSupdateprofileEntry",mult=nusers,sched="f"),tsize=nusers)
	T_MSupdateMilesEntry=Task(name="T_MSupdateMilesEntry",proc=Processor(name="T_MSupdateMilesEntry",mult=nusers,sched="f"),tsize=nusers)
	T_MSbookflightsEntry=Task(name="T_MSbookflightsEntry",proc=Processor(name="T_MSbookflightsEntry",mult=nusers,sched="f"),tsize=nusers)
	T_MScancelbookingEntry=Task(name="T_MScancelbookingEntry",proc=Processor(name="T_MScancelbookingEntry",mult=nusers,sched="f"),tsize=nusers)
	T_MSqueryflightsEntry=Task(name="T_MSqueryflightsEntry",proc=Processor(name="T_MSqueryflightsEntry",mult=nusers,sched="f"),tsize=nusers)
	T_MSgetrewardmilesEntry=Task(name="T_MSgetrewardmilesEntry",proc=Processor(name="T_MSgetrewardmilesEntry",mult=nusers,sched="f"),tsize=nusers)
	
	clientEntry = Entry("clientEntry")
	T_clientEntry.addEntry(clientEntry)
	MSauthEntry = Entry("MSauthEntry")
	T_MSauthEntry.addEntry(MSauthEntry)
	MSvalidateidEntry = Entry("MSvalidateidEntry")
	T_MSvalidateidEntry.addEntry(MSvalidateidEntry)
	MSviewprofileEntry = Entry("MSviewprofileEntry")
	T_MSviewprofileEntry.addEntry(MSviewprofileEntry)
	MSupdateprofileEntry = Entry("MSupdateprofileEntry")
	T_MSupdateprofileEntry.addEntry(MSupdateprofileEntry)
	MSupdateMilesEntry = Entry("MSupdateMilesEntry")
	T_MSupdateMilesEntry.addEntry(MSupdateMilesEntry)
	MSbookflightsEntry = Entry("MSbookflightsEntry")
	T_MSbookflightsEntry.addEntry(MSbookflightsEntry)
	MScancelbookingEntry = Entry("MScancelbookingEntry")
	T_MScancelbookingEntry.addEntry(MScancelbookingEntry)
	MSqueryflightsEntry = Entry("MSqueryflightsEntry")
	T_MSqueryflightsEntry.addEntry(MSqueryflightsEntry)
	MSgetrewardmilesEntry = Entry("MSgetrewardmilesEntry")
	T_MSgetrewardmilesEntry.addEntry(MSgetrewardmilesEntry)
	
	
	
	###### clientEntry logic
	
	###### clientEntry activities and calls
	clientEntryclientEntry_A1=SynchCall(dest=MSviewprofileEntry, parent=clientEntry, name="clientEntry_A1ToMSviewprofileEntry")
	clientEntry.getActivities().append(clientEntryclientEntry_A1)
	clientEntryclientEntry_A2=SynchCall(dest=MSupdateprofileEntry, parent=clientEntry, name="clientEntry_A2ToMSupdateprofileEntry")
	clientEntry.getActivities().append(clientEntryclientEntry_A2)
	clientEntryclientEntry_A3=SynchCall(dest=MSbookflightsEntry, parent=clientEntry, name="clientEntry_A3ToMSbookflightsEntry")
	clientEntry.getActivities().append(clientEntryclientEntry_A3)
	clientEntryclientEntry_A4=SynchCall(dest=MScancelbookingEntry, parent=clientEntry, name="clientEntry_A4ToMScancelbookingEntry")
	clientEntry.getActivities().append(clientEntryclientEntry_A4)
	clientEntryclientEntry_A5=SynchCall(dest=MSqueryflightsEntry, parent=clientEntry, name="clientEntry_A5ToMSqueryflightsEntry")
	clientEntry.getActivities().append(clientEntryclientEntry_A5)
	clientEntryclientEntry_A6=SynchCall(dest=MSauthEntry, parent=clientEntry, name="clientEntry_A6ToMSauthEntry")
	clientEntry.getActivities().append(clientEntryclientEntry_A6)
	clientEntryclientEntry_A7=Activity(stime=0.02003, parent=clientEntry, name="clientEntry_A7")
	clientEntry.getActivities().append(clientEntryclientEntry_A7)

	###### clientEntry Activity Diagram
	clientEntryD0=probChoice(parent=clientEntry, name="clientEntryD0", 
									probs=["P_clientEntryclientEntry_A2clientEntryD0"], 
									branches=[clientEntryclientEntry_A2], 
									origin=clientEntryclientEntry_A1)
	clientEntry.getDnodes().append(clientEntryD0)
	clientEntryD1=probChoice(parent=clientEntry, name="clientEntryD1", 
									probs=["P_clientEntryclientEntry_A3clientEntryD1"], 
									branches=[clientEntryclientEntry_A3], 
									origin=clientEntryclientEntry_A2)
	clientEntry.getDnodes().append(clientEntryD1)
	clientEntryD2=probChoice(parent=clientEntry, name="clientEntryD2", 
									probs=["P_clientEntryclientEntry_A4clientEntryD2"], 
									branches=[clientEntryclientEntry_A4], 
									origin=clientEntryclientEntry_A3)
	clientEntry.getDnodes().append(clientEntryD2)
	clientEntryD3=probChoice(parent=clientEntry, name="clientEntryD3", 
									probs=["P_clientEntryclientEntry_A5clientEntryD3"], 
									branches=[clientEntryclientEntry_A5], 
									origin=clientEntryclientEntry_A4)
	clientEntry.getDnodes().append(clientEntryD3)
	clientEntryD4=probChoice(parent=clientEntry, name="clientEntryD4", 
									probs=["P_clientEntryclientEntry_A6clientEntryD4"], 
									branches=[clientEntryclientEntry_A6], 
									origin=clientEntryclientEntry_A5)
	clientEntry.getDnodes().append(clientEntryD4)
	clientEntryD5=probChoice(parent=clientEntry, name="clientEntryD5", 
									probs=["P_clientEntryclientEntry_A7clientEntryD5"], 
									branches=[clientEntryclientEntry_A7], 
									origin=clientEntryclientEntry_A6)
	clientEntry.getDnodes().append(clientEntryD5)
	clientEntryDf=probChoice(parent=clientEntry, name="clientEntryDf", 
									probs=["P_clientEntry_A1"], 
									branches=[clientEntryclientEntry_A1], 
									origin=clientEntryclientEntry_A7)
	clientEntry.getDnodes().append(clientEntryDf)
	
	
	###### MSauthEntry logic
	
	###### MSauthEntry activities and calls
	MSauthEntryMSauthEntry_A1=SynchCall(dest=MSvalidateidEntry, parent=MSauthEntry, name="MSauthEntry_A1ToMSvalidateidEntry")
	MSauthEntry.getActivities().append(MSauthEntryMSauthEntry_A1)
	MSauthEntryMSauthEntry_A2=Activity(stime=0.03165, parent=MSauthEntry, name="MSauthEntry_A2")
	MSauthEntry.getActivities().append(MSauthEntryMSauthEntry_A2)

	###### MSauthEntry Activity Diagram
	# connect the entry to the main activity of function 
	MSauthEntryDI=probChoice(parent=MSauthEntry, name="MSauthEntryDI", 
									probs=["P_MSauthEntryMSauthEntry_A1"], 
									branches=[MSauthEntryMSauthEntry_A1], 
									origin=MSauthEntry)
	MSauthEntry.getDnodes().append(MSauthEntryDI)
	MSauthEntryD0=probChoice(parent=MSauthEntry, name="MSauthEntryD0", 
									probs=["P_MSauthEntryMSauthEntry_A2MSauthEntryD0"], 
									branches=[MSauthEntryMSauthEntry_A2], 
									origin=MSauthEntryMSauthEntry_A1)
	MSauthEntry.getDnodes().append(MSauthEntryD0)
	MSauthEntryD1=awsActivity(parent=MSauthEntry, name="MSauthEntryD1",activity=MSauthEntryMSauthEntry_A2)
	MSauthEntry.getDnodes().append(MSauthEntryD1)
	
	
	###### MSvalidateidEntry logic
	
	###### MSvalidateidEntry activities and calls
	MSvalidateidEntryMSvalidateidEntry_A1=Activity(stime=0.04331, parent=MSvalidateidEntry, name="MSvalidateidEntry_A1")
	MSvalidateidEntry.getActivities().append(MSvalidateidEntryMSvalidateidEntry_A1)

	###### MSvalidateidEntry Activity Diagram
	# connect the entry to the main activity of function 
	MSvalidateidEntryDI=probChoice(parent=MSvalidateidEntry, name="MSvalidateidEntryDI", 
									probs=["P_MSvalidateidEntryMSvalidateidEntry_A1"], 
									branches=[MSvalidateidEntryMSvalidateidEntry_A1], 
									origin=MSvalidateidEntry)
	MSvalidateidEntry.getDnodes().append(MSvalidateidEntryDI)
	MSvalidateidEntryD0=awsActivity(parent=MSvalidateidEntry, name="MSvalidateidEntryD0",activity=MSvalidateidEntryMSvalidateidEntry_A1)
	MSvalidateidEntry.getDnodes().append(MSvalidateidEntryD0)
	
	
	###### MSviewprofileEntry logic
	
	###### MSviewprofileEntry activities and calls
	MSviewprofileEntryMSviewprofileEntry_A1=Activity(stime=0.0463, parent=MSviewprofileEntry, name="MSviewprofileEntry_A1")
	MSviewprofileEntry.getActivities().append(MSviewprofileEntryMSviewprofileEntry_A1)

	###### MSviewprofileEntry Activity Diagram
	# connect the entry to the main activity of function 
	MSviewprofileEntryDI=probChoice(parent=MSviewprofileEntry, name="MSviewprofileEntryDI", 
									probs=["P_MSviewprofileEntryMSviewprofileEntry_A1"], 
									branches=[MSviewprofileEntryMSviewprofileEntry_A1], 
									origin=MSviewprofileEntry)
	MSviewprofileEntry.getDnodes().append(MSviewprofileEntryDI)
	MSviewprofileEntryD0=awsActivity(parent=MSviewprofileEntry, name="MSviewprofileEntryD0",activity=MSviewprofileEntryMSviewprofileEntry_A1)
	MSviewprofileEntry.getDnodes().append(MSviewprofileEntryD0)
	
	
	###### MSupdateprofileEntry logic
	
	###### MSupdateprofileEntry activities and calls
	MSupdateprofileEntryMSupdateprofileEntry_A1=Activity(stime=0.04102, parent=MSupdateprofileEntry, name="MSupdateprofileEntry_A1")
	MSupdateprofileEntry.getActivities().append(MSupdateprofileEntryMSupdateprofileEntry_A1)

	###### MSupdateprofileEntry Activity Diagram
	# connect the entry to the main activity of function 
	MSupdateprofileEntryDI=probChoice(parent=MSupdateprofileEntry, name="MSupdateprofileEntryDI", 
									probs=["P_MSupdateprofileEntryMSupdateprofileEntry_A1"], 
									branches=[MSupdateprofileEntryMSupdateprofileEntry_A1], 
									origin=MSupdateprofileEntry)
	MSupdateprofileEntry.getDnodes().append(MSupdateprofileEntryDI)
	MSupdateprofileEntryD0=awsActivity(parent=MSupdateprofileEntry, name="MSupdateprofileEntryD0",activity=MSupdateprofileEntryMSupdateprofileEntry_A1)
	MSupdateprofileEntry.getDnodes().append(MSupdateprofileEntryD0)
	
	
	###### MSupdateMilesEntry logic
	
	###### MSupdateMilesEntry activities and calls
	MSupdateMilesEntryMSupdateMilesEntry_A1=Activity(stime=0.12271, parent=MSupdateMilesEntry, name="MSupdateMilesEntry_A1")
	MSupdateMilesEntry.getActivities().append(MSupdateMilesEntryMSupdateMilesEntry_A1)

	###### MSupdateMilesEntry Activity Diagram
	# connect the entry to the main activity of function 
	MSupdateMilesEntryDI=probChoice(parent=MSupdateMilesEntry, name="MSupdateMilesEntryDI", 
									probs=["P_MSupdateMilesEntryMSupdateMilesEntry_A1"], 
									branches=[MSupdateMilesEntryMSupdateMilesEntry_A1], 
									origin=MSupdateMilesEntry)
	MSupdateMilesEntry.getDnodes().append(MSupdateMilesEntryDI)
	MSupdateMilesEntryD0=awsActivity(parent=MSupdateMilesEntry, name="MSupdateMilesEntryD0",activity=MSupdateMilesEntryMSupdateMilesEntry_A1)
	MSupdateMilesEntry.getDnodes().append(MSupdateMilesEntryD0)
	
	
	###### MSbookflightsEntry logic
	
	###### MSbookflightsEntry activities and calls
	MSbookflightsEntryMSbookflightsEntry_A1=SynchCall(dest=MSupdateMilesEntry, parent=MSbookflightsEntry, name="MSbookflightsEntry_A1ToMSupdateMilesEntry")
	MSbookflightsEntry.getActivities().append(MSbookflightsEntryMSbookflightsEntry_A1)
	MSbookflightsEntryMSbookflightsEntry_A2=SynchCall(dest=MSgetrewardmilesEntry, parent=MSbookflightsEntry, name="MSbookflightsEntry_A2ToMSgetrewardmilesEntry")
	MSbookflightsEntry.getActivities().append(MSbookflightsEntryMSbookflightsEntry_A2)
	MSbookflightsEntryMSbookflightsEntry_A3=SynchCall(dest=MSupdateMilesEntry, parent=MSbookflightsEntry, name="MSbookflightsEntry_A3ToMSupdateMilesEntry")
	MSbookflightsEntry.getActivities().append(MSbookflightsEntryMSbookflightsEntry_A3)
	MSbookflightsEntryMSbookflightsEntry_A4=SynchCall(dest=MSgetrewardmilesEntry, parent=MSbookflightsEntry, name="MSbookflightsEntry_A4ToMSgetrewardmilesEntry")
	MSbookflightsEntry.getActivities().append(MSbookflightsEntryMSbookflightsEntry_A4)
	MSbookflightsEntryMSbookflightsEntry_A5=Activity(stime=0.0249, parent=MSbookflightsEntry, name="MSbookflightsEntry_A5")
	MSbookflightsEntry.getActivities().append(MSbookflightsEntryMSbookflightsEntry_A5)

	###### MSbookflightsEntry Activity Diagram
	# connect the entry to the main activity of function 
	MSbookflightsEntryDI=probChoice(parent=MSbookflightsEntry, name="MSbookflightsEntryDI", 
									probs=["P_MSbookflightsEntryMSbookflightsEntry_A1"], 
									branches=[MSbookflightsEntryMSbookflightsEntry_A1], 
									origin=MSbookflightsEntry)
	MSbookflightsEntry.getDnodes().append(MSbookflightsEntryDI)
	MSbookflightsEntryD0=probChoice(parent=MSbookflightsEntry, name="MSbookflightsEntryD0", 
									probs=["P_MSbookflightsEntryMSbookflightsEntry_A2MSbookflightsEntryD0"], 
									branches=[MSbookflightsEntryMSbookflightsEntry_A2], 
									origin=MSbookflightsEntryMSbookflightsEntry_A1)
	MSbookflightsEntry.getDnodes().append(MSbookflightsEntryD0)
	MSbookflightsEntryD1=probChoice(parent=MSbookflightsEntry, name="MSbookflightsEntryD1", 
									probs=["P_MSbookflightsEntryMSbookflightsEntry_A3MSbookflightsEntryD1"], 
									branches=[MSbookflightsEntryMSbookflightsEntry_A3], 
									origin=MSbookflightsEntryMSbookflightsEntry_A2)
	MSbookflightsEntry.getDnodes().append(MSbookflightsEntryD1)
	MSbookflightsEntryD2=probChoice(parent=MSbookflightsEntry, name="MSbookflightsEntryD2", 
									probs=["P_MSbookflightsEntryMSbookflightsEntry_A4MSbookflightsEntryD2"], 
									branches=[MSbookflightsEntryMSbookflightsEntry_A4], 
									origin=MSbookflightsEntryMSbookflightsEntry_A3)
	MSbookflightsEntry.getDnodes().append(MSbookflightsEntryD2)
	MSbookflightsEntryD3=probChoice(parent=MSbookflightsEntry, name="MSbookflightsEntryD3", 
									probs=["P_MSbookflightsEntryMSbookflightsEntry_A5MSbookflightsEntryD3"], 
									branches=[MSbookflightsEntryMSbookflightsEntry_A5], 
									origin=MSbookflightsEntryMSbookflightsEntry_A4)
	MSbookflightsEntry.getDnodes().append(MSbookflightsEntryD3)
	MSbookflightsEntryD4=awsActivity(parent=MSbookflightsEntry, name="MSbookflightsEntryD4",activity=MSbookflightsEntryMSbookflightsEntry_A5)
	MSbookflightsEntry.getDnodes().append(MSbookflightsEntryD4)
	
	
	###### MScancelbookingEntry logic
	
	###### MScancelbookingEntry activities and calls
	MScancelbookingEntryMScancelbookingEntry_A1=SynchCall(dest=MSupdateMilesEntry, parent=MScancelbookingEntry, name="MScancelbookingEntry_A1ToMSupdateMilesEntry")
	MScancelbookingEntry.getActivities().append(MScancelbookingEntryMScancelbookingEntry_A1)
	MScancelbookingEntryMScancelbookingEntry_A2=SynchCall(dest=MSgetrewardmilesEntry, parent=MScancelbookingEntry, name="MScancelbookingEntry_A2ToMSgetrewardmilesEntry")
	MScancelbookingEntry.getActivities().append(MScancelbookingEntryMScancelbookingEntry_A2)
	MScancelbookingEntryMScancelbookingEntry_A3=Activity(stime=0.03137, parent=MScancelbookingEntry, name="MScancelbookingEntry_A3")
	MScancelbookingEntry.getActivities().append(MScancelbookingEntryMScancelbookingEntry_A3)

	###### MScancelbookingEntry Activity Diagram
	# connect the entry to the main activity of function 
	MScancelbookingEntryDI=probChoice(parent=MScancelbookingEntry, name="MScancelbookingEntryDI", 
									probs=["P_MScancelbookingEntryMScancelbookingEntry_A1"], 
									branches=[MScancelbookingEntryMScancelbookingEntry_A1], 
									origin=MScancelbookingEntry)
	MScancelbookingEntry.getDnodes().append(MScancelbookingEntryDI)
	MScancelbookingEntryD0=probChoice(parent=MScancelbookingEntry, name="MScancelbookingEntryD0", 
									probs=["P_MScancelbookingEntryMScancelbookingEntry_A2MScancelbookingEntryD0"], 
									branches=[MScancelbookingEntryMScancelbookingEntry_A2], 
									origin=MScancelbookingEntryMScancelbookingEntry_A1)
	MScancelbookingEntry.getDnodes().append(MScancelbookingEntryD0)
	MScancelbookingEntryD1=probChoice(parent=MScancelbookingEntry, name="MScancelbookingEntryD1", 
									probs=["P_MScancelbookingEntryMScancelbookingEntry_A3MScancelbookingEntryD1"], 
									branches=[MScancelbookingEntryMScancelbookingEntry_A3], 
									origin=MScancelbookingEntryMScancelbookingEntry_A2)
	MScancelbookingEntry.getDnodes().append(MScancelbookingEntryD1)
	MScancelbookingEntryD2=awsActivity(parent=MScancelbookingEntry, name="MScancelbookingEntryD2",activity=MScancelbookingEntryMScancelbookingEntry_A3)
	MScancelbookingEntry.getDnodes().append(MScancelbookingEntryD2)
	
	
	###### MSqueryflightsEntry logic
	
	###### MSqueryflightsEntry activities and calls
	MSqueryflightsEntryMSqueryflightsEntry_A1=Activity(stime=0.03107, parent=MSqueryflightsEntry, name="MSqueryflightsEntry_A1")
	MSqueryflightsEntry.getActivities().append(MSqueryflightsEntryMSqueryflightsEntry_A1)

	###### MSqueryflightsEntry Activity Diagram
	# connect the entry to the main activity of function 
	MSqueryflightsEntryDI=probChoice(parent=MSqueryflightsEntry, name="MSqueryflightsEntryDI", 
									probs=["P_MSqueryflightsEntryMSqueryflightsEntry_A1"], 
									branches=[MSqueryflightsEntryMSqueryflightsEntry_A1], 
									origin=MSqueryflightsEntry)
	MSqueryflightsEntry.getDnodes().append(MSqueryflightsEntryDI)
	MSqueryflightsEntryD0=awsActivity(parent=MSqueryflightsEntry, name="MSqueryflightsEntryD0",activity=MSqueryflightsEntryMSqueryflightsEntry_A1)
	MSqueryflightsEntry.getDnodes().append(MSqueryflightsEntryD0)
	
	
	###### MSgetrewardmilesEntry logic
	
	###### MSgetrewardmilesEntry activities and calls
	MSgetrewardmilesEntryMSgetrewardmilesEntry_A1=Activity(stime=0.02003, parent=MSgetrewardmilesEntry, name="MSgetrewardmilesEntry_A1")
	MSgetrewardmilesEntry.getActivities().append(MSgetrewardmilesEntryMSgetrewardmilesEntry_A1)

	###### MSgetrewardmilesEntry Activity Diagram
	# connect the entry to the main activity of function 
	MSgetrewardmilesEntryDI=probChoice(parent=MSgetrewardmilesEntry, name="MSgetrewardmilesEntryDI", 
									probs=["P_MSgetrewardmilesEntryMSgetrewardmilesEntry_A1"], 
									branches=[MSgetrewardmilesEntryMSgetrewardmilesEntry_A1], 
									origin=MSgetrewardmilesEntry)
	MSgetrewardmilesEntry.getDnodes().append(MSgetrewardmilesEntryDI)
	MSgetrewardmilesEntryD0=awsActivity(parent=MSgetrewardmilesEntry, name="MSgetrewardmilesEntryD0",activity=MSgetrewardmilesEntryMSgetrewardmilesEntry_A1)
	MSgetrewardmilesEntry.getDnodes().append(MSgetrewardmilesEntryD0)
	
	LQN={"tasks":[T_clientEntry ,T_MSauthEntry,T_MSvalidateidEntry,T_MSviewprofileEntry,T_MSupdateprofileEntry,T_MSupdateMilesEntry,T_MSbookflightsEntry,T_MScancelbookingEntry,T_MSqueryflightsEntry,T_MSgetrewardmilesEntry], "name":"lqnmodel_24.lqn"}
	lqn2mpp.getMPP(lqn=LQN)
	#lqn2mpp.removeInfSynch()
	#lqn2mpp.removeInfAsynch()
	#lqn2mpp.removeInfAcquire()
	lqn2mpp.toMatlab(outDir="./")
	#lqn2mpp.toLqns(outDir="model",LQN=LQN)
	