import pandapower as pp

class FluxoDePotencia:

    def __init__(self, data_DBAR, data_DLIN, data_DGER, data_DLOAD, data_DSIM) -> None:

        from DATA_Simulacao import Log_Simulação
        from RedeEletrica import ModeloRedeEletrica
        from AnaliseFluxPot import Analise_FluxPot  
        # Começa a contagem de tempo
        self.LOG_SIMULACAO = Log_Simulação()
        #############################

        self.RedeEletrica_simulada = ModeloRedeEletrica()
        self.DBAR = self.RedeEletrica_simulada.DBAR(data_DBAR)
        self.DLIN = self.RedeEletrica_simulada.DLIN(data_DLIN) 
        self.DGER = self.RedeEletrica_simulada.DGER(data_DGER)
        self.DLOAD = self.RedeEletrica_simulada.DLOAD(data_DLOAD)
        self.LOG_SIMULACAO.Identificacao_Simulacao(data_DSIM)

        self.LOG_SIMULACAO.msg_log("Leitura do Modelo Realizada")

        self.executar()
        self.Analise = Analise_FluxPot()

        ##############################
        # Termina a contagem de tempo
        self.LOG_SIMULACAO.log_fim_simulacao()

    def executar(self):
        pp.runpp(self.RedeEletrica_simulada.net)
        self.LOG_SIMULACAO.msg_log("Fluxo de Potência Executado")
    
    def avaliacao_tensao (self):

        dados_tensao = self.RedeEletrica_simulada.net.res_bus

        self.Analise.analise_tensao(data_vm_pu=dados_tensao.vm_pu)
        
  


if __name__ == '__main__':
    
    data_DBAR = "DBAR"
    data_DLIN = "DLIN"
    data_DGER = "DGER"
    data_DLOAD = "DLOAD"
    data_DSIM = "DSIM"

    flux_pot = FluxoDePotencia(data_DBAR, data_DLIN, data_DGER, data_DLOAD, data_DSIM)
    print(flux_pot.RedeEletrica_simulada.net.res_bus)
    