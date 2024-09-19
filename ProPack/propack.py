import numpy as np
import random
import math
from scipy.optimize import curve_fit, minimize
from functools import partial
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("-datafile", help="Path of the input csv")
args = parser.parse_args()

datapath = args.datafile
if(not Path(datapath).exists()):
    raise ValueError(f"{datapath} does not exsits")

data = np.genfromtxt(datapath, delimiter=',')
concurrency = data[1:,0]
exectime = data[1:,1]

# ProPack assume di conoscere C, il numero di richieste concorrenti da servire,
# per calcolare il numero totale di istanze che servirebbero con concorrenza=1
# Non avendo questa informazione, metto qui il numero massimo di istanze che
# il provider consente di avviare
MAX_INSTANCES=1024
MAX_CONCURRENCY=concurrency.max()
cost_per_unit_of_time = 0.001 # irrilevante

def rt_model (conc, alpha):
    return np.exp(alpha*conc)

# curve fit
alpha, _ = curve_fit(rt_model, concurrency, exectime)
rt_model = lambda x: np.exp(alpha*x) # fix alpha

# Optimal for RT (sappiamo gia' che e' 1)
opt_rt = int(minimize(rt_model, x0=MAX_CONCURRENCY, bounds=[(1, MAX_CONCURRENCY)]).x[0])
print(f"Optimal for RT: {opt_rt}")

cost_model = lambda conc: rt_model(conc) * cost_per_unit_of_time * MAX_INSTANCES/conc
opt_cost = int(minimize(cost_model, x0=MAX_CONCURRENCY, bounds=[(1, MAX_CONCURRENCY)]).x[0])
print(f"Optimal for cost: {opt_cost}")

delta_rt = lambda conc: (rt_model(conc)-rt_model(opt_rt))/rt_model(opt_rt)
delta_cost = lambda conc: (cost_model(conc)-cost_model(opt_cost))/cost_model(opt_cost)
obj = lambda conc: delta_rt(conc)*0.5 + delta_cost(conc)*0.5
opt = int(minimize(obj, x0=MAX_CONCURRENCY, bounds=[(1, MAX_CONCURRENCY)]).x[0])
print(f"Multi-objective sol: {opt}")
