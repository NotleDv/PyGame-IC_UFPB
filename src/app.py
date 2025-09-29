import pygame, time
import sys, threading
# x, y
# largura. altura
stop_event = threading.Event()
timer_thread = None ## MUDANÇA: Variável para manter uma referência à thread do timer atual

def main():
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
                             height = h_game,
                             dimensao = 4,
                             size_elements = 1.5)
    
    ## 
    from utils.background import background_surface_game, background_display, back_player_atual, back_points
    background_surface_game(screen=surface_game,
                            matriz=matriz_k)

    background_display(display)
    
    ##
    from utils.pallet_color import main as pallet_color_
    pallet_color = pallet_color_()
    
    ##
    from utils.fonts import main as fonts             
      
    ##
    from logic.blit_elements import main as blit_elements   
    
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
    
    def color_barra (status_bar):
        palet_color_barra = {'inicio': '#55B3F2', 'meio': '#EDF54B', 'final': '#F22929'}
        cor = ''
        
        if status_bar['progresso'] >= 300: 
            cor = palet_color_barra['inicio']
        elif status_bar['progresso'] < 300 and status_bar['progresso'] >= 100:
            cor = palet_color_barra['meio']
        else:
            cor = palet_color_barra['final']
            
        return cor
    
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
        pygame.draw.rect(surface_head, color, (170, 20, largura, 25))
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
            
    ## MUDANÇA: Função centralizada para resetar o timer.
    def reset_timer():
        #global timer_thread
        
        if timer_thread and timer_thread.is_alive():
            stop_event.set() # Sinaliza para a thread antiga parar
            timer_thread.join(timeout=0.1) # Espera um pouco por ela
            
        stop_event.clear() # Limpa o evento para a nova thread
        status_bar['termino'] = False
        
        # Cria e inicia a nova thread
        timer_thread = threading.Thread(target=time_play)
        timer_thread.start()

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
        
        qtd_bau, status, element, validacao = click(click_user=click_point, matriz=matriz_k,search_elements=search_elements)
        
        validacao_2 = False
        if element and not element in history_rects: 
            validacao_2 = True
        
        potucao = 0
        if status == 1:
            potucao = 100
        elif status == -1:
            potucao = -50
            
        if validacao and validacao_2:
            blit_elements(status=status, 
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

            # MUDANÇA: Blita o nome do novo jogador e reseta o timer de forma centralizada
            blit_play_atual()
            reset_timer()
            atualizacao_points(surface_point, history_points)
        return total_jogadas

    def blit_play_atual ():
        rect_play_atual = pygame.Rect((20, 10, 135, 50))
        
        font = fonts(30)
        player_atual = jogada['player_atual']
        print(player_atual)
        texto = font.render(str(name_player[player_atual]), True, pallet_color['cinza'])
        texto_rect = texto.get_rect(center=rect_play_atual.center)
        back_player_atual(surface_head)
        surface_head.blit(texto, texto_rect)
    #############################################
    
    
    def atualizacao_points(surface, history_points):
        rect_point = pygame.Rect((0, 0, 700, 100))
        back_points(surface_point, rect_point)
        
        def create_text(size_font, info_text, rect_center, surface, color, type_font='default'):
            font = fonts(size_font, type_font)
            texto = font.render(str(info_text), True, color)
            texto_rect = texto.get_rect(center=rect_center.center)
            #back_player_atual(surface)
            surface.blit(texto, texto_rect)
        #p
        rect_play_01 = pygame.Rect((0,0,140,40))
        rect_play_01.left = 95
        rect_play_01.top = 47    
        create_text(size_font= 30,
                    info_text=name_player['play_01'],
                    rect_center=rect_play_01,
                    surface=surface,
                    color= pallet_color['branco'],
                    type_font='point_normal') 
            
        rect_play_02 = pygame.Rect((0,0,140,40))
        rect_play_02.left = 483
        rect_play_02.top = 47 
        create_text(size_font= 30,
                    info_text=name_player['play_02'],
                    rect_center=rect_play_02,
                    surface=surface,
                    color=pallet_color['branco'],
                    type_font='point_normal')
        #pp
        rect_point_p1 = pygame.Rect((0,0,93,40))
        rect_point_p1.left = 247
        rect_point_p1.top = 47    
        create_text(size_font= 40,
                    info_text=history_points['play_01'],
                    rect_center=rect_point_p1,
                    surface=surface,
                    color=pallet_color['alaranjado'],
                    type_font='point_negrito')
        
        rect_point_p2 = pygame.Rect((0,0,93,40))
        rect_point_p2.left = 378
        rect_point_p2.top = 47 
        create_text(size_font= 40,
                    info_text=history_points['play_02'],
                    rect_center=rect_point_p2,
                    surface=surface,
                    color=pallet_color['alaranjado'],
                    type_font='point_negrito')
        
    
    #############################################
    # Inicia o jogo
    blit_play_atual()
    reset_timer() # MUDANÇA: Inicia o primeiro timer aqui

    atualizacao_points(surface_point, history_points)
    
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
        
    
        ## MUDANÇA: Lógica de tempo esgotado simplificada e movida para o loop principal
        if status_bar['termino'] and run:
            player_atual = jogada['player_atual']
            player_anterior = jogada['player_anterior']
            
            # Evita que a troca ocorra múltiplas vezes enquanto `termino` for True
            if not timer_thread or not timer_thread.is_alive():
                jogada['player_atual'] = player_anterior
                jogada['player_anterior'] = player_atual
                
                print(f'|| TEMPO ESGOTADO - TROCA DE TURNO || Trocando para: {jogada["player_atual"]}')
                
                blit_play_atual()
                reset_timer()

        # rect_point = pygame.Rect((0, 0, 700, 100))
        # pygame.draw.rect(surface_point, (255,255,2), rect_point)
        
        blit_bar_progress()
        
        # pygame.draw.rect( surface_point, (124,24,125), rect_a)
        # pygame.draw.rect( surface_point, (124,24,125), rect_play_02)
        # pygame.draw.rect( surface_point, (124,155,125), rect_c)
        # pygame.draw.rect( surface_point, (124,155,125), rect_d)
        pygame.display.update()
        #clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()