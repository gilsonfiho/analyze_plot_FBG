import pandas as pd
import matplotlib.pyplot as plt

# Dados fornecidos
data = {
}

# Cria o DataFrame
df = pd.DataFrame(data, columns=['Time', 'SystemTemperature(°C)', 'FBG_0', 'FBG_1', 'FBG_2'])

# Configurações do gráfico
plt.figure(figsize=(10, 6))

# Plotagem dos dados
plt.plot(df['Time'], df['FBG_0'], label='FBG_0', color='blue')
plt.plot(df['Time'], df['FBG_1'], label='FBG_1', color='green')
plt.plot(df['Time'], df['FBG_2'], label='FBG_2', color='red')

# Adiciona título e rótulos aos eixos
plt.title('Dados das FBGs ao longo do Tempo')
plt.xlabel('Tempo')
plt.ylabel('Valores das FBGs')

# Adiciona uma grade ao gráfico
plt.grid(True)

# Adiciona a legenda
plt.legend()

# Exibe o gráfico
plt.show()