import os
import pandas as pd

# Função para processar todos os arquivos PKL em uma pasta
def process_files_in_folder(folder_path):
    # Dicionário para armazenar as contagens de passagens por placa de veículo
    vehicle_counts = {}
    
    # Lista para armazenar os dataframes filtrados
    filtered_dfs = []

    # Criar subpasta para salvar os arquivos filtrados
    output_folder_path = os.path.join(folder_path, 'filtered_by_placa')
    os.makedirs(output_folder_path, exist_ok=True)
    print(f"Subpasta '{output_folder_path}' criada.")

    # Percorrer todos os arquivos na pasta
    for filename in os.listdir(folder_path):
        if filename.endswith('.pkl'):
            file_path = os.path.join(folder_path, filename)
            print(f"Processando arquivo: {file_path}")
            data = pd.read_pickle(file_path)
            
            # Verificar se a coluna 'placa_veiculo' existe
            if 'placa_veiculo' not in data.columns:
                print(f"A coluna 'placa_veiculo' não existe no arquivo {file_path}. Pulando arquivo.")
                continue

            # Contar as passagens por placa de veículo
            vehicle_counts_in_file = data['placa_veiculo'].value_counts()
            print(f"Contagem de passagens no arquivo {filename}:")
            print(vehicle_counts_in_file)
            
            # Atualizar o dicionário de contagens gerais
            for placa, count in vehicle_counts_in_file.items():
                if placa not in vehicle_counts:
                    vehicle_counts[placa] = 0
                vehicle_counts[placa] += count
                
            # Filtrar veículos que passaram pelo menos duas vezes
            filtered_data = data[data['placa_veiculo'].isin(vehicle_counts_in_file[vehicle_counts_in_file >= 2].index)]
            filtered_dfs.append(filtered_data)
    
    # Gerar arquivos PKL e CSV para veículos que passaram pelo menos duas vezes
    for placa, count in vehicle_counts.items():
        if count >= 2:
            vehicle_data = pd.concat([df[df['placa_veiculo'] == placa] for df in filtered_dfs])
            
            if not vehicle_data.empty:
                output_pkl_file_path = os.path.join(output_folder_path, f'{placa}_{count}_passagens.pkl')
                output_csv_file_path = os.path.join(output_folder_path, f'{placa}_{count}_passagens.csv')
                
                # Salvar em .pkl
                vehicle_data.to_pickle(output_pkl_file_path)
                print(f"Arquivo PKL gerado para o veículo {placa}: {output_pkl_file_path}")
                
                # Salvar em .csv
                vehicle_data.to_csv(output_csv_file_path, index=False)
                print(f"Arquivo CSV gerado para o veículo {placa}: {output_csv_file_path}")
    
    # Imprimir veículos que passaram mais de duas vezes
    for placa, count in vehicle_counts.items():
        if count >= 2:
            print(f'Veículo {placa} passou {count} vezes.')

# Caminho para a pasta contendo os arquivos PKL
folder_path = r'C:\Users\Gilson\Downloads\Teste_Plot_Corte'

# Chamar a função para processar os arquivos na pasta
process_files_in_folder(folder_path)
