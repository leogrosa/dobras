import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdb
from mpl_toolkits.mplot3d import Axes3D
import concurrent.futures

i_max = 50
step = 20
max_size = 10000
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

def dimension_sweep(m, n, i_max, c, l, espessura):
    e = espessura.copy()
    i = calculate_foldings(i_max, c[:,m], l[:,n], e)
    current_results = np.array([c[0, m], l[0, n], e[i], i]).T
    return current_results

def calculate_foldings(i_max, c, l, e):
    for i in range(i_max-1):
        if c[i] > l[i]:
            c[i+1] = c[i]/2 - e[i]
            l[i+1] = l[i]
        else:
            c[i+1] = c[i]
            l[i+1] = l[i]/2 - e[i]
        if any([value < 0 for value in [c[i+1], l[i+1]]]):
            return i
        e[i+1] = 2*e[i]

threads_results = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    for m, comprimento in enumerate(c[0,:]):
        for n, largura in enumerate(l[0,:]):
            threads_results.append(executor.submit(dimension_sweep, m, n, i_max, c, l, e))
    executor.shutdown()
    concurrent.futures.wait(threads_results)

final_results = [r.result() for r in threads_results]
results = pd.DataFrame([r.result() for r in threads_results], columns=columns)

# Plotagem
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

X, Y = np.meshgrid(results['c'].unique(), results['l'].unique())
Z = results.pivot(index='c', columns='l', values='i').values

ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_xlabel('Comprimento')
ax.set_ylabel('Largura')
ax.set_zlabel('Iterações')

plt.show()
