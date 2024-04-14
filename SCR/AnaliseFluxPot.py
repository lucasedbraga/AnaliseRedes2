import plotly
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class Analise_FluxPot():

    def analise_tensao(self,data_vm_pu):
        
        def plot_magnitude_tensao(series, x_values=None, legend_title=None):
        
            # Definir categorias como índices da série
            categorias = series.index.tolist()
            
            # Obter os valores da série
            valores = series.values.tolist()
            
            # Definir cores com base nos valores
            cores = []
            for valor in valores:
                if valor < 0.8:
                    cores.append('#4B0082')  # Roxo escuro
                elif 0.8 <= valor < 0.95:
                    cores.append('#9370DB')  # Roxo claro
                elif 0.95 <= valor < 1.05:
                    cores.append('green')    # Verde
                elif 1.05 <= valor <= 1.2:
                    cores.append('orange')   # Laranja
                else:
                    cores.append('red')       # Outras cores (valores acima de 1.2, por exemplo)
            
            # Criar figura
            fig = go.Figure()
            
            # Adicionar barras ao gráfico
            fig.add_trace(go.Bar(
                x=list(range(1, len(categorias) + 1)),  # Contagem discreta de 1 até o tamanho do vetor de entrada
                y=valores,
                marker=dict(color=cores),  # Definir as cores das barras
                legendgroup='group'         # Agrupa as barras para personalizar a legenda
            ))
            
            # Atualizar layout
            fig.update_layout(
                title='Gráfico de Barras com Cores Variáveis',
                xaxis=dict(
                    title='Categorias' if not x_values else 'Valores',
                    tickmode='linear',      # Definir modo de marcação como linear (contagem discreta)
                    tickvals=list(range(1, len(categorias) + 1)),  # Definir os valores de marcação de 1 ao tamanho do vetor de entrada
                    ticktext=categorias    # Definir os rótulos de marcação como as categorias
                ),
                yaxis=dict(title='Valores'),
                legend_title_text=legend_title if legend_title else 'Legenda'  # Define o título da legenda
            )
            
            # Mostrar gráfico
            fig.show()

        plot_magnitude_tensao(data_vm_pu)

    
    def compara_tensao(self, data_vm_pu_calc, data_vm_pu_est):

        def plot_comparativo(series1, series2):
            # Verificar se as séries têm o mesmo índice
            if not series1.index.equals(series2.index):
                raise ValueError("Os índices das séries devem ser iguais.")
            
            # Definir categorias como índices das séries
            categorias = series1.index.tolist()
            
            # Obter os valores das séries
            valores1 = series1.values.tolist()
            valores2 = series2.values.tolist()
            
            # Calcular a diferença entre os valores das séries
            diferenca = series1 - series2
            
            # Criar figura com duas subplots (gráfico de barras e gráfico de linha)
            fig = go.Figure()
            
            # Adicionar as duas barras ao gráfico de barras
            fig.add_trace(go.Bar(
                x=categorias,
                y=valores1,
                name='Série 1'  # Nome da primeira série
            ))
            fig.add_trace(go.Bar(
                x=categorias,
                y=valores2,
                name='Série 2'  # Nome da segunda série
            ))
            
            # Criar subplot para o gráfico de linha
            fig.add_trace(go.Scatter(
                x=categorias,
                y=diferenca.values.tolist(),
                mode='lines+markers',
                name='Diferença',  # Nome da linha
                yaxis='y2'  # Utiliza o segundo eixo y para o gráfico de linha
            ))
            
            # Encontrar o máximo valor absoluto da diferença
            max_diff = abs(diferenca).max()
            
            # Atualizar layout
            fig.update_layout(
                title='Gráfico de Barras e Linha Comparativos',
                xaxis=dict(title='Categorias'),
                yaxis=dict(title='Valores'),
                yaxis2=dict(title='Diferença', overlaying='y', side='right', range=[-max_diff, max_diff]),  # Configurações do segundo eixo y
                barmode='group'  # Agrupa as barras
            )
            
            # Mostrar gráfico
            fig.show()

        plot_comparativo(series1=data_vm_pu_calc, series2=data_vm_pu_est)


        print(data_vm_pu_calc-data_vm_pu_est)