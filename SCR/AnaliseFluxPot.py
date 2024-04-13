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