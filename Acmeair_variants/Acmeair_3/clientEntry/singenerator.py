import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import savemat
from scipy.io import loadmat

optCore=loadmat("optCore_high.mat")

fiNT=optCore["optCore"]["fiNT"][0][0]
fiRep=optCore["optCore"]["fiRep"][0][0]


mod = 200
shift = 10
period = 1200 / (2*math.pi)

  
def f(x):
    return max(math.sin(x/period)*mod,0)+shift

x=np.linspace(0,3600,60)
y=[int(f(i)) for i in range(0,3600,60)]

# plt.figure()
# plt.step(x,y)
# plt.show()

stages = []
for i in range(len(y)-1):
    stages+=[{"duration": int(x[i+1]), "users": y[i], "spawn_rate": 1, "functions":["f3","f4"],"Rep":fiRep[i,:].tolist(),"Conc":fiNT[i,:].tolist()}]

print(stages)

#savemat("gcfwork.mat",{"pop":y})
    

