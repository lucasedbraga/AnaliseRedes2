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
                x=list(range(1, len(categorias) + 1)),
                y=valores1,
                name='Série 1'  # Nome da primeira série
            ))
            fig.add_trace(go.Bar(
                x=list(range(1, len(categorias) + 1)),
                y=valores2,
                name='Série 2'  # Nome da segunda série
            ))
            
            # Criar subplot para o gráfico de linha
            fig.add_trace(go.Scatter(
                x=list(range(1, len(categorias) + 1)),
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
                xaxis=dict(title='Categorias', tickmode='array', tickvals=list(range(1, len(categorias) + 1)), ticktext=categorias),
                yaxis=dict(title='Valores'),
                yaxis2=dict(title='Diferença', overlaying='y', side='right', range=[-max_diff, max_diff]),  # Configurações do segundo eixo y
                barmode='group'  # Agrupa as barras
            )
            
            # Mostrar gráfico
            fig.show()

        plot_comparativo(series1=data_vm_pu_calc, series2=data_vm_pu_est)
        print(data_vm_pu_calc-data_vm_pu_est)

    
    def analise_fluxo_linhas(self, Rede_Analisada):

        def plot_sankey_linhas(dataframe):

            df_conectividade = dataframe.line
            df_flux_lin = dataframe.res_line
            df_conectividade['FLUXO_LINHA'] = df_flux_lin.p_from_mw - df_flux_lin.p_to_mw
            df_conectividade['from_bus'] = df_conectividade['from_bus'] + 1
            df_conectividade['to_bus'] = df_conectividade['to_bus'] + 1 

            df_conectividade['NIVEL_PERCENTUAL'] = (df_flux_lin.loading_percent)

            # Excluir ligações de um nó para si mesmo
            df_conectividade = df_conectividade[df_conectividade['from_bus'] !=  df_conectividade['to_bus']]

            # Criar lista de nós únicos
            nodes = list(set(df_conectividade['from_bus'].tolist() +  df_conectividade['to_bus'].tolist()))

            # Definir as cores com base no nível percentual
            colors = ['green' if percent < 70 else 'yellow' if percent < 90 else 'red' for percent in df_conectividade['NIVEL_PERCENTUAL']]

            fig = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=nodes,
                    color="blue"  # Cor dos nós
                ),
                link=dict(
                    source=df_conectividade['from_bus'].map(lambda x: nodes.index(x)),
                    target= df_conectividade['to_bus'].map(lambda x: nodes.index(x)),
                    value= df_conectividade['FLUXO_LINHA'],
                    color=colors  # Cor dos links com base no nível percentual
                )
            )])

            fig.update_layout(title_text="Diagrama Sankey", font_size=10)
            fig.show()

        plot_sankey_linhas(Rede_Analisada)