import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

# Caminho para a pasta contendo os arquivos PKL gerados
folder_path = r'C:\Users\Gilson\Downloads\Teste_Plot_Corte\filtered_by_placa'

# Listar todos os arquivos PKL na pasta
pkl_files = [f for f in os.listdir(folder_path) if f.endswith('.pkl')]

# Distância média entre eixos em metros
distancia_entre_eixos = 2.6

# Percorrer cada arquivo PKL na pasta
for pkl_file in pkl_files:
    # Carregar o arquivo PKL
    file_path = os.path.join(folder_path, pkl_file)
    df = pd.read_pickle(file_path)
    
    # Verificar se o DataFrame não está vazio
    if len(df) == 0:
        continue
    
    # Percorrer cada linha do DataFrame
    for index, row in df.iterrows():
        data = row['FBG']
        placa = row.get('placa', 'Desconhecida')  # Adicionar a placa ao título

        # Verificar se a coluna 'vel_medida' existe no DataFrame
        if 'vel_medida' in row:
            velocidade = row['vel_medida']  # Velocidade em metros por segundo
        else:
            print(f"Aviso: A coluna 'vel_medida' não foi encontrada no arquivo {pkl_file}.")
            continue  # Pular esta iteração se a velocidade não estiver presente
        
        # Calcular o tempo esperado entre os picos com base na velocidade
        tempo_entre_eixos = distancia_entre_eixos / velocidade  # Tempo em segundos
        
        # Converter o tempo para a escala do índice dos dados (assumindo que os dados são medidos em tempo real)
        sampling_rate = 1  # Supondo 1 amostra por segundo; ajustar conforme necessário
        distance_param = max(1, int(tempo_entre_eixos * sampling_rate))  # Garantir que seja pelo menos 1

        # Definir o número de eixos esperado (ajuste conforme necessário)
        numero_eixos = 2  # Supondo 2 eixos por veículo

        # Encontrar picos nos dados das FBGs
        peaks0, _ = find_peaks(data['FBG_0'], height=0, distance=distance_param)
        peaks1, _ = find_peaks(data['FBG_1'], height=0, distance=distance_param)
        peaks2, _ = find_peaks(data['FBG_2'], height=0, distance=distance_param)

        # Verificar se encontramos exatamente o número de picos esperado
        if len(peaks0) == numero_eixos and len(peaks1) == numero_eixos and len(peaks2) == numero_eixos:
            # Plotar os dados e os picos identificados
            plt.figure(figsize=(12, 6))
            plt.plot(data['FBG_0'], label='FBG_0', color='blue')
            plt.scatter(x=peaks0, y=np.array(data['FBG_0'])[peaks0], color='black', zorder=5)
            plt.plot(data['FBG_1'], label='FBG_1', color='green')
            plt.scatter(x=peaks1, y=np.array(data['FBG_1'])[peaks1], color='black', zorder=5)
            plt.plot(data['FBG_2'], label='FBG_2', color='red')
            plt.scatter(x=peaks2, y=np.array(data['FBG_2'])[peaks2], color='black', zorder=5)

            # Adicionar título e legendas
            plt.title(f'Placa: {placa} | Velocidade: {velocidade:.2f} m/s - Passagem {index + 1}')
            plt.xlabel('Tempo')
            plt.ylabel('Valores das FBGs')
            plt.legend()

            # Exibir o gráfico
            plt.show()

# Mantém os gráficos abertos até que o usuário os feche
plt.show()
