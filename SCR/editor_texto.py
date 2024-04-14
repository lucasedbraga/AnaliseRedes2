# Editoração


def margem():
    print('-'*50)
#class Texto():


def error(texto):
    print(f'\033[1;30;41m [...] ERRO !! : {texto} !!! \033[m', end='\n')


def aviso(texto):
    print(f'\033[1;33m [...] ATENÇÃO : {texto} ! \033[m', end='\n')


def list(texto):
    print(f'\033[1;36; m{texto} \033[m', end='\n')


def endereco(texto):
    print(f'\033[0;33; m{texto} \033[m', end='\n \n')


def resposta(texto):
   print(f'\033[92m [...] {texto} \033[0m', end='\n')

def sucesso(texto):
   print(f'\033[1;30;42m  [...] >>> {texto} <<< \033[m', end='\n')

def titulo(texto):
    print(f'\033[1;33;44m {texto} \033[m', end='\n')


if __name__ == '__main__':

    error("error")
    sucesso("sucesso")
    aviso("aviso")
    list("lista")
    endereco("endereco")
    resposta("resposta")
    titulo("titulo")