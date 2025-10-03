import pygame, time
import sys, os
from dotenv import load_dotenv
# x, y
# largura. altura
def cache_sound ():
    ## Carregando as músicas
    encontrou_nada_sound = pygame.mixer.Sound('../assets/Sounds/encontrou_nada.wav')
    bau_sound = pygame.mixer.Sound('../assets/Sounds/bau.wav')
    buraco_sound = pygame.mixer.Sound('../assets/Sounds/buraco.wav')
    
    ## Modificando o volume
    bau_sound.set_volume(0.5)
    buraco_sound.set_volume(0.1)
    encontrou_nada_sound.set_volume(0.1)
    
    result = {'encontrou_nada': encontrou_nada_sound,
              'bau': bau_sound,
              'buraco': buraco_sound}
    
    return result

def main():
    from dotenv import load_dotenv
    load_dotenv()
    path_json = os.getenv("PATH_JSON")
    path_json_restart = os.getenv("PATH_JSON_RESTART")
    
    ## Inicializações do pygame
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    run = True
    
    sounds = cache_sound()
    
    ## --------------------------------------------------------------------
    ## Cache animation 
    from utils.animation import load_animation_bau, load_animation_buraco
    cache_animation_bau = load_animation_bau()
    cache_animation_buraco = load_animation_buraco()

    ## --------------------------------------------------------------------
    ## Screens do Cabeçalho, Centro e Rodapé
    from configs.screen import config_screens as screens
    config_screen = screens(w_display=700, h_display=700)
    
    w_game, h_game= config_screen[1] # Posições H e W da surface de game, posição H da surface do cabeçalho
    display, surface_game, surface_point, surface_head = config_screen[0] # Surfaces e Display
    
    ## --------------------------------------------------------------------
    ## Carregando o modulo para manipulação do json
    from utils.json_manager import write_json, read_json, write_json_restart
    write_json_restart(path_json, path_json_restart)
    
    ## --------------------------------------------------------------------
    ## Carregando o modulo com as matrizes
    from logic.matriz import main as create_matriz
    matriz_k = create_matriz(width = w_game,
                             height = h_game)
    
    ## --------------------------------------------------------------------
    ## Carregando o modulo com os backgrounds 
    from utils.background import background_surface_game, background_display, back_player_atual, back_points
    background_surface_game(screen=surface_game,
                            matriz=matriz_k)

    background_display(display)
    
    ## --------------------------------------------------------------------
    ## Carregando o modulo com as cores
    from utils.pallet_color import pallet_color, color_barra
    pallet_color_ = pallet_color()
    
    ## --------------------------------------------------------------------
    ## Outros modulos
    #1 - Fonts
    from utils.fonts import main as fonts 
    
    #2 - Todos os blits
    from logic.blit_elements import blit_element, blit_play_atual, atualizacao_points
    
    #3 - Lógica de click e validação de jogada
    from logic.click import click, jogadas
    
    ## --------------------------------------------------------------------
    ## Carregando o modulo com os backgrounds 
    from utils.background import back_progresso, front_progresso
    rect_barra_tempo = pygame.Rect((170, 10, 530, 40))
    
    def count_bar_time(status_bar, get_time, reset):
        total_jogadas = read_json(path_json)['total_jogos']
        if total_jogadas < 16:
            
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
        back_progresso(surface_head, rect_barra_tempo)
        
        status_bar = read_json(path_json)['status_bar']
        color = color_barra(status_bar)
        pygame.draw.rect(surface_head, color, (170, 18, largura, 28))

        #Blit front
        front_progresso(surface_head, rect_barra_tempo)

    
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
    
    # Inicia o jogo
    name_player = read_json(path_json)['name_player']
    jogada = read_json(path_json)['jogada']
    history_points = read_json(path_json)['history_points']
    
    
    blit_play_atual(name_player = name_player,
                    pallet_color = pallet_color_,
                    back_player_atual = back_player_atual,
                    surface_head = surface_head)

    atualizacao_points(surface = surface_point,
                       background_points = back_points, 
                       pallet_color = pallet_color_)
    
    ### Responsáveis por orquestrar 
    frame_animation = {'frame_atual': 0, 'concluido': False}
    blit_elements_click = {'status': 0, 'validacao': False, 'qtd_bau': None, 'rect_element': None, 'screen': None, 'animation': None}
    
    ## É para deslocar a surface do game, deixando ela centralizada
    offset_x_game, offset_y_game = 100, 70
    
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
                if not blit_elements_click['validacao']: #val= True (animação em andamento), val = False (animação finalizada). Trava enquanto animação tá em andamento
                    
                    ## 1. Valido o click
                    element = click(click_user=posicao_click, matriz=matriz_k)
                    
                    result_modulo_click = read_json(path_json)['return_click']
                    
                    ## 2. Valido a jogada
                    validacao_jogada, history_rects = jogadas ( click_valido = result_modulo_click['click_valido'], 
                                                                               element = element, 
                                                                               status = result_modulo_click['status'],
                                                                               max_jogadas = max_jogadas, 
                                                                               history_rects = history_rects,
                                                                               sounds = sounds ) 
                    ## 3. Jogada foi válida?
                    if validacao_jogada:
                        if result_modulo_click['status'] == 1: cache_animation = cache_animation_bau
                        if result_modulo_click['status'] == -1: cache_animation = cache_animation_buraco
                        if result_modulo_click['status'] == 0: cache_animation = []

                        ## Atualiza as informações a serem repassadas ao blit que faz animação
                        blit_elements_click.update({
                                                    'validacao': True,
                                                    'status': result_modulo_click['status'], 
                                                    'qtd_bau': result_modulo_click['qtd_bau'],
                                                    'rect_element': element,
                                                    'screen': surface_game,
                                                    'animation': cache_animation
                                                    })
                        
                        name_player = read_json(path_json)['name_player']
                        
                        ## Atualiza o nome que está ao lado da barra de tempo 
                        blit_play_atual(name_player = name_player,
                                        pallet_color = pallet_color_,
                                        back_player_atual = back_player_atual,
                                        surface_head = surface_head)

                        ## Reset na barra de tempo
                        count_bar_time( status_bar = status_bar, 
                                        get_time = time_clock, 
                                        reset = True )

                        ## Atualiza a pontuação no rodapé
                        atualizacao_points( surface = surface_point, 
                                            background_points = back_points, 
                                            pallet_color = pallet_color_ )
        

        if blit_elements_click['validacao'] and run:
            
            blit_element( rect_element=blit_elements_click['rect_element'],
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
    