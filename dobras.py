import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdb
from mpl_toolkits.mplot3d import Axes3D

i_max = 50
step = 100
max_size = 500
c_max = max_size + step
l_max = max_size + step
e0 = 0.1

# Vetores
c = np.zeros([i_max, round(c_max/step)])
c[0,:] = np.arange(0, c_max, step)
l = np.zeros([i_max, round(c_max/step)])
l[0,:] = np.arange(0, l_max, step)
e = np.zeros(i_max)
e[0] = e0

columns = ['c', 'l', 'e', 'i']
results = pd.DataFrame(columns=columns)

# Processo iterativo
for m, comprimento in enumerate(c[0,:]):
    for n, largura in enumerate(l[0,:]):
        for i in range(i_max-1):
            if c[i,m] > l[i,n]:
                c[i+1,m] = c[i,m]/2 - e[i]
                l[i+1,n] = l[i,n]
            else:
                c[i+1,m] = c[i,m]
                l[i+1,n] = l[i,n]/2 - e[i]
            if any([value < 0 for value in [c[i+1,m], l[i+1,n]]]):
                current_results = pd.DataFrame([comprimento, largura, e[i], i]).T 
                current_results.columns = columns
                results = pd.concat([results, \
                                         current_results],\
                                         ignore_index=True)
                break
            e[i+1] = 2*e[i]

# Plotagem

