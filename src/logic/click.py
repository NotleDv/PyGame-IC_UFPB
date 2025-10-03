from utils.json_manager import write_json, read_json, write_json_restart
import os

def click (click_user:tuple, matriz, search_elements):
    
    condicion = False
    posicao = ''
    element_ = ''
    validacao = False
    
    for index, i in enumerate(matriz):    
        for index_j, j in enumerate(i):   
            elemento = matriz[index][index_j]['rect'] 
            
            if elemento.collidepoint(click_user):
                element_ = elemento
                condicion = True
                posicao = matriz[index][index_j]['posicao_relativa']
                break

    if condicion:
        qtd_bau, status = search_elements(posicao_relativa=posicao, matriz=matriz)
        
        validacao = True
        
        return qtd_bau, status, element_, validacao     
   
    else:
        return [None]*4       

def jogadas(click_valido, total_jogadas, max_jogadas, history_points, sounds, element, history_rects, status):
        path_json = os.path.join( os.getcwd(), 'configs', 'parametros.json' )
        jogada = read_json(path_json)['jogada']
        
        # Verificando se já acabou o jogo
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
            
            # Troca de jogador
            jogada['player_atual'] = player_anterior
            jogada['player_anterior'] = player_atual
            write_json(path_json, 'jogada', jogada)
            
            total_jogadas += 1
            
            history_rects.append(element)
            
            print(f'|| JOGADA VÁLIDA || Trocando para: {jogada["player_atual"]}')
            print("Histórico de pontos:", history_points)
            
            
        return total_jogadas, validacao_jogada
     