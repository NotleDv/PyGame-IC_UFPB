import pygame, time
import sys, os
from dotenv import load_dotenv
from pygame.locals import * 

def cache_sound ():
    pygame.mixer.init()
    pygame.mixer.set_num_channels(32)
    pygame.mixer.set_reserved(4) 
    
    # Canais
    canal_musica = pygame.mixer.Channel(0)
    canal_sfx_bau = pygame.mixer.Channel(1)
    canal_sfx_buraco = pygame.mixer.Channel(2)
    canal_sfx_nada = pygame.mixer.Channel(3)
    
    # Música de fundo (BG = background)
    sound_bg = pygame.mixer.Sound('../assets/Sounds/sound_bg.wav')
    sound_bg.set_volume(0.2)
    # CORREÇÃO: Toque a música no canal que você reservou para ela
    canal_musica.play(sound_bg, -1) # -1 para tocar em loop
    
    # Efeitos Sonoros (SFX = sound effects)
    encontrou_nada_sound = pygame.mixer.Sound('../assets/Sounds/encontrou_nada.wav')
    bau_sound = pygame.mixer.Sound('../assets/Sounds/bau.wav')
    buraco_sound = pygame.mixer.Sound('../assets/Sounds/buraco.wav')
    
    bau_sound.set_volume(0.5)
    buraco_sound.set_volume(0.1)
    encontrou_nada_sound.set_volume(0.1)
    
    # CORREÇÃO: Retorne os sons E os canais em um único dicionário
    result = {
        'sfx': {
            'nada': encontrou_nada_sound,
            'bau': bau_sound,
            'buraco': buraco_sound
        },
        'channels': {
            'musica': canal_musica,
            'bau': canal_sfx_bau,
            'buraco': canal_sfx_buraco,
            'nada': canal_sfx_nada
        }
    }
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
    pygame.key.set_repeat(300, 30)
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
    from utils.background import background_surface_game, background_display, back_player_atual, back_points, background_display_menu, background_display_escolha_nomes, background_final
    
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
    from logic.blit_elements import blit_element, blit_play_atual, atualizacao_points, blit_name_player
    
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
    ###############
    
    # Inicia o jogo
    jogada = read_json(path_json)['jogada']
    history_points = read_json(path_json)['history_points']
    
    ### Responsáveis por orquestrar 
    blit_elements_click = {'status': 0, 'validacao': False, 'qtd_bau': None, 'rect_element': None, 'screen': None, 'animation': None}
    
    ## É para deslocar a surface do game, deixando ela centralizada
    offset_x_game, offset_y_game = 100, 70
    from dotenv import load_dotenv
    load_dotenv()
    path_json = os.getenv("PATH_JSON")
    path_json_restart = os.getenv("PATH_JSON_RESTART")
    
    ## Carregando o modulo para manipulação do json
    from utils.json_manager import write_json, read_json, write_json_restart
    write_json_restart(path_json, path_json_restart)
    
    ## ------------------------------------------------------------------------
    pygame.key.set_repeat(300, 30)

    from configs.rect_button_and_player import rect_button, rect_player
    button_start, bot_retorno, bot_avançar = rect_button()
    campo_player1, campo_player2 = rect_player()

    
    tela_atual = "menu"



    cursor_visivel = True
    ultimo_tempo_alternancia = pygame.time.get_ticks()
    tempo_alternancia = 500 

    run = True
    ### Rian
    def troca_tela(event):
        if event.type == MOUSEBUTTONDOWN:
            tela_atual = read_json(path_json)['tela_atual']
            
            ## Alterar entre as telas
            if tela_atual == "menu":
                if button_start.collidepoint(event.pos):
                    tela_atual = "tela_escolha_nome"
                    write_json(path_json, 'tela_atual', tela_atual)
            
            if tela_atual == "tela_escolha_nome":
                if bot_retorno.collidepoint(event.pos):
                    tela_atual = "menu"
                    write_json(path_json, 'tela_atual', tela_atual)
                    
                if campo_player1.collidepoint(event.pos):
                    campo_ativo = 1
                elif campo_player2.collidepoint(event.pos):
                    campo_ativo = 2
                    
                if bot_avançar.collidepoint(event.pos):
                    tela_atual = "jogo"
                    write_json(path_json, 'tela_atual', tela_atual)
    
    def tela_nomes(sreen):
        campo_ativo = read_json(path_json)['campo_ativo_name'] 
    
        background_display_escolha_nomes(display)
        blit_name_player(display, campo_player1, campo_player2)

        name_player = read_json(path_json)['name_player']
        
        
        fonte = pygame.font.SysFont(None, 50)
        if campo_ativo == 1 and cursor_visivel:
            # Calcula a largura usando o texto ATUAL do JSON
            largura_texto = fonte.size(name_player['play_01'])[0]
            
            # Coordenadas para desenhar a linha
            x_cursor = campo_player1.x + 10 + largura_texto
            y_inicio = campo_player1.y + 8
            y_fim = campo_player1.y + 40
            pygame.draw.line(sreen, (60, 60, 60), (x_cursor, y_inicio), (x_cursor, y_fim), 5)
            
        if campo_ativo == 2 and cursor_visivel:
            # Calcula a largura usando o texto ATUAL do JSON
            largura_texto = fonte.size(name_player['play_01'])[0]
            
            # Coordenadas para desenhar a linha
            x_cursor = campo_player1.x + 10 + largura_texto
            y_inicio = campo_player1.y + 8
            y_fim = campo_player1.y + 40
            pygame.draw.line(sreen, (60, 60, 60), (x_cursor, y_inicio), (x_cursor, y_fim), 5)
    
    def input_text_user(event):
        tela_atual = read_json(path_json)['tela_atual']
        campo_ativo = read_json(path_json)['campo_ativo_name']
        
        ## Verifica se o jogador dois apertou o Enter 
        if event.type == pygame.KEYDOWN and tela_atual == "tela_escolha_nome" and campo_ativo == 2:
            if event.key == pygame.K_RETURN:
                tela_atual = "jogo"
                write_json(path_json, 'tela_atual', tela_atual)

        
        if event.type == pygame.KEYDOWN and tela_atual == "tela_escolha_nome":
            ## Verifica se foi apertado ENTER
            if event.key == pygame.K_RETURN:
                campo_ativo = 2 if campo_ativo == 1 else 1
                write_json(path_json, 'campo_ativo_name', campo_ativo)
            
            ## Apagar a escrita se necessário
            campo_ativo = read_json(path_json)['campo_ativo_name']
            if event.key == pygame.K_BACKSPACE:
                name_player = read_json(path_json)['name_player']
                
                if campo_ativo == 1:
                    name_player['play_01'] = name_player['play_01'][:-1]
                else:
                    name_player['play_02'] = name_player['play_02'][:-1]
                    
                write_json(path_json, 'name_player', name_player)
            
            ## 
            if event.unicode.isprintable() and len(event.unicode) > 0:
                name_player = read_json(path_json)['name_player']
                
                if campo_ativo == 1:
                    name_player['play_01'] += event.unicode
                else:
                    name_player['play_02'] += event.unicode
                
                write_json(path_json, 'name_player', name_player)
            
    ## Elton
    def verificacao_quantidade_partidas():
        # Verificando se já acabou o jogo
        path_json = os.getenv("PATH_JSON")
        total_jogadas = read_json(path_json)['total_jogos']
        
        if total_jogadas >= max_jogadas:
            pontucao_total_play_01 = history_points['play_01']
            pontucao_total_play_02 = history_points['play_02']
            print(f'>>>> Fim de jogo!! Play_01: {pontucao_total_play_01} | Play_02: {pontucao_total_play_02}')  
            
            tela_atual = read_json(path_json)['tela_atual']
            tela_atual = 'final'
            write_json(path_json, 'tela_atual', tela_atual)
            
            # tela_atual = read_json(path_json)['tela_atual']
            # print('>>>>>>> ', tela_atual)
            
            return False
        return True
    
    def game(event, time_clock, blit_elements_click, history_rects):
       
        status_bar = read_json(path_json)['status_bar']
        count_bar_time(status_bar = status_bar, get_time = time_clock, reset = None)
        
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
                                             
                        ## Atualiza o nome que está ao lado da barra de tempo 
                        blit_play_atual(back_player_atual = back_player_atual,
                                        surface_head = surface_head)

                        ## Reset na barra de tempo
                        count_bar_time( status_bar = status_bar, 
                                        get_time = time_clock, 
                                        reset = True )

                        ## Atualiza a pontuação no rodapé
                        atualizacao_points( surface = surface_point, 
                                            background_points = back_points)
    
    def animation(run, blit_elements_click):
        frame_animation = read_json(path_json)['frame_animation']
        
        if blit_elements_click['validacao'] and run:
            
            blit_element( rect_element=blit_elements_click['rect_element'],
                          screen=blit_elements_click['screen'],
                          animation =blit_elements_click['animation'],
                          frame_animation = frame_animation )
            
            if frame_animation['concluido'] == False:
                frame_animation['frame_atual'] += 1
                write_json(path_json, 'frame_animation', frame_animation)
            
            lista_animation = blit_elements_click['animation']
            if frame_animation['frame_atual'] >= len(lista_animation) -1:
                frame_animation['frame_atual'] = len(lista_animation) -1
                frame_animation['frame_atual'] = 0
                write_json(path_json, 'frame_animation', frame_animation)
                
                blit_elements_click['validacao'] = False
    
    def bar_time(run, blit_play_atual, count_bar_time):
        status_bar = read_json(path_json)['status_bar']
        if status_bar['termino'] and run:
            player_atual = jogada['player_atual']
            player_anterior = jogada['player_anterior']
            
            jogada['player_atual'] = player_anterior
            jogada['player_anterior'] = player_atual
            write_json(path_json, 'jogada', jogada)
             
            print(f'TROCA DE TURNO: {jogada["player_atual"]}')
                
            blit_play_atual(back_player_atual = back_player_atual,
                            surface_head = surface_head)
            
            count_bar_time(status_bar = status_bar, 
                           get_time = time_clock, 
                           reset = True)
    
    def update_display_game(time_clock, blit_elements_click):
        """Esta função é chamada a cada quadro para desenhar e animar."""
        if count_background == 0: background_display(display)
        
        display.blit(surface_game, (offset_x_game, offset_y_game))
        display.blit(surface_head, (0, 0))
        display.blit(surface_point, (0, 600))
        
        # Desenha os elementos estáticos
        if count_background == 0:    
            ## Exibir a pontuação em baixo, e o nome do jogar ao lado da barra
            atualizacao_points( surface=surface_point, background_points=back_points )
            blit_play_atual(back_player_atual = back_player_atual, surface_head = surface_head)
            
        
        # Funções que rodam continuamente
        status_bar = read_json(path_json)['status_bar']
        count_bar_time(status_bar, time_clock, reset=None)
        animation(run, blit_elements_click)
        bar_time(run, blit_play_atual, count_bar_time)
    
    ## Rian 2         
                             
    def tabela(screen):
        load_dotenv()
        path_json = os.getenv("PATH_JSON")
        pontuação = read_json(path_json)["history_points"]
        name_player = read_json(path_json)["name_player"]
        
        #placar com pontuação e nomes dos jogadores, com a maior pontuação sendo sempre a primeira
        name_ganhador, name_perdedor = '', ''
        pontuação_ganhador, pontuacao_perdedor = 0, 0
        
        if pontuação["play_01"] > pontuação["play_02"]: 
            name_ganhador = name_player["play_01"]
            name_perdedor = name_player["play_02"]
            pontuação_ganhador, pontuacao_perdedor = pontuação["play_01"], pontuação["play_02"]
        else:
            name_ganhador = name_player["play_02"]
            name_perdedor = name_player["play_01"]
            pontuação_ganhador, pontuacao_perdedor = pontuação["play_02"], pontuação["play_01"]
        
        base_rect_texto_1 = pygame.Rect((165,250, 173, 65))
        base_rect_texto_2 = pygame.Rect((183,340, 160, 55))
        
        base_rect_potuacao_1 = pygame.Rect((425,250, 103, 65))
        base_rect_potuacao_2 = pygame.Rect((423,340, 90, 55))

                
        font_1 = fonts(50, 'default')
        texto_1 = font_1.render(name_ganhador, True, pallet_color_['cinza'])
        rect_texto_1 = texto_1.get_rect(center=base_rect_texto_1.center)
        screen.blit(texto_1, rect_texto_1)
        
        font_2 = fonts(40, 'default')
        texto_2 = font_2.render(name_perdedor, True, pallet_color_['cinza'])
        rect_texto_2 = texto_2.get_rect(center=base_rect_texto_2.center)
        screen.blit(texto_2, rect_texto_2)
        
        font_3 = fonts(70, 'default')
        texto_3 = font_3.render(str(pontuação_ganhador), True, pallet_color_['cinza'])
        rect_texto_3 = texto_3.get_rect(center=base_rect_potuacao_1.center)
        screen.blit(texto_3, rect_texto_3)
        
        font_4 = fonts(60, 'default')
        texto_4 = font_4.render(str(pontuacao_perdedor), True, pallet_color_['cinza'])
        rect_texto_4 = texto_4.get_rect(center=base_rect_potuacao_2.center)
        screen.blit(texto_4, rect_texto_4)


    event = ''
    count_background = 0
    
    click_restart = False
    while run:
        
        clock.tick(30)
        time_clock = clock.get_time()
        
        tela_atual = read_json(path_json)['tela_atual']
        
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - ultimo_tempo_alternancia >= tempo_alternancia:
            cursor_visivel = not cursor_visivel
            ultimo_tempo_alternancia = tempo_atual
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            troca_tela(event)
            input_text_user(event)
            
            if verificacao_quantidade_partidas():
                if tela_atual == "jogo" and event.type == MOUSEBUTTONDOWN:               
                    game(event, time_clock, blit_elements_click, history_rects)
                    
            if tela_atual == "final":
                rect_return = pygame.Rect(538, 469, 41, 37)
                if rect_return.collidepoint(event.pos):
                    click_restart = True
                    print("Botão de reiniciar clicado!")
                    write_json_restart(path_json, path_json_restart)   

            
        if tela_atual == "menu":
            background_display_menu(display)

        if tela_atual == "tela_escolha_nome":
            tela_nomes(display)

        if tela_atual == "jogo":
            update_display_game(time_clock, blit_elements_click)
        
        if tela_atual == "final":
            if not blit_elements_click['validacao']:
                background_final(display)
                tabela(display) 
                if click_restart:
                    history_rects = []
                    blit_elements_click = {'status': 0, 'validacao': False, 'qtd_bau': None, 'rect_element': None, 'screen': None, 'animation': None}
                    background_display(display)
                    matriz_k = create_matriz(width = w_game, height = h_game)
                    background_surface_game(screen=surface_game, matriz=matriz_k)
                    click_restart = False
        
            
        pygame.display.update()

if __name__ == '__main__':
    main()
    