'''
curl command for gettinh the billable time programmatically from googl cloud monitoring

#to get the access token
TOKEN=$(gcloud auth print-access-token)

PROJECT_ID=modellearning

curl -d @query.json -H "Authorization: Bearer $TOKEN" \
--header "Content-Type: application/json" -X POST https://monitoring.googleapis.com/v3/projects/$PROJECT_ID/timeSeries:query
'''

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from pytz import utc
import matplotlib.pyplot as plt
from pathlib import Path
from pygnuplot import gnuplot as gp
from scipy.io import savemat
from pathlib import Path
import re

def main(resDir=None):
    jdata=json.load(open(resDir.joinpath("billingres.json"),"r"))
    trace=jdata["timeSeriesData"][0]["pointData"]
    df_bill=pd.DataFrame([[p["values"][0]["doubleValue"],p["timeInterval"]["startTime"]] for p in trace],columns=["values","time"])
    df_bill["time"]=pd.to_datetime(df_bill["time"])

    expdf=pd.read_csv(resDir.joinpath("experiments.csv"))

    defbill=[]
    noconcbill=[]
    wlessbill=[]

    defconcRt95=[]
    noconcRt95=[]
    wlessRt95=[]

    defconcRt70=[]
    noconcRt70=[]
    wlessRt70=[]

    defconcRtAvg=[]
    noconcRtAvg=[]
    wlessRtAvg=[]

    allOptCon=[]

    models=list(set(expdf["modelname"].to_numpy()))
    for m in sorted(models):
        midx=re.findall(r"[0-9]+",m)[0]
        clientEntryPath=resDir.parent.joinpath("Acmeair_variants")/Path(m).joinpath("clientEntry")
        lqnModelPath=resDir.parent.joinpath("Acmeair_variants")/Path(m).joinpath(f"lqnmodel_{midx}.lqn").joinpath("optSol.csv")

        optCon=pd.read_csv(lqnModelPath)
        allOptCon+=[optCon[["ncopt","ntopt"]].to_numpy()]

        defconcRt95+=[np.percentile(np.loadtxt(clientEntryPath.joinpath("defconcrt.txt")),95)]
        noconcRt95+=[np.percentile(np.loadtxt(clientEntryPath.joinpath("noconcrt.txt")),95)]
        wlessRt95+=[np.percentile(np.loadtxt(clientEntryPath.joinpath("wlessrt.txt")),95)]

        defconcRt70+=[np.percentile(np.loadtxt(clientEntryPath.joinpath("defconcrt.txt")),70)]
        noconcRt70+=[np.percentile(np.loadtxt(clientEntryPath.joinpath("noconcrt.txt")),70)]
        wlessRt70+=[np.percentile(np.loadtxt(clientEntryPath.joinpath("wlessrt.txt")),70)]

        defconcRtAvg+=[np.mean(np.loadtxt(clientEntryPath.joinpath("defconcrt.txt")))]
        noconcRtAvg+=[np.mean(np.loadtxt(clientEntryPath.joinpath("noconcrt.txt")))]
        wlessRtAvg+=[np.mean(np.loadtxt(clientEntryPath.joinpath("wlessrt.txt")))]

        

        #get billable instance
        defcond_start=expdf[(expdf["modelname"]==m) & (expdf["exptype"]=="defconc") & (expdf["action"]=="start")]["time"].iloc[0]
        defcond_end=expdf[(expdf["modelname"]==m) & (expdf["exptype"]=="defconc") & (expdf["action"]=="end")]["time"].iloc[0]
        nocon_start=expdf[(expdf["modelname"]==m) & (expdf["exptype"]=="noconc") & (expdf["action"]=="start")]["time"].iloc[0]
        nocon_end=expdf[(expdf["modelname"]==m) & (expdf["exptype"]=="noconc") & (expdf["action"]=="end")]["time"].iloc[0]
        wlesscon_start=expdf[(expdf["modelname"]==m) & (expdf["exptype"]=="wlessconc") & (expdf["action"]=="start")]["time"].iloc[0]
        wlesscon_end=expdf[(expdf["modelname"]==m) & (expdf["exptype"]=="wlessend") & (expdf["action"]=="end")]["time"].iloc[0]


        defcond_start_date=datetime.fromtimestamp(defcond_start, tz=utc)-timedelta(days=0, hours=0, minutes=0)
        defcond_end_date=datetime.fromtimestamp(defcond_end, tz=utc)+timedelta(days=0, hours=0, minutes=2)

        nocon_start_date=datetime.fromtimestamp(nocon_start, tz=utc)-timedelta(days=0, hours=0, minutes=0)
        nocon_end_date=datetime.fromtimestamp(nocon_end, tz=utc)+timedelta(days=0, hours=0, minutes=0)

        wlesscon_start_date=datetime.fromtimestamp(wlesscon_start, tz=utc)-timedelta(days=0, hours=0, minutes=0)
        wlesscon_end_date=datetime.fromtimestamp(wlesscon_end, tz=utc)+timedelta(days=0, hours=0, minutes=2)

        defbill+=[np.trapz(df_bill[(df_bill["time"]>=defcond_start_date) & (df_bill["time"]<=defcond_end_date)]["values"].to_numpy())]
        noconcbill+=[np.trapz(df_bill[(df_bill["time"]>=nocon_start_date) & (df_bill["time"]<=nocon_end_date)]["values"].to_numpy())]
        wlessbill+=[np.trapz(df_bill[(df_bill["time"]>=wlesscon_start_date) & (df_bill["time"]<=wlesscon_end_date)]["values"].to_numpy())]

    defconcRt95=np.array(defconcRt95)
    noconcRt95=np.array(noconcRt95)
    wlessRt95=np.array(wlessRt95)

    defconcRt70=np.array(defconcRt70)
    noconcRt70=np.array(noconcRt70)
    wlessRt70=np.array(wlessRt70)

    defconcRtAvg=np.array(defconcRtAvg)
    noconcRtAvg=np.array(noconcRtAvg)
    wlessRtAvg=np.array(wlessRtAvg)

    defbill=np.array(defbill)
    noconcbill=np.array(noconcbill)
    wlessbill=np.array(wlessbill)

    savemat(resDir/Path("wless.mat"),{"defconcRt95":defconcRt95,"noconcRt95":noconcRt95,"wlessRt95":wlessRt95,
                         "defconcRt70":defconcRt70,"noconcRt70":noconcRt70,"wlessRt70":wlessRt70,
                         "defconcRtAvg":defconcRtAvg,"noconcRtAvg":noconcRtAvg,"wlessRtAvg":wlessRtAvg,
                        "defbill":defbill,"noconcbill":noconcbill,"wlessbill":wlessbill,"optCon":allOptCon})

if __name__ == '__main__':
    main(Path(__file__).parent.joinpath("results/"))