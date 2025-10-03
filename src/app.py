import pygame, time
import sys, os
# x, y
# largura. altura

def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    
    ## 'Globais'
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


    #print(cache_animation_bau)
    offset_x_game, offset_y_game = 100, 70
    
    
    w_display, h_display = 700, 700
    ##
    from utils.json_manager import write_json, read_json, write_json_restart
    path_json = os.path.join( os.getcwd(), 'configs', 'parametros.json' )
    path_json_restart = os.path.join( os.getcwd(), 'configs', 'parametros_restart.json' )
    write_json_restart(path_json, path_json_restart)
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
    from logic.click import click, jogadas
      
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
    history_rects = [] # Quais rects já foram clicados
    total_jogadas = 0
    ###############
    
    
    ## Blit da estrutura da barra de regressão do tempo    
    def count_bar_time(status_bar, get_time, reset):
        if reset == True:
            blit_bar_time( status_bar['larg_max'] )
            status_bar['termino'] = False
            status_bar['progresso'] = status_bar['larg_max']
            write_json(path_json, 'status_bar', status_bar)
            
        if status_bar['termino'] == False:
            valor = status_bar['larg_max']/(get_time/0.1)
            status_bar['progresso'] -= valor
            blit_bar_time( int(status_bar['progresso']) )
            write_json(path_json, 'status_bar', status_bar)
            
        if status_bar['progresso'] < 0 :
            status_bar['termino'] = True
            write_json(path_json, 'status_bar', status_bar)
        
        if status_bar['termino'] == True:
            blit_bar_time( status_bar['larg_max'] )
            status_bar['progresso'] = status_bar['larg_max']
            write_json(path_json, 'status_bar', status_bar)
                      
    def blit_bar_time (largura):
        #Blit back
        back_progresso(surface_head, rect_prog)
        
        #Blit maio
        status_bar = read_json(path_json)['status_bar']
        color = color_barra(status_bar)
        pygame.draw.rect(surface_head, color, (170, 18, largura, 28))

        #Blit front
        front_progresso(surface_head, rect_prog)
    #############################################
    # Inicia o jogo
    name_player = read_json(path_json)['name_player']
    jogada = read_json(path_json)['jogada']
    history_points = read_json(path_json)['history_points']
    
    
    blit_play_atual(#jogada = jogada,
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
        
        
        
        #### || JOGO ||
        
        display.blit( surface_game, (offset_x_game, offset_y_game))
        display.blit( surface_head, (0, 0) ) 
        display.blit( surface_point , (0, 600))
        ###
        clock.tick(30)
        time_clock = clock.get_time()
        
        status_bar = read_json(path_json)['status_bar']
        count_bar_time(status_bar = status_bar, get_time = time_clock, reset = None)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                          
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                posicao_click = ( (mouse_x-offset_x_game), (mouse_y-offset_y_game) )
                
            
                ##         
                if not blit_elements_click['validacao']:
                    ## Verificação de qual rect foi clicado {qtd_bau, status, element, click_valido}
                    qtd_bau, status, element, click_valido = click(click_user=posicao_click, matriz=matriz_k, search_elements=search_elements)
                    
                    ## Validação do Click
                    total_jogadas, validacao_jogada = jogadas ( click_valido = click_valido, 
                                                                element = element, 
                                                                status = status,
                                                                total_jogadas = total_jogadas,
                                                                max_jogadas = max_jogadas, 
                                                                history_points = history_points, 
                                                                history_rects = history_rects,
                                                                sounds = sounds ) 
                    if validacao_jogada:
                        if status == 1: cache_animation = cache_animation_bau
                        if status == -1: cache_animation = cache_animation_buraco
                        if status == 0: cache_animation = []

                        blit_elements_click.update({
                                                    'validacao': True,
                                                    'status': status, 
                                                    'qtd_bau': qtd_bau,
                                                    'rect_element': element,
                                                    'screen': surface_game,
                                                    'animation': cache_animation
                                                    })
                        
                        name_player = read_json(path_json)['name_player']

                        blit_play_atual(name_player = name_player,
                                        pallet_color = pallet_color_,
                                        back_player_atual = back_player_atual,
                                        surface_head = surface_head)
            
                        count_bar_time( status_bar = status_bar, 
                                        get_time = time_clock, 
                                        reset = True )
            
                        atualizacao_points( surface = surface_point, 
                                            history_points = history_points, 
                                            name_player = name_player, 
                                            back_points = back_points, 
                                            pallet_color = pallet_color_ )
        

        if blit_elements_click['validacao'] and run:
            
            blit_element( status=blit_elements_click['status'], 
                          qtd_baus=blit_elements_click['qtd_bau'],
                          rect_element=blit_elements_click['rect_element'],
                          screen=blit_elements_click['screen'],
                          animation =blit_elements_click['animation'],
                          frame_animation = frame_animation )
            
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
            write_json(path_json, 'jogada', jogada)
             
            print(f'TROCA DE TURNO: {jogada["player_atual"]}')
                
            blit_play_atual(name_player = name_player,
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
    