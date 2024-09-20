import numpy as np
import pandas as pd
import subprocess
from pathlib import Path
from glob import glob
import time
import re


# Retrieve all variants within the Acmeair_variants directory
# For each variant:
    # Get the optimal allocations
    # Perform deployment and update
    # Save the start and end time of the experiment

def runExp():
	dfexp=getExperiments()

	#get alredy analized systems
	if(dfexp is not None):
		exp=dfexp.to_numpy().tolist()
	else:
		exp=[]

	sys=getSystems()
	for s in sys:
		# if(Path(s).name=="Acmeair_1"):
		# 	print(f"analyzing {Path(s).name}")
		# else:
		# 	continue
		
		deploySys(s)

		modelname=f"./{Path(s).name}"
		if(dfexp.shape[0]>0 and dfexp[(dfexp["modelname"]==modelname) & (dfexp["exptype"]=="defconc")].shape[0]>0):
			print(f"{modelname} defconc analized")
		else:
			setDefConc(s)
			exp+=[[modelname,"defconc","start",time.time()]]
			startSys(s)
			exp+=[[modelname,"defconc","end",time.time()]]
			moveClientRt(s,"defconcrt")
			time.sleep(120)

		if(dfexp.shape[0]>0 and dfexp[(dfexp["modelname"]==modelname) & (dfexp["exptype"]=="noconc")].shape[0]>0):
			print(f"{modelname} noconc analized")
		else:
			setNoConc(s)
			exp+=[[modelname,"noconc","start",time.time()]]
			startSys(s)
			exp+=[[modelname,"noconc","end",time.time()]]
			moveClientRt(s,"noconcrt")
			time.sleep(120)

		if(dfexp.shape[0]>0 and dfexp[(dfexp["modelname"]==modelname) & (dfexp["exptype"]=="wlessconc")].shape[0]>0):
			print(f"{modelname} wlessconc analized")
		else:
			setWlessConc(s)
			exp+=[[modelname,"wlessconc","start",time.time()]]
			startSys(s)
			exp+=[[modelname,"wlessend","end",time.time()]]
			moveClientRt(s,"wlessrt")
			time.sleep(120)

		if(dfexp.shape[0]>0 and dfexp[(dfexp["modelname"]==modelname) & (dfexp["exptype"]=="propackconc")].shape[0]>0):
			print(f"{modelname} propackconc analized")
		else:
			setProPackConc(s)
			exp+=[[modelname,"propackconc","start",time.time()]]
			startSys(s)
			exp+=[[modelname,"propackconc","end",time.time()]]
			moveClientRt(s,"propackrt")
			time.sleep(120)
			print("should run ProPack")

		df = pd.DataFrame(exp, columns=["modelname","exptype","action","time"])
		df.to_csv("./results/experiments.csv", index=False)

def getOptNT(sys):
	print(f"getOptNT {sys}")
	instanceNbr=re.findall(r"[0-9]+",sys.name)[0]
	df=pd.read_csv(f"{sys.absolute()}/lqnmodel_{instanceNbr}.lqn/optSol.csv")
	return df

def getProPackNT(sys):
	print(f"getProPackNT {sys}")
	instanceNbr=re.findall(r"[0-9]+",sys.name)[0]
	df=pd.read_csv(f"{sys.absolute()}/lqnmodel_{instanceNbr}.lqn/ProPackSol.csv",)
	return df

def moveClientRt(sys,destname):
	sys=Path(sys)
	print(f"saving results {sys}")
	source_file=Path(f"{sys.absolute()}/clientEntry/clientrt.txt")
	source_file.rename(Path(f"{sys.absolute()}/clientEntry/{destname}.txt"))
	

def getSystems():
	pattern = str(Path(__file__).parent.joinpath("Acmeair_variants/Acmeair_*"))
	matching_folders = glob(pattern, recursive=False)  # Perform recursive search
	return matching_folders

def setDefConc(sys):
	sys=Path(sys)
	print(f"setDefConc {sys}")

	pattern = f"{sys}/MS**Entry"
	matching_folders = glob(pattern, recursive=False)  # Perform recursive search

	for ms in matching_folders:
		print(f"Updateing {ms}")
		# Define the command and working directory
		command = ["sh","./update.sh","80","200","1"]
		working_dir = Path(ms).absolute()

		with open("update.log", "w") as outfile:
			subprocess.run(command, cwd=working_dir)#stdout=outfile, stderr=subprocess.STDOUT)

def setWlessConc(sys):
	sys=Path(sys)
	print(f"setWlessConc {sys}")

	ntopt=getOptNT(sys)

	pattern = f"{sys}/MS**Entry"
	matching_folders = glob(pattern, recursive=False)  # Perform recursive search

	for ms in matching_folders:
		print(f"Updating {Path(ms).name}")

		nt=ntopt[ntopt["name"]==Path(ms).name]["ntopt"].iloc[0]
		print(nt)

		# Define the command and working directory
		command = ["sh","./update.sh",f"{nt}","200","1"]
		working_dir = Path(ms).absolute()

		with open("update.log", "w") as outfile:
		 	subprocess.run(command, cwd=working_dir)#stdout=outfile, stderr=subprocess.STDOUT)

def setProPackConc(sys):
	sys=Path(sys)
	print(f"setProPackConc {sys}")

	ntopt=getProPackNT(sys)

	pattern = f"{sys}/MS**Entry"
	matching_folders = glob(pattern, recursive=False)  # Perform recursive search

	for ms in matching_folders:
		print(f"Updating {Path(ms).name}")

		nt=ntopt[ntopt["name"]==Path(ms).name]["ncopt"].iloc[0]

		# Define the command and working directory
		command = ["sh","./update.sh",f"{nt}","200","1"]
		working_dir = Path(ms).absolute()

		with open("update.log", "w") as outfile:
		 	subprocess.run(command, cwd=working_dir)#stdout=outfile, stderr=subprocess.STDOUT)

def setNoConc(sys):
	sys=Path(sys)
	print(f"setNoConc {sys}")

	pattern = f"{sys}/MS**Entry"
	matching_folders = glob(pattern, recursive=False)  # Perform recursive search

	for ms in matching_folders:
		print(f"Updateing {ms}")
		# Define the command and working directory
		command = ["sh","./update.sh","1","200","1"]
		working_dir = Path(ms).absolute()

		with open("update.log", "w") as outfile:
			subprocess.run(command, cwd=working_dir)#stdout=outfile, stderr=subprocess.STDOUT)

def deploySys(sys):
	sys=Path(sys)
	print(f"Deploying {sys}")
	# Define the command and working directory
	command = ["sh","./deploy_sys.sh"]
	working_dir = sys.absolute()

	with open("deploy.log", "w") as outfile:
		subprocess.run(command, cwd=working_dir)#stdout=outfile, stderr=subprocess.STDOUT)

def startSys(sys):
	sys=Path(sys)
	print(f"startSys {sys}")
	command = ["sh","./profile.sh","10"]
	working_dir = f"{sys.absolute()}/clientEntry"

	with open("locust.log", "w") as outfile:
		subprocess.run(command, cwd=working_dir)#stdout=outfile, stderr=subprocess.STDOUT)

def getExperiments():
	df=None
	if(Path(__file__).parent.joinpath("results/experiments.csv").is_file()):
		df=pd.read_csv(Path(__file__).parent.joinpath("results/experiments.csv"))
	return df

def computeProPack(sys):
	sys=Path(sys)
	print(f"computing ProPack on {sys}")

	instanceNbr=re.findall(r"[0-9]+",sys.name)[0]

	pattern = f"{sys}/**/lqnmodel_{instanceNbr}.lqn"
	matching_folders = glob(pattern, recursive=True)  # Perform recursive search

	if(len(matching_folders)==0):
		raise ValueError(f"{pattern} not found")

	scriptDir=matching_folders[0]

	command = ["sh","runProPack.sh"]
	working_dir = Path(scriptDir).absolute()

	with open("ProPack.log", "w") as outfile:
		subprocess.run(command, cwd=working_dir)#,stdout=outfile, stderr=subprocess.STDOUT)	

if __name__ == '__main__':
	runExp()
	# sys=getSystems()
	# for s in sys:
	# 	computeProPack(s)