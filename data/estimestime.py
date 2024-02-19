import pandas as pd
import numpy as np
import os
import glob

path = './'
extension = 'csv'
os.chdir(path)
datafiles = glob.glob('*.{}'.format(extension))
for f in datafiles:
	print(f"reading {f}")
	df=pd.read_csv(f,names=["idx","severity","ms","date"],sep="  ",engine='python')
	df["date"]=df["date"].apply(lambda x:float(x.replace("time:=","")))
	print(df["date"].mean()/1e09)
