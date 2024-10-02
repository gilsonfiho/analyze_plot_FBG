import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

# Caminho para a pasta contendo os arquivos PKL gerados
folder_path = r'C:\Users\Gilson\Downloads\Teste_Plot_Corte\filtered_by_placa'

# Listar todos os arquivos PKL na pasta
pkl_files = [f for f in os.listdir(folder_path) if f.endswith('.pkl')]

for pkl_file in pkl_files:
    # Carregar o arquivo PKL
    file_path = os.path.join(folder_path, pkl_file)
    df = pd.read_pickle(file_path)
    
    # Verificar se o DataFrame não está vazio
    if len(df) == 0:
        continue
    
    # Criar uma figura para os subplots
    fig, ax = plt.subplots(len(df), 1, figsize=(12, len(df) * 4))
    fig.suptitle(f'Veículo: {pkl_file.split("_")[0]} - Passagens Comparadas')

    if len(df) == 1:
        ax = [ax]  # Garantir que ax seja uma lista mesmo com um subplot único
    
    for i, (index, row) in enumerate(df.iterrows()):
        data = row['FBG']

        # Encontrar picos nos dados das FBGs
        peaks0, _ = find_peaks(data['FBG_0'], height=0, threshold=250, distance=5)
        peaks1, _ = find_peaks(data['FBG_1'], height=0, threshold=250, distance=5)
        peaks2, _ = find_peaks(data['FBG_2'], height=0, threshold=250, distance=5)

        # Plotagem dos dados das FBGs
        ax[i].plot(data['FBG_0'], label='FBG_0', color='blue')
        ax[i].scatter(x=peaks0, y=np.array(data['FBG_0'])[peaks0], color='black')
        ax[i].plot(data['FBG_1'], label='FBG_1', color='green')
        ax[i].scatter(x=peaks1, y=np.array(data['FBG_1'])[peaks1], color='black')
        ax[i].plot(data['FBG_2'], label='FBG_2', color='red')
        ax[i].scatter(x=peaks2, y=np.array(data['FBG_2'])[peaks2], color='black')

        # Adicionar títulos e legendas
        ax[i].set_title(f'Passagem {i + 1}')
        ax[i].set_xlabel('Tempo')
        ax[i].set_ylabel('Valores das FBGs')
        ax[i].legend()

    # Ajustar o layout e exibir o gráfico
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
