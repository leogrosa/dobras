import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdb
from mpl_toolkits.mplot3d import Axes3D
import concurrent.futures

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
    return 0

i_max = 50

## Cálculo para A4
c = np.zeros(i_max)
l = np.zeros(i_max)
e = np.zeros(i_max)
c[0] = 297
l[0] = 210
e[0] = 0.1

result = calculate_foldings(i_max, c, l, e)

# Plot A4
plt.figure()
plt.grid(True)
plt.plot(c[:result+2], label='Comprimento')
plt.plot(l[:result+2], label='Largura')
plt.plot(e[:result+2], label='Espessura')
plt.axvline(x=result, color='r', linestyle='--', label='Iteração final')
plt.legend()

plt.figure()
plt.grid(True)
plt.plot(e[:result+2], label='Espessura')
plt.axvline(x=result, color='r', linestyle='--', label='Iteração final')
plt.legend()

# plt.show()

## Cálculo para encontrar tamanho do papel que chega na lua 
# Vetores
columns = ['c', 'l', 'e', 'i']

q = 1.075
c0 = 0.297*(2**42)
l0 = 0.210*(2**42)
e0 = 0.0001
n_termos = 100

pg_c = np.geomspace(c0, c0 * q**(n_termos-1), n_termos)
pg_l = np.geomspace(l0, l0 * q**(n_termos-1), n_termos)

c = np.zeros([i_max, n_termos])
c[0,:] = pg_c
l = np.zeros([i_max, n_termos])
l[0,:] = pg_l

e = np.zeros(i_max)
e[0] = e0

threads_results = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    for m, comprimento in enumerate(c[0,:]):
            threads_results.append(executor.submit(dimension_sweep, m, m, i_max, c, l, e))
    executor.shutdown()
    concurrent.futures.wait(threads_results)

final_results = [r.result() for r in threads_results]
results = pd.DataFrame([r.result() for r in threads_results], columns=columns)

distancia_terra_lua_em_metros = 384400000

# Plotagem
fig, ax1 = plt.subplots()

ax1.plot(results.index, results['e'], label='Espessura', color='r')
ax1.set_xlabel(f'Expoente da razão {q}: 2^42 * {q}^x')
ax1.set_ylabel('Espessura')
ax1.tick_params(axis='y')
ax1.axhline(y=distancia_terra_lua_em_metros, color='r', linestyle='--', label='Distância Terra-Lua')
ax1.legend()

ax2 = ax1.twinx()
ax2.plot(results.index, results['i'], color='b', label='Número de dobras')
ax2.set_ylabel('Número de dobras')
ax2.tick_params(axis='y')
ax2.legend()

fig.tight_layout()
plt.grid(True)
# plt.show()

## Cálculo para varredura de dimensões
step = 20
max_size = 10000
c_max = max_size + step
l_max = max_size + step

# Vetores
c = np.zeros([i_max, round(c_max/step)])
c[0,:] = np.arange(0, c_max, step)
l = np.zeros([i_max, round(c_max/step)])
l[0,:] = np.arange(0, l_max, step)
e = np.zeros(i_max)
e[0] = e0


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
ax.set_zlabel('Número de dobras')

plt.show()
