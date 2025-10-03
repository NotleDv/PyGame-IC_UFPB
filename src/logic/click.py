from utils.json_manager import write_json, read_json, write_json_restart
import os
from logic.search_elements import search_elements  
from dotenv import load_dotenv

def click (click_user:tuple, matriz):
    load_dotenv()
    path_json = os.getenv("PATH_JSON")
    
    validacao_local_click = False
    posicao_relativa_matriz = ''
    element_ = ''
    
    for index, i in enumerate(matriz):    
        for index_j, j in enumerate(i):   
            elemento = matriz[index][index_j]['rect'] # Pego os rect de cada elemento da matriz
            
            if elemento.collidepoint(click_user): # Verifico point de click foi em algum rect da matriz
                element_ = elemento
                validacao_local_click = True
                posicao_relativa_matriz = matriz[index][index_j]['posicao_relativa']
                break

    if validacao_local_click:
        qtd_bau, status = search_elements(posicao_relativa=posicao_relativa_matriz, matriz=matriz)
        
        result = {"qtd_bau": qtd_bau,
                  "status": status,
                  "click_valido": True }
        write_json(path_json, 'return_click', result)
        
        return element_     
   
    else:
        return None       

def jogadas(click_valido, max_jogadas, sounds, element, history_rects, status):
        load_dotenv()
        path_json = os.getenv("PATH_JSON")
        
        jogada = read_json(path_json)['jogada']
        history_points = read_json(path_json)['history_points']
        
        # Verificando se já acabou o jogo
        total_jogadas = read_json(path_json)['total_jogos']
        if total_jogadas >= max_jogadas:
            pontucao_total_play_01 = history_points['play_01']
            pontucao_total_play_02 = history_points['play_02']
            print(f'>>>> Fim de jogo!! Play_01: {pontucao_total_play_01} | Play_02: {pontucao_total_play_02}')  
            return total_jogadas
        
        # Caso o tempo tenha acabo e houve click
        status_bar = read_json(path_json)['status_bar']
        if status_bar['termino']:
             print("Tempo acabou")
             return total_jogadas

        ## Verificando o click
        player_atual = jogada['player_atual']
        player_anterior = jogada['player_anterior']

        ## Verificando se o rect clicado já foi clicado antes
        element_valido = False
        if element and not element in history_rects: 
            element_valido = True
        
        ## Verifica a pontuação e dispara o efeito sonoro
        potucao = 0
        if status == 1:
            potucao = 100
            sounds['bau'].play()
            
        if status == -1:
            potucao = -50
            sounds['buraco'].play()
            
        if status == 0:
            sounds['encontrou_nada'].play()
            
        ## Verifica se o rect clicado é valido, e se ele não foi cliado antes
        validacao_jogada = False
        if click_valido and element_valido:
            validacao_jogada = True
            # Atualiza pontuação
            history_points[player_atual] = max(0, history_points[player_atual] + potucao)
            write_json(path_json, 'history_points', history_points)
            
            # Troca de jogador
            jogada['player_atual'] = player_anterior
            jogada['player_anterior'] = player_atual
            write_json(path_json, 'jogada', jogada)
            
            total_jogadas += 1
            write_json(path_json, 'total_jogos', total_jogadas)
            
            history_rects.append(element)
            
            print(f'|| JOGADA VÁLIDA || Trocando para: {jogada["player_atual"]}')
            print("Histórico de pontos:", history_points)
            
            
        return validacao_jogada, history_rects
     