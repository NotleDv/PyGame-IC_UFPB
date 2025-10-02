import pygame, time
import sys
# x, y
# largura. altura
def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    
    ## 'Globais'
    name_01 = 'Elton_A1'
    name_02 = 'Etlon_A2'
    clock = pygame.time.Clock()
    run = True
    blit_elements_click = {'status': 0, 'validacao': False, 'qtd_bau': None, 'rect_element': None, 'screen': None, 'animation': None}
    
    encontrou_nada_sound = pygame.mixer.Sound('../assets/Sounds/encontrou_nada.wav')
    bau_sound = pygame.mixer.Sound('../assets/Sounds/bau.wav')
    buraco_sound = pygame.mixer.Sound('../assets/Sounds/buraco.wav')
    bau_sound.set_volume(0.5)
    buraco_sound.set_volume(0.1)
    encontrou_nada_sound.set_volume(0.1)
    
    sounds = {'encontrou_nada': encontrou_nada_sound,
              'bau': bau_sound,
              'buraco': buraco_sound}
    
    ## Cache animation
    from utils.animation import load_animation_bau, load_animation_buraco
    cache_animation_bau = load_animation_bau()
    cache_animation_buraco = load_animation_buraco()
    print(':: ',len(cache_animation_bau))
    #print(cache_animation_bau)
    offset_x_game, offset_y_game = 100, 70
    
    
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
    status_bar = {'larg_max': 530, 'progresso': 530, 'termino': False} 
    
    def count_bar_time(status_bar, get_time, reset):
        if reset == True:
            blit_bar_time( status_bar['larg_max'] )
            status_bar['termino'] = False
            status_bar['progresso'] = status_bar['larg_max']
            
        if status_bar['termino'] == False:
            valor = status_bar['larg_max']/(get_time/0.2)
            status_bar['progresso'] -= valor
            blit_bar_time( int(status_bar['progresso']) )
            
        if status_bar['progresso'] < 0 :
            status_bar['termino'] = True
        
        if status_bar['termino'] == True:
            blit_bar_time( status_bar['larg_max'] )
            status_bar['progresso'] = status_bar['larg_max']
            
    def blit_bar_time (largura):
        #Blit back
        back_progresso(surface_head, rect_prog)
        
        #Blit maio
        color = color_barra(status_bar)
        pygame.draw.rect(surface_head, color, (170, 18, largura, 28))

        #Blit front
        front_progresso(surface_head, rect_prog)
    
    ## Medindo o tempo do jogador
    def jogadas(click_point, total_jogadas, max_jogadas, history_points, jogada, animation_bau, animation_buraco, sounds):
        
        # Verificando se já acabou o jogo
        if total_jogadas >= max_jogadas:
            pontucao_total_play_01 = history_points['play_01']
            pontucao_total_play_02 = history_points['play_02']
            print(f'>>>> Fim de jogo!! Play_01: {pontucao_total_play_01} | Play_02: {pontucao_total_play_02}')  
            return total_jogadas
        
        # Caso o tempo tenha acabo e houve click
        if status_bar['termino']:
             print("Tempo acabou")
             return total_jogadas

        ## Verificando o click
        player_atual = jogada['player_atual']
        player_anterior = jogada['player_anterior']

        qtd_bau, status, element, click_valido = click(click_user=click_point, matriz=matriz_k,search_elements=search_elements)
        #print('>>>>> ', qtd_bau)
        element_valido = False
        if element and not element in history_rects: 
            element_valido = True
        
        ## Animation
        cache_animation = ''
        
        potucao = 0
        if status == 1:
            potucao = 100
            cache_animation = animation_bau

            sounds['bau'].play()
            
        if status == -1:
            potucao = -50
            cache_animation = animation_buraco
            sounds['buraco'].play()
            
        if status == 0:
            sounds['encontrou_nada'].play()
            
        if click_valido and element_valido:
            
            blit_elements_click.update({
                'validacao': True,
                'status': status, 
                'qtd_bau': qtd_bau,
                'rect_element': element,
                'screen': surface_game,
                'animation': cache_animation
            })
            #print(blit_elements_click)
            
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
            
            count_bar_time(status_bar = status_bar, 
                           get_time = time_clock, 
                           reset = True)
            
            atualizacao_points(surface = surface_point, 
                               history_points = history_points, 
                               name_player = name_player, 
                               back_points = back_points, 
                               pallet_color = pallet_color_)
        return total_jogadas
          
    
    #############################################
    # Inicia o jogo
    blit_play_atual(jogada = jogada,
                    name_player = name_player,
                    pallet_color = pallet_color_,
                    back_player_atual = back_player_atual,
                    surface_head = surface_head)

    atualizacao_points(surface = surface_point, 
                       history_points = history_points, 
                       name_player = name_player, 
                       back_points = back_points, 
                       pallet_color = pallet_color_)
    
    frame_animation = {'frame_atual': 0, 'concluido': False}
    while run:
        display.blit( surface_game, (offset_x_game, offset_y_game))
        display.blit( surface_head, (0, 0) ) 
        display.blit( surface_point , (0, 600))
        
        clock.tick(30)
        time_clock = clock.get_time()
        
        count_bar_time(status_bar = status_bar,
                   get_time = time_clock,
                   reset = None)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                          
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                posicao_click = ( (mouse_x-offset_x_game), (mouse_y-offset_y_game) )
                
                if not blit_elements_click['validacao']:
                    total_jogadas = jogadas (click_point = posicao_click, 
                                            total_jogadas = total_jogadas,
                                            max_jogadas = max_jogadas, 
                                            history_points = history_points, 
                                            jogada = jogada,
                                            animation_bau = cache_animation_bau,
                                            animation_buraco=cache_animation_buraco,
                                            sounds = sounds)
        
        if blit_elements_click['validacao'] and run:
            blit_element(status=blit_elements_click['status'], 
                          qtd_baus=blit_elements_click['qtd_bau'],
                          rect_element=blit_elements_click['rect_element'],
                          screen=blit_elements_click['screen'],
                          animation =blit_elements_click['animation'],
                          frame_animation = frame_animation)
            
            if frame_animation['concluido'] == False:
                frame_animation['frame_atual'] += 1
            
            lista_animation = blit_elements_click['animation']
            if frame_animation['frame_atual'] >= len(lista_animation) -1:
                frame_animation['frame_atual'] = len(lista_animation) -1
                frame_animation['frame_atual'] = 0
                blit_elements_click['validacao'] = False
                
        
        ## 
        if status_bar['termino'] and run:
            player_atual = jogada['player_atual']
            player_anterior = jogada['player_anterior']
            
            jogada['player_atual'] = player_anterior
            jogada['player_anterior'] = player_atual
                
            print(f'TROCA DE TURNO: {jogada["player_atual"]}')
                
            blit_play_atual(jogada = jogada,
                            name_player = name_player,
                            pallet_color = pallet_color_,
                            back_player_atual = back_player_atual,
                            surface_head = surface_head)
            
            count_bar_time(status_bar = status_bar, 
                           get_time = time_clock, 
                           reset = True)

        
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()