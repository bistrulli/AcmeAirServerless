import numpy as np
import pandas as pd
import subprocess
from pathlib import Path
from glob import glob
import time


#recupero tutti i le cartelle con estensione .lqn,
#per ognuna di loro recupero le allocazioni ottime e faccio deploy e update e salvo il tempo di inizio e fine esperimento

def runExp():
	dfexp=getExperiments()

	#get alredy analized systems
	if(dfexp is not None):
		exp=dfexp.to_numpy().tolist()
	else:
		exp=[]

	initLogger()

	sys=getSystems()
	for s in sys:
		if(s in np.array(exp)[:,0]):
			print(f"skipping {s}")
			continue
		else:
			print(f"analyzing {s}")

		deploySys(s)
		
		setDefConc(s)
		exp+=[[s,"defconc","start",time.time()]]
		startSys(s)
		exp+=[[s,"defconc","end",time.time()]]
		moveClientRt(s,"defconcrt")

		time.sleep(120)

		setNoConc(s)
		exp+=[[s,"noconc","start",time.time()]]
		startSys(s)
		exp+=[[s,"noconc","end",time.time()]]
		moveClientRt(s,"noconcrt")

		time.sleep(120)

		setWlessConc(s)
		exp+=[[s,"wlessconc","start",time.time()]]
		startSys(s)
		exp+=[[s,"wlessend","end",time.time()]]
		moveClientRt(s,"wlessrt")

		time.sleep(120)

		df = pd.DataFrame(exp, columns=["modelname","exptype","action","time"])
		df.to_csv("experiments.csv", index=False)

def getOptNT(sys):
	print(f"getOptNT {sys}")
	df=pd.read_csv(f"{sys.absolute()}/{sys.name}/optSol.csv")
	return df

def moveClientRt(sys,destname):
	sys=Path(sys)
	print(f"saving results {sys}")
	source_file=Path(f"{sys.absolute()}/clientEntry/clientrt.txt")
	source_file.rename(Path(f"{sys.absolute()}/clientEntry/{destname}.txt"))
	

def getSystems():
	pattern = "./*.lqn"
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
	if(Path("experiments.csv").is_file()):
		df=pd.read_csv("experiments.csv")
	return df

def initLogger():
	pass

if __name__ == '__main__':
	runExp()