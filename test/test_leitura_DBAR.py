# test_leitura_DBAR.py
def test_exemplo_DBAR():
    # String de teste
    vn_kv=1.
    min_vm_pu=0.95
    max_vm_pu=1.05

    try:
        net = pp.create_empty_network()
    except:
        net = None
    

    # Verificar se a contagem de caracteres está correta
    assert net != None

