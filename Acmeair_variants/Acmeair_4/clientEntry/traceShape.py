from locust import  LoadTestShape
import subprocess
import math
import numpy as np
from scipy.io import loadmat

class traceShape(LoadTestShape):
    
    lastStage = None
    mod = None
    shift = None
    duration = None
    traceFile = None
    data = None
    
    def __init__(self,mod=400, shift=10, duration=600,traceFile="twitter_20210101_730-24_freq120sec.mat"):
        super().__init__()
        self.mod = mod
        self.shift =  shift
        self.duration = duration
        self.traceFile=traceFile
        #load trace data (for now in matlab format but in general I have to use a csv)
        self.data=loadmat(f"{self.traceFile}")["tweets"][0]
        self.maxIndex = len(self.data)
        #rescale the trace
        mx = max(self.data)
        mn = min(self.data)
        self.data = [(v - mn)/(mx-mn)*self.mod+self.shift for v in self.data]

    def tick(self):
        run_time = self.get_run_time()
        if run_time <= self.duration:
            if(int(run_time) % 30==0):
                self.users=(self.f(int(run_time)), 1)
            return self.users 
        return None
    
    def f(self,x):
        return self.data[int(x) % self.maxIndex]