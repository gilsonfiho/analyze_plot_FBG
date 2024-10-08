import pandas as pd
import matplotlib.pyplot as plt

# Dados fornecidos
data = {
    'Time': [pd.Timestamp('2024-07-09 16:04:33.000195'), pd.Timestamp('2024-07-09 16:04:33.000352'), pd.Timestamp('2024-07-09 16:04:33.000547'), pd.Timestamp('2024-07-09 16:04:33.000781'), pd.Timestamp('2024-07-09 16:04:33.000977'), pd.Timestamp('2024-07-09 16:04:33.001133'), pd.Timestamp('2024-07-09 16:04:33.001367'), pd.Timestamp('2024-07-09 16:04:33.001523'), pd.Timestamp('2024-07-09 16:04:33.001719'), pd.Timestamp('2024-07-09 16:04:33.001914'), pd.Timestamp('2024-07-09 16:04:33.002148'), pd.Timestamp('2024-07-09 16:04:33.002344'), pd.Timestamp('2024-07-09 16:04:33.002539'), pd.Timestamp('2024-07-09 16:04:33.002734'), pd.Timestamp('2024-07-09 16:04:33.002891'), pd.Timestamp('2024-07-09 16:04:33.003086'), pd.Timestamp('2024-07-09 16:04:33.003281'), pd.Timestamp('2024-07-09 16:04:33.003477'), pd.Timestamp('2024-07-09 16:04:33.003711'), pd.Timestamp('2024-07-09 16:04:33.003906'), pd.Timestamp('2024-07-09 16:04:33.004062'), pd.Timestamp('2024-07-09 16:04:33.004297'), pd.Timestamp('2024-07-09 16:04:33.004492'), pd.Timestamp('2024-07-09 16:04:33.004687'), pd.Timestamp('2024-07-09 16:04:33.004883'), pd.Timestamp('2024-07-09 16:04:33.005078'), pd.Timestamp('2024-07-09 16:04:33.005273'), pd.Timestamp('2024-07-09 16:04:33.005469'), pd.Timestamp('2024-07-09 16:04:33.005664'), pd.Timestamp('2024-07-09 16:04:33.005859'), pd.Timestamp('2024-07-09 16:04:33.006055'), pd.Timestamp('2024-07-09 16:04:33.006250'), pd.Timestamp('2024-07-09 16:04:33.006445'), pd.Timestamp('2024-07-09 16:04:33.006641'), pd.Timestamp('2024-07-09 16:04:33.006836'), pd.Timestamp('2024-07-09 16:04:33.007031'), pd.Timestamp('2024-07-09 16:04:33.007227'), pd.Timestamp('2024-07-09 16:04:33.007422'), pd.Timestamp('2024-07-09 16:04:33.007617'), pd.Timestamp('2024-07-09 16:04:33.007812'), pd.Timestamp('2024-07-09 16:04:33.008047'), pd.Timestamp('2024-07-09 16:04:33.008203'), pd.Timestamp('2024-07-09 16:04:33.008398'), pd.Timestamp('2024-07-09 16:04:33.008594'), pd.Timestamp('2024-07-09 16:04:33.008828'), pd.Timestamp('2024-07-09 16:04:33.009102'), pd.Timestamp('2024-07-09 16:04:33.009297'), pd.Timestamp('2024-07-09 16:04:33.009492'), pd.Timestamp('2024-07-09 16:04:33.009687'), pd.Timestamp('2024-07-09 16:04:33.009883')],
    'SystemTemperature(°C)': [52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.55, 52.55, 52.55, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.56, 52.55, 52.55, 52.55, 52.55, 52.55, 52.55, 52.55, 52.55, 52.56, 52.56, 52.56, 52.56, 52.55, 52.55, 52.55, 52.55, 52.55, 52.56, 52.56],
    'FBG_0': [32.2179, 121.5729, 4.9278, 25.3663, 92.7354, 140.2387, -62.4807, 48.3425, -3.3509, -22.9301, 6.2583, 11.5013, 89.6719, -111.7976, -78.3412, 91.3791, -26.1807, 57.6756, -25.4556, 107.2256, -141.9534, 126.7928, 46.8594, 104.8878, 23.1493, 7.9266, -7.702, -57.5334, 175.926, -52.4283, 13.5395, 66.9812, 13.3312, 136.3213, 195.2217, -48.2725, 68.8058, 111.9235, 85.872, 83.6927, 5.9136, 58.2093, 110.4798, 112.8593, 98.0286, 54.5887, 124.6668, -15.9496, 100.2707, 42.8072],
    'FBG_1': [166.1034, 53.4398, 52.2539, 223.3024, 64.2362, -89.229, 127.9489, 299.8327, -274.2702, 43.4686, 179.5988, 68.0306, 12.2157, 282.3937, 63.3828, 51.8603, -14.9627, 150.3544, 249.6077, 595.1861, 106.6321, 151.6191, 116.5717, 19.5182, 178.277, 113.66, -78.4752, 65.4967, 219.2845, 18.2116, 23.4499, 32.4008, -71.3309, 74.8815, -33.7907, -21.3646, 246.2211, 50.6151, 134.7341, 18.9267, 103.2757, 70.8339, 274.6275, 129.9299, 25.4978, 129.7687, 21.9793, -4.5736, 15.5928, 11.9351],
    'FBG_2': [76.9273, 34.7744, 4.8839, 37.1892, 189.9373, -19.2979, 90.6116, -34.6393, 135.2127, -106.6444, -26.3817, 151.1347, 106.5274, -39.5154, 21.1926, 19.0042, 0.428, -8.3525, 75.4258, 122.0843, 11.8438, -19.2577, 4.1499, -78.8584, 180.4902, 48.591, -25.7332, -166.4876, 120.3286, -72.2193, -2.3892, 153.2466, 81.703, -7.0206, -140.8927, 19.8381, 142.3556, 84.9228, -63.504, -68.4318, -35.8565, 4.236, -75.4115, -20.9117, 84.9645, -6.6478, -136.1865, 79.8947, -179.491, -57.0707]
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