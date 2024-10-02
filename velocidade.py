import os
import pandas as pd

# Função para processar todos os arquivos PKL em uma pasta
def process_files_in_folder_by_speed(folder_path):
    # Criar subpasta para salvar os arquivos filtrados por velocidade
    output_folder_path = os.path.join(folder_path, 'filtered_by_speed')
    os.makedirs(output_folder_path, exist_ok=True)
    print(f"Subpasta '{output_folder_path}' criada.")
    
    # Dicionário para armazenar DataFrames filtrados por velocidade
    speed_data = {speed: [] for speed in range(0, 200)}  # Exemplo de faixas de 0 km/h a 199 km/h

    # Percorrer todos os arquivos na pasta
    for filename in os.listdir(folder_path):
        if filename.endswith('.pkl'):
            file_path = os.path.join(folder_path, filename)
            print(f"Processando arquivo: {file_path}")
            data = pd.read_pickle(file_path)
            
            # Verificar se a coluna 'vel_medida' existe
            if 'vel_medida' not in data.columns:
                print(f"A coluna 'vel_medida' não existe no arquivo {file_path}. Pulando arquivo.")
                continue

            # Adicionar dados filtrados por velocidade no dicionário
            for speed in range(0, 200):
                filtered_data = data[data['vel_medida'] == speed]
                if not filtered_data.empty:
                    speed_data[speed].append(filtered_data)

    # Consolidar e salvar os dados por faixa de velocidade
    for speed, dfs in speed_data.items():
        if dfs:
            consolidated_data = pd.concat(dfs, ignore_index=True)
            vehicle_count = len(consolidated_data)
            
            output_pkl_file_path = os.path.join(output_folder_path, f'veiculos_{speed}kmh_{vehicle_count}_veiculos.pkl')
            output_csv_file_path = os.path.join(output_folder_path, f'veiculos_{speed}kmh_{vehicle_count}_veiculos.csv')
            
            # Salvar em .pkl
            consolidated_data.to_pickle(output_pkl_file_path)
            print(f"Arquivo PKL gerado para veículos na velocidade de {speed} km/h: {output_pkl_file_path}")
            
            # Salvar em .csv
            consolidated_data.to_csv(output_csv_file_path, index=False)
            print(f"Arquivo CSV gerado para veículos na velocidade de {speed} km/h: {output_csv_file_path}")

# Caminho para a pasta contendo os arquivos PKL
folder_path = r'C:\Users\Gilson\Downloads\Teste_Plot_Corte'

# Chamar a função para processar os arquivos na pasta
process_files_in_folder_by_speed(folder_path)
