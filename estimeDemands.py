import numpy as np
from pathlib import Path
import pandas as pd
import re

def estimeDeaand(lqn=None,con=None):
    logs=Path("./logs")
    if(logs.is_dir()):
        print("log exist I can calibrate")
    else:
        print("log not exist I can calibrate")
    
    for t in lqn["tasks"]:
        if(not t.ref):
            for  e in t.getEntries():
                print(f"calibrating {e.name}")
                #get rt of this function
                df=pd.read_csv(f"./logs/{e.name}.csv",names=["A","B","C","D","Time"],delim_whitespace=True)
                df["Time"]=df["Time"].apply(lambda x:float(re.findall("\d+",x)[0])*1e-9)
                
                #get rt of called function
                eidx=con["idx"].tolist().index(e.name)
                calledEntry=con["con"][eidx,:]
                nestedTime=0
                for idx,val in enumerate(calledEntry):
                    #print(idx,val,eidx,calledEntry)
                    if(val>0):
                        dname=con["idx"].tolist()[idx]
                        print(f"{val}x{e.name}->{dname}")
                        
                        #get rt of nested functions
                        df_nested=pd.read_csv(f"./logs/{dname}.csv",names=["A","B","C","D","Time"],delim_whitespace=True)
                        df_nested["Time"]=df_nested["Time"].apply(lambda x:float(re.findall("\d+",x)[0])*1e-9)
                        nestedTime+=val*df_nested["Time"].mean()
                
                print(df["Time"].mean(),nestedTime)
                
                