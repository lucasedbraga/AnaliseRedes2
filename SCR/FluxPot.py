import pandapower as pp

class FluxoDePotencia:

    def __init__(self, RedeEletrica_simulada, data_DSIM) -> None:

        from DATA_Simulacao import Log_Simulação
        from AnaliseFluxPot import Analise_FluxPot  
        # Começa a contagem de tempo

        data_DSIM["Modelo Executado"] = "Fluxo de Potência"
        self.LOG_SIMULACAO = Log_Simulação(data_DSIM=data_DSIM)
        #############################

        self.RedeEletrica_simulada = RedeEletrica_simulada
        self.LOG_SIMULACAO.msg_log(f"Sistema Elétrico Carregado:{None} ")

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
        
    def avaliacao_fluxo_linhas (self):
        self.Analise.analise_fluxo_linhas(self.RedeEletrica_simulada.net)
        
if __name__ == '__main__':
    import sys
    sys.path.append('./SYS/')  
    from sistema_teste_4Barras import SistemaTeste_4Barras

    RedeEletrica_simulada = SistemaTeste_4Barras()

    data_SIM = {
        "Descrição": "Teste do Fluxo de Potência - Sistema 4 Barras",
        "Versão": "0.1"
    }

    flux_pot = FluxoDePotencia(RedeEletrica_simulada=RedeEletrica_simulada,
                               data_DSIM=data_SIM)
    
    print(flux_pot.RedeEletrica_simulada.net.res_bus)
    