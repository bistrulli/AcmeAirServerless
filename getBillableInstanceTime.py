'''
curl command for gettinh the billablr time programmatically

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


def main():
    jdata=json.load(open("billingres.json","r"))
    trace=jdata["timeSeriesData"][0]["pointData"]
    df_bill=pd.DataFrame([[p["values"][0]["doubleValue"],p["timeInterval"]["startTime"]] for p in trace],columns=["values","time"])
    df_bill["time"]=pd.to_datetime(df_bill["time"])

    expdf=pd.read_csv("experiments.csv")

    defbill=[]
    noconcbill=[]
    wlessbill=[]

    defconcRt=[]
    noconcRt=[]
    wlessRt=[]

    allOptCon=[]

    models=list(set(expdf["modelname"].to_numpy()))
    for m in sorted(models):
        clientEntryPath=Path(m).joinpath("clientEntry")
        lqnModelPath=Path(m).joinpath(Path(m).name).joinpath("optSol.csv")

        optCon=pd.read_csv(lqnModelPath)
        allOptCon+=[optCon[["ncopt","ntopt"]].to_numpy()]

        defconcRt+=[np.percentile(np.loadtxt(clientEntryPath.joinpath("defconcrt.txt")),95)]
        noconcRt+=[np.percentile(np.loadtxt(clientEntryPath.joinpath("noconcrt.txt")),95)]
        wlessRt+=[np.percentile(np.loadtxt(clientEntryPath.joinpath("wlessrt.txt")),95)]

        

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

        #print(defcond_start_date,wlesscon_end_date)

        defbill+=[np.trapz(df_bill[(df_bill["time"]>=defcond_start_date) & (df_bill["time"]<=defcond_end_date)]["values"].to_numpy())]
        noconcbill+=[np.trapz(df_bill[(df_bill["time"]>=nocon_start_date) & (df_bill["time"]<=nocon_end_date)]["values"].to_numpy())]
        wlessbill+=[np.trapz(df_bill[(df_bill["time"]>=wlesscon_start_date) & (df_bill["time"]<=wlesscon_end_date)]["values"].to_numpy())]

        print(m,"\t",defcond_start_date.isoformat(),
                "\t",defcond_end_date.isoformat(),
                "\t",wlesscon_start_date.isoformat(),
                "\t",wlesscon_end_date.isoformat(),
                "\t",(defconcRt[-1]-wlessRt[-1])*100/wlessRt[-1])
    
    # plt.figure()
    # plt.boxplot(defconcRt,positions=[1])
    # plt.boxplot(noconcRt,positions=[2])
    # plt.boxplot(wlessRt,positions=[3])
    # plt.xticks([1,2,3], ["gcfDefault", "NoConc", "wLess"])
    # plt.grid()
    # plt.show()

    # plt.figure()
    # plt.boxplot(defbill,positions=[1])
    # plt.boxplot(noconcbill,positions=[2])
    # plt.boxplot(wlessbill,positions=[3])
    # plt.xticks([1,2,3], ["gcfDefault", "NoConc", "wLess"])
    # plt.grid()
    # plt.show()

    # plt.figure()
    # plt.scatter(defbill,defconcRt,label="gcfdefault")
    # plt.scatter(noconcbill,noconcRt,label="noconc")
    # plt.scatter(wlessbill,wlessRt,label="wless")
    # plt.grid()
    # plt.legend()
    # plt.xlabel("E2E RT 95th")
    # plt.ylabel("Billable Instnce")
    # plt.show()

    defconcRt=np.array(defconcRt)
    noconcRt=np.array(noconcRt)
    wlessRt=np.array(wlessRt)

    defbill=np.array(defbill)
    noconcbill=np.array(noconcbill)
    wlessbill=np.array(wlessbill)

    savemat("wless.mat",{"defconcRt":defconcRt,"noconcRt":noconcRt,"wlessRt":wlessRt,
                        "defbill":defbill,"noconcbill":noconcbill,"wlessbill":wlessbill,"optCon":allOptCon})


    # ratio1=np.divide((defconcRt-wlessRt),wlessRt)*100
    # ratio2=np.divide((noconcRt-wlessRt),wlessRt)*100

    # ratio3=np.divide((defbill-wlessbill),wlessbill)*100
    # ratio4=np.divide((noconcbill-wlessbill),wlessbill)*100

    # plt.figure()
    # plt.scatter(ratio1,ratio3,label="gcfdefault")
    # #plt.scatter(ratio2,ratio4,label="noconc")
    # plt.grid()
    # plt.legend()
    # #plt.ylim([-50,200])
    # plt.xlabel("E2E RT 95th")
    # plt.ylabel("Billable Instnce")
    # plt.show()

    # Create a gnuplot object
    #p = gp.Gnuplot()
    # Set the plot title and labels
    #p.title("Sine Wave")
    #p.xlabel("X")
    #p.ylabel("Y")

    # Plot the data using gnuplot commands
    #p.plot(x, y, with_="lines")  # "with_='lines'" specifies line plot style

    # Show the plot
    #p.show()

if __name__ == '__main__':
    main()