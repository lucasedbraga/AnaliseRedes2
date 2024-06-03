import plotly
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandapower.networks as pn

class GeradorCenario:
   
    def __init__(self,net) -> None:
        self.net = net
        self.DLOAD()
        
        
    def DMED(self):
        pass
    
    def DLOAD(self):
        def gerar_valores_distribuicao_normal(valores_referencia, desvio_padrao_percentual=13.33):
            # Calcula o desvio padrão com base no percentual
            desvios_padrao = valores_referencia * (desvio_padrao_percentual / 100)
            # Gera valores aleatórios dentro da distribuição normal para cada valor de referência
            valores_sorteados = np.random.normal(loc=valores_referencia, scale=desvios_padrao)
            
            return valores_sorteados

        # Exemplo de uso
        valores_referencia = self.net.load       
        self.net.load['p_mw'] = gerar_valores_distribuicao_normal(valores_referencia['p_mw'])
        self.net.load['q_mvar'] = gerar_valores_distribuicao_normal(valores_referencia['q_mvar'])
        

        
if __name__ == '__main__':
    import sys
    sys.path.append('./SYS/')  
    sistema = pn.case_ieee30
    net = sistema()
    print(net.load)
    cenario = GeradorCenario(net=net)
    print(cenario.net.load)

    