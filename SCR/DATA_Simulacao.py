import time
import editor_texto


class Log_Simulação():

    def __init__(self) -> None:
            self.inicio_simulacao = time.time()
            editor_texto.resposta(self.msg_log("Inicializando Modelo"))

    def msg_log(self, mensagem:str):
        return mensagem

    def log_fim_simulacao(self):
        
        self.fim_simulacao = time.time()
        # Calcula o tempo decorrido
        self.tempo_de_rodada = self.fim_simulacao - self.inicio_simulacao
        editor_texto.aviso(f"tempo_de_rodada: = {self.tempo_de_rodada:.3f} seg")
        editor_texto.error(self.msg_log("Fim da Rodada"))
    
    def Identificacao_Simulacao(self, data_SIM):
          editor_texto.resposta(self.msg_log("Dados de Simulação Salvos"))

    

