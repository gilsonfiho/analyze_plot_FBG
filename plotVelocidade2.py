import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

# Caminho para a pasta contendo os arquivos PKL gerados
folder_path = r'C:\Users\Gilson\Downloads\Teste_Plot_Corte\filtered_by_speed'

pkl_file = 'veiculos_18kmh_23_veiculos.pkl'  # Substitua pelo nome do arquivo desejado

# Construir o caminho completo para o arquivo
file_path = os.path.join(folder_path, pkl_file)
print(f"Carregando arquivo: {file_path}")

# Verificar se o arquivo existe
if not os.path.exists(file_path):
    print(f"Erro: O arquivo {file_path} não foi encontrado.")
else:
    df = pd.read_pickle(file_path)
    print("Arquivo carregado com sucesso!")

    # Verificar se o DataFrame não está vazio
    if df.empty:
        print("O arquivo selecionado está vazio.")
    else:
        print("Iniciando a plotagem...")

        # Distância média entre eixos em metros
        distancia_entre_eixos = 2.6

        # Percorrer cada linha do DataFrame
        for index, row in df.iterrows():
            data = row['FBG']
            velocidade = row.get('vel_medida', 'Desconhecida')  # Usar velocidade como título

            # Filtrar veículos que possuem placa
            placa = row.get('placa_veiculo', '')
            if pd.isna(placa) or not placa:
                continue  # Ignorar veículos sem placa

            print(f"Processando linha {index + 1} com velocidade {velocidade} m/s")

            # Verificar se os dados são listas e converter para numpy arrays
            if isinstance(data['FBG_0'], list):
                data['FBG_0'] = np.array(data['FBG_0'])
            if isinstance(data['FBG_1'], list):
                data['FBG_1'] = np.array(data['FBG_1'])
            if isinstance(data['FBG_2'], list):
                data['FBG_2'] = np.array(data['FBG_2'])

            # Calcular o tempo esperado entre os picos com base na velocidade
            tempo_entre_eixos = distancia_entre_eixos / velocidade  # Tempo em segundos

            # Converter o tempo para a escala do índice dos dados
            sampling_rate = 1  # Supondo 1 amostra por segundo; ajustar conforme necessário
            distance_param = max(1, int(tempo_entre_eixos * sampling_rate))

            # Encontrar picos nos dados das FBGs
            peaks0, _ = find_peaks(data['FBG_0'], height=0, distance=distance_param)
            peaks1, _ = find_peaks(data['FBG_1'], height=0, distance=distance_param)
            peaks2, _ = find_peaks(data['FBG_2'], height=0, distance=distance_param)

            # Filtrar os dois maiores picos, considerando a variação
            def filter_peaks(peaks, data):
                if len(peaks) == 0:
                    return [], [], []
                peak_values = data[peaks]
                sorted_indices = np.argsort(peak_values)[::-1]  # Ordenar os picos por valor
                top_indices = sorted_indices[:2]  # Pegando os dois maiores picos
                top_peaks = peaks[top_indices]
                top_values = peak_values[top_indices]
                variations = top_values - data[top_peaks - 1]  # Calcular a variação em relação ao valor anterior
                if len(top_peaks) > 1 and (top_values[0] - top_values[1]) >= 400:
                    return top_peaks, top_values, variations
                return [], [], []

            peaks0, values0, variations0 = filter_peaks(peaks0, data['FBG_0'])
            peaks1, values1, variations1 = filter_peaks(peaks1, data['FBG_1'])
            peaks2, values2, variations2 = filter_peaks(peaks2, data['FBG_2'])

            print(f"Peaks filtrados - FBG_0: {len(peaks0)}, FBG_1: {len(peaks1)}, FBG_2: {len(peaks2)}")
            print(f"Variações dos picos - FBG_0: {variations0}, FBG_1: {variations1}, FBG_2: {variations2}")

            if len(peaks0) > 0 or len(peaks1) > 0 or len(peaks2) > 0:
                # Adicionar isto para fechar todas as figuras abertas antes de criar uma nova
                plt.close('all')

                # Plotar os dados e os picos identificados
                plt.figure(figsize=(12, 6))
                plt.plot(data['FBG_0'], label='FBG_0', color='blue')
                plt.scatter(x=peaks0, y=np.array(data['FBG_0'])[peaks0], color='black', zorder=5, label=f'Picos FBG_0 (variações: {variations0})')
                plt.plot(data['FBG_1'], label='FBG_1', color='green')
                plt.scatter(x=peaks1, y=np.array(data['FBG_1'])[peaks1], color='black', zorder=5, label=f'Picos FBG_1 (variações: {variations1})')
                plt.plot(data['FBG_2'], label='FBG_2', color='red')
                plt.scatter(x=peaks2, y=np.array(data['FBG_2'])[peaks2], color='black', zorder=5, label=f'Picos FBG_2 (variações: {variations2})')

                # Adicionar título com placa e velocidade
                plt.title(f'Placa: {placa} - Velocidade: {velocidade:.2f} km/h - Passagem {index + 1}')
                plt.xlabel('Tempo')
                plt.ylabel('Valores das FBGs')
                plt.legend()

                # Exibir o gráfico
                plt.show()

                # Pausa para visualizar o gráfico antes de continuar
                input("Pressione Enter para continuar para o próximo gráfico...")

        print("Plotagem concluída.")
