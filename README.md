
---

## 🚀 Objetivo do Projeto

Permitir a análise dos sinais obtidos via sensores FBG, especialmente para:
- 📈 Visualização dos dados em tempo real ou pós-processamento
- 🧠 Regressão e suavização dos sinais
- 🚗 Identificação de eventos (como passagem de veículos)
- 🕒 Cálculo da velocidade com base no tempo entre sensores
- 📊 Geração de estatísticas dos experimentos

---

## ⚙️ Principais Scripts

### 🔹 Regressão e Pré-processamento

- `regress.py`, `regress2.py`, `regress3.py`  
  > Contém funções para interpolação, suavização e regressão de sinais, com base em bibliotecas como `scipy` e `numpy`. Utilizado para melhorar a qualidade dos dados antes da análise.

---

### 🔹 Visualização

- `plotVelocidade.py`, `plotVelocidade2.py`, `plotVelocidade3.py`, `plotVelocidade4.py`  
  > Scripts de plotagem da velocidade estimada entre pares de sensores. Cada versão pode conter diferentes métodos de detecção ou thresholds.

- `plotPlaca.py`, `plotPlaca2.py`, `plotPlaca3.py`  
  > Focados na visualização do comportamento de strain em veiculos que passaram mais de uma vez.

- `plot.py`, `plot2.py`  
  > Versões genéricas de visualização dos sinais brutos ou processados.

---

### 🔹 Cálculo e Estatística

- `statistic.py`  
  > Gera histogramas, médias, desvios padrão e análises de pico para eventos detectados.

- `velocidade.py`  
  > Calcula a velocidade entre sensores a partir do tempo de detecção em múltiplas placas.

---

### 🔹 Scripts de Análise por Placa

- `placa.py`, `placa1.py`, `placa3.py`  
  > Scripts dedicados a analisar e comparar dados em placas individuais, utilizados em testes de campo.

---

## 💻 Como Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/analyze_plot_FBG.git
   cd analyze_plot_FBG