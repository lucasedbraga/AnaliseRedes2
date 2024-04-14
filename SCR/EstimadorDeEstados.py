import pandapower as pp
import pandapower.estimation as se
from FluxPot import FluxoDePotencia
from DATA_Simulacao import Log_Simulação
from AnaliseFluxPot import Analise_FluxPot

class EstimacaoDeEstados:

    def __init__(self, RedeEletrica_simulada, data_SIM) -> None:

        # Começa a contagem de tempo
        self.LOG_SIMULACAO = Log_Simulação()
        #############################          
        self.RedeEletrica_simulada = RedeEletrica_simulada
        self.flux_pot_resolvido = FluxoDePotencia(RedeEletrica_simulada=self.RedeEletrica_simulada,
                                                  data_DSIM=data_SIM)
        
        self.Analise = Analise_FluxPot()
        self.RedeEletrica_simulada.DMED()
        self.executar()      
       

    def executar(self):
        se.estimate(self.RedeEletrica_simulada.net)
        self.LOG_SIMULACAO.msg_log("Fluxo de Potência Executado")
    
    def compara_tensao (self):

        dados_tensao_calculados = self.RedeEletrica_simulada.net.res_bus
        dados_tensao_estimados = self.RedeEletrica_simulada.net.res_bus_est
        self.Analise.compara_tensao(data_vm_pu_calc=dados_tensao_calculados.vm_pu, data_vm_pu_est= dados_tensao_estimados.vm_pu)


if __name__ == '__main__':
    import sys
    sys.path.append('./SYS/')  
    from sistema_teste_4Barras import SistemaTeste_4Barras

    RedeEletrica_simulada = SistemaTeste_4Barras()

    data_SIM = {
        "Descrição": "Teste da Estimação de Estados - Sistema 4 Barras",
        "Versão": "0.1"
    }

  
    Estimador = EstimacaoDeEstados(RedeEletrica_simulada=RedeEletrica_simulada, data_SIM=data_SIM)
    Estimador.compara_tensao()