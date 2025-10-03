import json

def read_json(path:str):
    result = ''
    with open (path, 'r', encoding='utf-8') as file:
        result = json.load(file)
    
    return result

def write_json (path:str, chave, atualizacao):
    try:
        json_atual = read_json(path)
        json_atual[chave] = atualizacao

        with open (path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(json_atual, indent=2))
    except Exception as error:
        print('🚩 Erro em salvar json', error)
        
def write_json_restart (path:str, path_restart):
    try:
        dados = read_json(path_restart)
        with open (path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(dados, indent=2))
    except Exception as error:
        print('🚩 Erro em salvar json', error)