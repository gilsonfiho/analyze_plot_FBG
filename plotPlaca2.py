import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

# Caminho para a pasta contendo os arquivos PKL gerados
folder_path = r'C:\Users\Gilson\Downloads\Teste_Plot_Corte\filtered_by_placa'

# Listar todos os arquivos PKL na pasta
pkl_files = [f for f in os.listdir(folder_path) if f.endswith('.pkl')]

# Mapear os nomes das subplots para os FBGs
fbgs = ['FBG_0', 'FBG_1', 'FBG_2']
colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

for pkl_file in pkl_files:
    # Carregar o arquivo PKL
    file_path = os.path.join(folder_path, pkl_file)
    df = pd.read_pickle(file_path)
    
    # Verificar se o DataFrame não está vazio
    if len(df) == 0:
        continue
    
    # Criar uma figura para os subplots
    fig, ax = plt.subplots(3, 1, figsize=(12, 12), sharex=True)
    fig.suptitle(f'Veículo: {pkl_file.split("_")[0]} - Passagens Comparadas')

    for i, fbg in enumerate(fbgs):
        for index, row in df.iterrows():
            data = row['FBG']

            # Encontrar picos nos dados das FBGs
            peaks, _ = find_peaks(data[fbg], height=0, threshold=250, distance=5)

            # Plotagem dos dados das FBGs
            ax[i].plot(data[fbg], label=f'Passagem {index + 1}', color=colors[index % len(colors)])
            ax[i].scatter(x=peaks, y=np.array(data[fbg])[peaks], color='black')

        # Adicionar títulos e legendas
        ax[i].set_title(f'{fbg}')
        ax[i].set_xlabel('Tempo')
        ax[i].set_ylabel('Valores das FBGs')
        ax[i].legend()

    # Ajustar o layout e exibir o gráfico
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
