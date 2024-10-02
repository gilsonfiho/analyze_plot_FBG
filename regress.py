import numpy as np
import matplotlib.pyplot as plt

# Dados fornecidos
'''
deformacao = np.array([2161.37 , 1910.12 , 1866.99, 1548.21, 1677.9 ,1480.28 , 3970.81, 4042.18 ,4080.15])
peso = np.array([2670, 2670, 2670,  1950, 1950, 1950, 4890, 4890, 4890])
'''
'''
deformacao = np.array([1979.49, 1568.80, 4031.05])
peso = np.array([2670,  1950,  4890, ])
'''

deformacao = np.array([2161.37 , 1910.12 , 1866.99, 1548.21, 1677.9 ,1480.28 , 3970.81, 4042.18 ,4080.15])
peso = np.array([5500, 5500, 5500,  3500, 3500, 3500,  7700,  7700,  7700])

'''
deformacao = np.array([1979.49, 1568.80, 4031.05])
peso = np.array([5000,  3500,  7700 ])
'''

# Cálculo dos coeficientes da regressão linear
a, b = np.polyfit(deformacao, peso, 1)

# Geração dos valores para a linha de regressão
deformacao_fit = np.linspace(min(deformacao), max(deformacao), 100)
peso_fit = a * deformacao_fit + b

correlacao = np.corrcoef(deformacao, peso)[0, 1]

# Criação do gráfico
plt.figure(figsize=(10, 6))
plt.scatter(deformacao, peso, color='red', label=f'Dados Reais - Coeficiente: {correlacao:.4f}')
plt.plot(deformacao_fit, peso_fit, color='blue', label=f'Regressão Linear: Peso = {a:.4f} * Deformação + {b:.2f}')


plt.xlabel('Deformação (micrômetros por metro)')
plt.ylabel('Peso (quilogramas)')
plt.title('Relação entre Deformação e Peso')
plt.legend()
plt.grid(True)
plt.show()
