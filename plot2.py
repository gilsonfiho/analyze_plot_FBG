import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
from scipy.signal import find_peaks

# Carrega o CSV
file_path = 'cortex4_30_07_2024_08h_13h.pkl'
df = pd.read_pickle(file_path)

#print(df['FBG'].iloc[0]["FBG_0"])

fig , plots = plt.subplots(2)

for index,row in df.iterrows():
    data = row['FBG']

    if( row['vel_medida'] < 40):
        #Configurações do gráfico
        #plt.figure(figsize=(10, 6))

        peaks0, _ = find_peaks(data['FBG_0'], height = 0, threshold = 250, distance = 5)
        peaks1, _ = find_peaks(data['FBG_1'], height = 0, threshold = 250, distance = 5)
        peaks2, _ = find_peaks(data['FBG_2'], height = 0, threshold = 250, distance = 5)
        
        # Plotagem dos dados
        plots[0].plot(data['FBG_0'], label='FBG_0', color='blue')
        plots[0].scatter(x = peaks0, y = np.array(data['FBG_0'])[peaks0] , color='black')
        plots[0].plot(data['FBG_1'], label='FBG_1', color='green')
        plots[0].scatter(x = peaks1, y = np.array(data['FBG_1'])[peaks1] , color='black')
        plots[0].plot(data['FBG_2'], label='FBG_2', color='red')
        plots[0].scatter(x = peaks2, y = np.array(data['FBG_2'])[peaks2] , color='black')
        
        der1 = np.gradient(data['FBG_0'])
        der2 = np.gradient(data['FBG_1'])
        der3 = np.gradient(data['FBG_2'])

        peaks3, _ = find_peaks(der1, height = 0, threshold = 300, distance = 5)
        peaks4, _ = find_peaks(der2, height = 0, threshold = 300, distance = 5)
        peaks5, _ = find_peaks(der3, height = 0, threshold = 300, distance = 5)

        #Plotagem da Derivada
        plots[1].plot(der1, label='FBG_0', color='blue')
        #plots[1].scatter(x = peaks3, y = np.array(data['FBG_0'])[peaks3] , color='black')
        plots[1].plot(der2, label='FBG_1', color='green')
        #plots[1].scatter(x = peaks4, y = np.array(data['FBG_1'])[peaks4] , color='black')
        plots[1].plot(der3, label='FBG_2', color='red')
        #plots[1].scatter(x = peaks5, y = np.array(data['FBG_2'])[peaks5] , color='black')

        # Adiciona título e rótulos aos eixos
        plots[0].title.set_text(f'Dados das FBGs ao longo do Tempo. Velocidade:{row['vel_medida']}km/h')
        '''plots[0].xlabel('Tempo')
        plots[0].ylabel('Valores das FBGs')'''

        plots[1].title.set_text(f'Deriava das FBGs ao longo do Tempo.{data['Time'][(len(data['Time']))//2]}')
        '''plots[1].xlabel('Tempo')
        plots[1].ylabel('Valores das FBGs')'''

        plots[0].legend()
        plots[1].legend()
        plt.pause(0.5)
        plots[0].cla()
        plots[1].cla()