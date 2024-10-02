import numpy as np
import matplotlib.pyplot as plt

# Dados fornecidos

deformacao = np.array([3226.72, 3844.87, 6101.66])
peso = np.array([3660,  3900,  4890])


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
