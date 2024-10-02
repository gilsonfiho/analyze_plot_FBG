import numpy as np
import matplotlib.pyplot as plt

# Dados fornecidos
deformacao = np.array([1979.49, 1568.80, 4031.05])
peso = np.array([2670,  1950,  4890, ])

# Definir o grau do polinômio
grau = 2  # Altere este valor para o grau desejado

# Cálculo dos coeficientes da regressão polinomial de grau n
coeficientes = np.polyfit(deformacao, peso, grau)

# Geração dos valores para a linha de regressão polinomial
deformacao_fit = np.linspace(min(deformacao), max(deformacao), 100)
peso_fit = np.polyval(coeficientes, deformacao_fit)

# Cálculo do coeficiente de correlação para a regressão polinomial
correlacao = np.corrcoef(deformacao, peso)[0, 1]

# Criação do gráfico
plt.figure(figsize=(10, 6))
plt.scatter(deformacao, peso, color='red', label=f'Dados Reais - Coeficiente: {correlacao:.4f}')
plt.plot(deformacao_fit, peso_fit, color='blue', label=f'Regressão Polinomial de Grau {grau}: ' + ' + '.join([f'{coef:.4f} * x^{grau-i}' for i, coef in enumerate(coeficientes)]))

plt.xlabel('Deformação (micrômetros por metro)')
plt.ylabel('Peso (quilogramas)')
plt.title(f'Relação entre Deformação e Peso - Regressão Polinomial de Grau {grau}')
plt.legend()
plt.grid(True)
plt.show()
