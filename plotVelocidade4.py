import os
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import matplotlib as plt

# Caminho para a pasta contendo os arquivos PKL gerados
folder_path = r'C:\Users\Gilson\Downloads\Teste_Plot_Corte\filtered_by_speed'

# Lista para armazenar as informações dos veículos
veiculos_data = []

# Processar cada arquivo PKL na pasta
for pkl_file in os.listdir(folder_path):
    if pkl_file.endswith('.pkl'):
        # Construir o caminho completo para o arquivo
        file_path = os.path.join(folder_path, pkl_file)
        print(f"Carregando arquivo: {file_path}")

        # Carregar o DataFrame
        df = pd.read_pickle(file_path)

        # Processar cada linha do DataFrame
        for index, row in df.iterrows():
            data = row['FBG']
            velocidade = row.get('vel_medida', 'Desconhecida')  # Usar velocidade como título

            # Filtrar veículos que possuem placa
            placa = row.get('placa_veiculo', '')
            if pd.isna(placa) or not placa:
                continue  # Ignorar veículos sem placa

            # Verificar se os dados são listas e converter para numpy arrays
            if isinstance(data['FBG_0'], list):
                data['FBG_0'] = np.array(data['FBG_0'])
            if isinstance(data['FBG_1'], list):
                data['FBG_1'] = np.array(data['FBG_1'])
            if isinstance(data['FBG_2'], list):
                data['FBG_2'] = np.array(data['FBG_2'])

            # Calcular o tempo esperado entre os picos com base na velocidade
            distancia_entre_eixos = 2.6
            tempo_entre_eixos = distancia_entre_eixos / velocidade  # Tempo em segundos
            sampling_rate = 1  # Supondo 1 amostra por segundo; ajustar conforme necessário
            distance_param = max(1, int(tempo_entre_eixos * sampling_rate))

            # Encontrar picos nos dados das FBGs
            peaks0, _ = find_peaks(data['FBG_0'], height=0, distance=distance_param)
            peaks1, _ = find_peaks(data['FBG_1'], height=0, distance=distance_param)
            peaks2, _ = find_peaks(data['FBG_2'], height=0, distance=distance_param)

            # Filtrar os dois maiores picos
            def filter_peaks(peaks, data):
                if len(peaks) == 0:
                    return np.array([]), np.array([])
                peak_values = data[peaks]
                sorted_indices = np.argsort(peak_values)[::-1]  # Ordenar os picos por valor
                top_indices = sorted_indices[:2]  # Pegando os dois maiores picos
                top_peaks = peaks[top_indices]
                return top_peaks, data[top_peaks]

            peaks0, values0 = filter_peaks(peaks0, data['FBG_0'])
            peaks1, values1 = filter_peaks(peaks1, data['FBG_1'])
            peaks2, values2 = filter_peaks(peaks2, data['FBG_2'])

            # Armazenar os dados processados
            veiculos_data.append({
                'passagem': index + 1,
                'velocidade': velocidade,
                'placa': placa,
                'picos_FBG_0': values0.tolist() if values0.size > 0 else [],
                'picos_FBG_1': values1.tolist() if values1.size > 0 else [],
                'picos_FBG_2': values2.tolist() if values2.size > 0 else []
            })

# Criar um DataFrame a partir da lista de dados dos veículos
output_df = pd.DataFrame(veiculos_data)

# Salvar os dados em um arquivo CSV
output_csv_path = os.path.join(folder_path, 'dados_processados.csv')
output_df.to_csv(output_csv_path, index=False)
print(f"Dados processados salvos em: {output_csv_path}")
