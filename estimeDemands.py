import numpy as np
from pathlib import Path
import pandas as pd
import re

def getNesstedRTime(e,con):
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
            df_nested=pd.read_csv(f"./logs/{dname}.csv",names=["A","B","C","D","cpu","rt"],delim_whitespace=True)
            df_nested["rt"]=df_nested["rt"].apply(lambda x:float(re.findall("\d+",x)[0])*1e-9)
            nestedTime+=val*df_nested["rt"].mean()
    return nestedTime

def estimeDeaand(lqn=None,con=None):
    logs=Path("./logs")
    if(logs.is_dir()):
        print("log exist I can calibrate")
    else:
        print("log not exist I can calibrate")
    
    demands={}
    
    for t in lqn["tasks"]:
        if(not t.ref):
            for  e in t.getEntries():
                print(f"calibrating {e.name}")
                #get rt of this function
                df=pd.read_csv(f"./logs/{e.name}.csv",names=["A","B","C","D","cpu","rt"],delim_whitespace=True)
                df["rt"]=df["rt"].apply(lambda x:float(re.findall("\d+",x)[0])*1e-9)
                df["cpu"]=df["cpu"].apply(lambda x:float(re.findall("\d+",x)[0])*1e-9)
                
                #get rt of called function
                nestedTime=getNesstedRTime(e,con)
                
                #print("\t",df["rt"].mean()-nestedTime)
                demands[e.name]=df["rt"].mean()-nestedTime
        else:
            for e in t.getEntries():
                print(f"calibrating {e.name}")
                df=pd.read_csv(f"./logs/{e.name}.csv")
                df["Average Response Time"].iloc[0:-1].sum()
                
                #get rt of called function
                nestedTime=getNesstedRTime(e,con)
                #print("\t",3.0/df["Requests/s"].iloc[0]-nestedTime)
                demands[e.name]=3.0/df["Requests/s"].iloc[0]-nestedTime
    return demands