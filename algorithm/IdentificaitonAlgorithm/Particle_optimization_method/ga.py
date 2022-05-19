
import numpy as np
from geneticalgorithm import geneticalgorithm as ga

def Evaluation_Function(Mu):
    g=abs(Mu[0]-5)+4*abs(Mu[1]+3)
    return g

varbound=np.array([[1,8],[-5,-2]])
model=ga(function=Evaluation_Function,dimension=2,variable_type='real',variable_boundaries=varbound)
model.run()

