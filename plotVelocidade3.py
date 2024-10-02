import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

# Caminho para a pasta contendo os arquivos PKL gerados
folder_path = r'C:\Users\Gilson\Downloads\Teste_Plot_Corte\filtered_by_speed'
pkl_file = 'veiculos_33kmh_606_veiculos.pkl'  # Substitua pelo nome do arquivo desejado

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
                    return [], []
                peak_values = data[peaks]
                sorted_indices = np.argsort(peak_values)[::-1]  # Ordenar os picos por valor
                top_indices = sorted_indices[:2]  # Pegando os dois maiores picos
                top_peaks = peaks[top_indices]
                if len(top_peaks) > 1 and (data[top_peaks[0]] - data[top_peaks[1]]) >= 400:
                    return top_peaks, data[top_peaks]
                return [], []

            peaks0, values0 = filter_peaks(peaks0, data['FBG_0'])
            peaks1, values1 = filter_peaks(peaks1, data['FBG_1'])
            peaks2, values2 = filter_peaks(peaks2, data['FBG_2'])

            print(f"Peaks filtrados - FBG_0: {len(peaks0)}, FBG_1: {len(peaks1)}, FBG_2: {len(peaks2)}")

            # Encontrar picos na derivada do sinal
            def find_derivative_peaks(signal, distance_param):
                deriv = np.diff(signal)
                deriv_peaks, _ = find_peaks(deriv, height=0, distance=distance_param)
                return deriv_peaks, deriv

            deriv_peaks0, deriv_fbg0 = find_derivative_peaks(data['FBG_0'], distance_param)
            deriv_peaks1, deriv_fbg1 = find_derivative_peaks(data['FBG_1'], distance_param)
            deriv_peaks2, deriv_fbg2 = find_derivative_peaks(data['FBG_2'], distance_param)

            # Filtrar os dois maiores picos da derivada
            deriv_peaks0, deriv_values0 = filter_peaks(deriv_peaks0, deriv_fbg0)
            deriv_peaks1, deriv_values1 = filter_peaks(deriv_peaks1, deriv_fbg1)
            deriv_peaks2, deriv_values2 = filter_peaks(deriv_peaks2, deriv_fbg2)

            print(f"Picos da derivada filtrados - FBG_0: {len(deriv_peaks0)}, FBG_1: {len(deriv_peaks1)}, FBG_2: {len(deriv_peaks2)}")

            if len(peaks0) > 0 or len(peaks1) > 0 or len(peaks2) > 0:
                # Adicionar isto para fechar todas as figuras abertas antes de criar uma nova
                plt.close('all')

                # Plotar os dados e os picos identificados
                plt.figure(figsize=(12, 12))

                # Sinal original
                plt.subplot(2, 1, 1)
                plt.plot(data['FBG_0'], label='FBG_0', color='blue')
                plt.scatter(x=peaks0, y=data['FBG_0'][peaks0], color='black', zorder=5, label='Picos FBG_0')
                plt.plot(data['FBG_1'], label='FBG_1', color='green')
                plt.scatter(x=peaks1, y=data['FBG_1'][peaks1], color='black', zorder=5, label='Picos FBG_1')
                plt.plot(data['FBG_2'], label='FBG_2', color='red')
                plt.scatter(x=peaks2, y=data['FBG_2'][peaks2], color='black', zorder=5, label='Picos FBG_2')

                # Adicionar título com placa, velocidade e valores dos picos
                def format_peak_info(peaks, values):
                    return ', '.join([f'Pico {i+1}: {values[i]:.2f}' for i in range(len(values))])

                peak_info0 = format_peak_info(peaks0, values0) if len(values0) > 0 else 'Nenhum pico significativo'
                peak_info1 = format_peak_info(peaks1, values1) if len(values1) > 0 else 'Nenhum pico significativo'
                peak_info2 = format_peak_info(peaks2, values2) if len(values2) > 0 else 'Nenhum pico significativo'

                plt.title(f'Placa: {placa} - Velocidade: {velocidade:.2f} km/h - Passagem {index + 1}\n'
                          f'FBG_0: {peak_info0} | FBG_1: {peak_info1} | FBG_2: {peak_info2}')
                plt.xlabel('Tempo')
                plt.ylabel('Valores das FBGs')
                plt.legend()

                # Derivada do sinal
                plt.subplot(2, 1, 2)
                plt.plot(deriv_fbg0, label='Derivada FBG_0', color='blue')
                plt.scatter(x=deriv_peaks0, y=deriv_fbg0[deriv_peaks0], color='black', zorder=5, label='Picos Derivada FBG_0')
                plt.plot(deriv_fbg1, label='Derivada FBG_1', color='green')
                plt.scatter(x=deriv_peaks1, y=deriv_fbg1[deriv_peaks1], color='black', zorder=5, label='Picos Derivada FBG_1')
                plt.plot(deriv_fbg2, label='Derivada FBG_2', color='red')
                plt.scatter(x=deriv_peaks2, y=deriv_fbg2[deriv_peaks2], color='black', zorder=5, label='Picos Derivada FBG_2')

                # Adicionar valores dos picos da derivada
                def format_peak_info_deriv(peaks, values):
                    return ', '.join([f'{values[i]:.2f}' for i in range(len(values))])

                deriv_peak_info0 = format_peak_info_deriv(deriv_peaks0, deriv_values0) if len(deriv_values0) > 0 else 'Nenhum pico significativo'
                deriv_peak_info1 = format_peak_info_deriv(deriv_peaks1, deriv_values1) if len(deriv_values1) > 0 else 'Nenhum pico significativo'
                deriv_peak_info2 = format_peak_info_deriv(deriv_peaks2, deriv_values2) if len(deriv_values2) > 0 else 'Nenhum pico significativo'

                plt.title(f'Derivada do Sinal - Passagem {index + 1}\n'
                          f'FBG_0: {deriv_peak_info0} | FBG_1: {deriv_peak_info1} | FBG_2: {deriv_peak_info2}')
                plt.xlabel('Tempo')
                plt.ylabel('Derivada dos Valores das FBGs')
                plt.legend()

                # Exibir o gráfico
                plt.tight_layout()
                plt.show()

                # Pausa para visualizar o gráfico antes de continuar
                input("Pressione Enter para continuar para o próximo gráfico...")

        print("Plotagem concluída.")

