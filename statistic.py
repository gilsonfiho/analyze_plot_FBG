import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def generate_dashboard_pdf(folder_path):
    # Criar subpasta para salvar o PDF do dashboard
    pdf_folder_path = os.path.join(folder_path, 'dashboard')
    os.makedirs(pdf_folder_path, exist_ok=True)
    pdf_file_path = os.path.join(pdf_folder_path, 'dashboard_summary.pdf')
    
    # Dicionário para armazenar todos os dados consolidados
    all_data = pd.DataFrame()

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

            # Consolidar os dados
            all_data = pd.concat([all_data, data], ignore_index=True)
    
    if all_data.empty:
        print("Nenhum dado disponível para gerar o PDF.")
        return

    # Filtrar dados para velocidades <= 100 km/h
    filtered_data = all_data[all_data['vel_medida'] <= 100]

    # Preparar o PDF
    with PdfPages(pdf_file_path) as pdf:
        # Página de Resumo
        plt.figure(figsize=(10, 6))
        plt.suptitle('Dashboard Velocidade', fontsize=16)
        
        # Estatísticas principais
        mean_speed = filtered_data['vel_medida'].mean()
        std_speed = filtered_data['vel_medida'].std()
        min_speed = filtered_data['vel_medida'].min()
        max_speed = filtered_data['vel_medida'].max()
        vehicle_count = len(filtered_data)
        
        plt.text(0.1, 0.9, f'Média da Velocidade: {mean_speed:.2f} km/h', fontsize=12)
        plt.text(0.1, 0.8, f'Desvio Padrão da Velocidade: {std_speed:.2f} km/h', fontsize=12)
        plt.text(0.1, 0.7, f'Velocidade Mínima: {min_speed:.2f} km/h', fontsize=12)
        plt.text(0.1, 0.6, f'Velocidade Máxima: {max_speed:.2f} km/h', fontsize=12)
        plt.text(0.1, 0.5, f'Número Total de Veículos: {vehicle_count}', fontsize=12)
        plt.axis('off')
        pdf.savefig()
        plt.close()
        
        # Histograma Geral
        plt.figure(figsize=(10, 6))
        plt.hist(filtered_data['vel_medida'], bins=20, edgecolor='black')
        plt.title('Distribuição das Velocidades dos Veículos')
        plt.xlabel('Velocidade (km/h)')
        plt.ylabel('Número de Veículos')
        pdf.savefig()
        plt.close()
        
    print(f"Arquivo PDF gerado: {pdf_file_path}")

# Caminho para a pasta contendo os arquivos PKL
folder_path = r'C:\Users\Gilson\Downloads\Teste_Plot_Corte'

# Chamar a função para gerar o dashboard PDF
generate_dashboard_pdf(folder_path)
