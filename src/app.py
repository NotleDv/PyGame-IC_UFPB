import pygame, time
import sys, threading
# x, y
# largura. altura
def main():
    stop_event = threading.Event()
    timer_thread = {'timer_thread':None}
    
    run = True
    
    offset_x_game, offset_y_game = 100, 70
    
    name_01 = 'Elton_A1'
    name_02 = 'Etlon_A2'
    
    pygame.init()
    pygame.font.init()
    
    w_display, h_display = 700, 700
    
    ##
    from configs.screen import main as screens
    config_screen = screens(w_display=w_display, h_display=h_display)
    
    w_game, h_game, h_head= config_screen[1]
    display, surface_game, surface_point, surface_head = config_screen[0]
    
    ## 
    from logic.matriz import main as create_matriz
    matriz_k = create_matriz(width = w_game,
                             height = h_game)
    
    ## 
    from utils.background import background_surface_game, background_display, back_player_atual, back_points
    background_surface_game(screen=surface_game,
                            matriz=matriz_k)

    background_display(display)
    
    ##
    from utils.pallet_color import pallet_color, color_barra
    pallet_color_ = pallet_color()
    
    ##
    from utils.fonts import main as fonts             
      
    ##
    from logic.blit_elements import blit_element, blit_play_atual, atualizacao_points
    
    
    ##
    from logic.click import click
      
    ##
    from logic.search_elements import search_elements  
    
    ##
    from utils.background import back_progresso, front_progresso
    rect_prog = pygame.Rect((170, 10, 530, 40))
    
    for i in matriz_k:
        print('| ', end='')
        for j in i:
            print(j['valor'], end=' ')
        print(' |')
        
    ###############
    max_jogadas = 16
    history_points = {'play_01': 0, 'play_02':0} # Pontuação do jogador
    name_player = {'play_01': name_01, 'play_02':name_02} # Nome dos jogadores
    history_rects = [] # Quais rects já foram clicados
    
    jogada = {'jogada_atual':0 , 'player_atual': 'play_01','jogada_anterior':0 , 'player_anterior': 'play_02'}
    total_jogadas = 0
    ###############
    
    
    ## Blit da estrutura da barra de regressão do tempo
    status_bar = {'progresso': 530, 'termino': True} 
    def blit_bar_progress ():
        back_progresso(surface_head, rect_prog)
        largura = int(status_bar['progresso']) 
          
        color = color_barra(status_bar)
        
        pygame.draw.rect(surface_head, color, (170, 18, largura, 28))
        front_progresso(surface_head, rect_prog)
    
    ## Medindo o tempo do jogador
    def time_play():
        
        print('||| Jogos feitos: ',total_jogadas)
        
        ## Verificando se já foram a quantidade max de partidas
        if total_jogadas < 16:
            ## Dando inicio ao novo tempo
            ### Inicia com False - Já que está começando do zero.
            status_bar['termino'] = False 
            
            for i in range(530, -1, -1):
                if stop_event.is_set():  # Verifica se foi pedido para parar
                    print("::: TIMER RESETADO POR JOGADA :::")
                    return # Encerra a função na thread
                status_bar["progresso"] = i
                time.sleep(0.02)
            
            print("::: TEMPO ESGOTADO :::")
            status_bar["termino"] = True # Sinaliza que o tempo acabou
            
    ## Reset da Thread
    def reset_timer(timer_thread):
        timer_thread_ = timer_thread['timer_thread']
        if timer_thread_ and timer_thread_.is_alive(): # Se tem uma thread ou ela está ativa então...
            stop_event.set() # Sinaliza para a thread parar
            timer_thread_.join(0.1) # Atrasa a próxima execução até a thread parar
            
        stop_event.clear() # Limpa o evento para a nova thread
        status_bar['termino'] = False
        
        # Cria e inicia a nova thread
        timer_thread_ = threading.Thread(target=time_play)
        timer_thread['timer_thread'] = timer_thread_
        timer_thread_.start()

    def jogadas(click_point, total_jogadas, max_jogadas, history_points, jogada):
        if total_jogadas >= max_jogadas:
            pontucao_total_play_01 = history_points['play_01']
            pontucao_total_play_02 = history_points['play_02']
            print(f'>>>> Fim de jogo!! Play_01: {pontucao_total_play_01} | Play_02: {pontucao_total_play_02}')  
            return total_jogadas
        
        # Se o tempo já acabou, o clique é inválido para esta jogada
        if status_bar['termino']:
             print("Clique ignorado, tempo já esgotado.")
             return total_jogadas

        player_atual = jogada['player_atual']
        player_anterior = jogada['player_anterior']
        
        qtd_bau, status, element, click_valido = click(click_user=click_point, matriz=matriz_k,search_elements=search_elements)
        
        element_valido = False
        if element and not element in history_rects: 
            element_valido = True
        
        potucao = 0
        if status == 1:
            potucao = 100
        elif status == -1:
            potucao = -50
            
        if click_valido and element_valido:
            blit_element(status=status, 
                          qtd_baus=qtd_bau,
                          rect_element=element,
                          screen=surface_game)
            
            # Atualiza pontuação
            history_points[player_atual] = max(0, history_points[player_atual] + potucao)
            
            # Troca de jogador
            jogada['player_atual'] = player_anterior
            jogada['player_anterior'] = player_atual
            total_jogadas += 1
            
            history_rects.append(element)
            
            print(f'|| JOGADA VÁLIDA || Trocando para: {jogada["player_atual"]}')
            print("Histórico de pontos:", history_points)

            blit_play_atual(jogada = jogada,
                    name_player = name_player,
                    pallet_color = pallet_color_,
                    back_player_atual = back_player_atual,
                    surface_head = surface_head)
            reset_timer(timer_thread)
            atualizacao_points(surface = surface_point, history_points = history_points, name_player = name_player, back_points = back_points, pallet_color = pallet_color_)
        return total_jogadas
          
    
    #############################################
    # Inicia o jogo
    blit_play_atual(jogada = jogada,
                    name_player = name_player,
                    pallet_color = pallet_color_,
                    back_player_atual = back_player_atual,
                    surface_head = surface_head)
    reset_timer(timer_thread)

    atualizacao_points(surface = surface_point, 
                       history_points = history_points, 
                       name_player = name_player, 
                       back_points = back_points, 
                       pallet_color = pallet_color_)
    
    
    while run:
        display.blit( surface_game, (offset_x_game, offset_y_game))
        display.blit( surface_head, (0, 0) ) 
        display.blit( surface_point , (0, 600))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                stop_event.set() # Sinaliza para a thread parar ao sair
                          
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                posicao_click = ( (mouse_x-offset_x_game), (mouse_y-offset_y_game))
                total_jogadas= jogadas(posicao_click, total_jogadas, max_jogadas, history_points, jogada)
        
    
        ## 
        if status_bar['termino'] and run:
            player_atual = jogada['player_atual']
            player_anterior = jogada['player_anterior']
            
            ## Inicialização da uma nova thread
            if timer_thread['timer_thread'] or timer_thread['timer_thread'].is_alive():
                jogada['player_atual'] = player_anterior
                jogada['player_anterior'] = player_atual
                
                print(f'TROCA DE TURNO: {jogada["player_atual"]}')
                
                blit_play_atual(jogada = jogada,
                    name_player = name_player,
                    pallet_color = pallet_color_,
                    back_player_atual = back_player_atual,
                    surface_head = surface_head)
                reset_timer(timer_thread)

        blit_bar_progress()
        
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()