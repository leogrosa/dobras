import matplotlib.pyplot as plt
import numpy as np

n_max = 100

# Vetores de dimensões
c = np.zeros(n_max)
l = np.zeros(n_max)
e = np.zeros(n_max)

# Condições iniciais
c[0] = 297
l[0] = 210
e[0] = 0.1

begin_fold_in_bigger_size = input('Começar dobrando no maior lado? (s/n) ') == 's'

size_choice = {True: 1, False: 0}

# Processo iterativo
for i in range(n_max-1):
    if (i + size_choice[begin_fold_in_bigger_size]) % 2 == 0:
        c[i+1] = c[i]/2 - e[i]
        l[i+1] = l[i]
    else:
        c[i+1] = c[i]
        l[i+1] = l[i]/2 - e[i]
    if any([value < 0 for value in [c[i+1], l[i+1]]]):
        break
    e[i+1] = 2*e[i]

# Plotagem
plt.plot(c, label='Comprimento')
plt.plot(l, label='Largura')
plt.plot(e, label='Espessura')
plt.legend()
plt.show()
    

