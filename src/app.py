import pygame, time
import sys, os
from dotenv import load_dotenv
from pygame.locals import * 

def cache_sound ():
    pygame.mixer.init()
    pygame.mixer.set_reserved(4) 
    
    # Canais
    canal_musica = pygame.mixer.Channel(0)
    canal_sfx_bau = pygame.mixer.Channel(1)
    canal_sfx_buraco = pygame.mixer.Channel(2)
    canal_sfx_nada = pygame.mixer.Channel(3)
    
    # Música de fundo (BG = background)
    sound_bg = pygame.mixer.Sound('../assets/Sounds/sound_bg.wav')
    sound_bg.set_volume(0.6)
    canal_musica.play(sound_bg, -1) # -1 para tocar em loop
    
    # Efeitos Sonoros (SFX = sound effects)
    encontrou_nada_sound = pygame.mixer.Sound('../assets/Sounds/encontrou_nada.wav')
    bau_sound = pygame.mixer.Sound('../assets/Sounds/bau.wav')
    buraco_sound = pygame.mixer.Sound('../assets/Sounds/buraco.wav')
    
    bau_sound.set_volume(0.5)
    buraco_sound.set_volume(0.1)
    encontrou_nada_sound.set_volume(0.1)
    
    # Retorne os sons E os canais em um único dicionário
    result = {
        'sfx': {
            'nada': encontrou_nada_sound,
            'bau': bau_sound,
            'buraco': buraco_sound
        },
        'channels': {
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
    clock = pygame.time.Clock()
    run = True
    
    sounds = cache_sound()
    
    tela_atual = "menu"

    
    ## --------------------------------------------------------------------
    ## Cache animation 
    from utils.animation import load_animation_bau, load_animation_buraco, animation
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
    matriz_k = create_matriz(width = w_game, height = h_game)
    
    ## --------------------------------------------------------------------
    ## Carregando o modulo com os backgrounds 
    from utils.background import background_surface_game, background_display, back_player_atual, back_points, background_display_menu, background_final

    #background_display(display)
      
    ## --------------------------------------------------------------------
    ## Carregando o modulo com as cores
    from utils.pallet_color import color_barra
    
    ## --------------------------------------------------------------------
    ## Outros modulos
    
    #2 - Todos os blits
    from logic.blit_elements import blit_play_atual, atualizacao_points, blit_tabela_final
    
    #3 - Lógica de click e validação de jogada
    from logic.click import click, jogadas
    
    ## --------------------------------------------------------------------
    ## Carregando o modulo com os backgrounds 
    from utils.background import back_progresso, front_progresso
    
    ## --------------------------------------------------------------------
    ## Troca de Tela
    from logic.troca_de_tela import troca_tela
    
    ## --------------------------------------------------------------------
    ## Tanto para aparecer o nome, quanto para salvar
    from logic.name_user import barrinha_da_tela_de_nomes, input_text_user
    
    ## Funções Relacionadas a Barra de Tempo
    rect_barra_tempo = pygame.Rect((170, 10, 530, 40))
    ### Calculo do tamanho da barra
    def count_bar_time(status_bar, reset):
        total_jogadas = read_json(path_json)['total_jogos']
        if total_jogadas < 16:
            
            if reset == True:
                blit_bar_time( status_bar['larg_max'] )
                status_bar['termino'] = False
                status_bar['progresso'] = status_bar['larg_max']
                write_json(path_json, 'status_bar', status_bar)
                
            if status_bar['termino'] == False:
                status_bar['progresso'] -= 2
                blit_bar_time( int(status_bar['progresso']) )
                write_json(path_json, 'status_bar', status_bar)
                
            if status_bar['progresso'] < 0 :
                status_bar['termino'] = True
                write_json(path_json, 'status_bar', status_bar)
            
            if status_bar['termino'] == True:
                blit_bar_time( status_bar['larg_max'] )
                status_bar['progresso'] = status_bar['larg_max']
                write_json(path_json, 'status_bar', status_bar)
    
    ### Atualização do tamanho da barra
    def blit_bar_time (largura):
        #Blit back
        back_progresso(surface_head, rect_barra_tempo)
        
        status_bar = read_json(path_json)['status_bar']
        color = color_barra(status_bar)
        pygame.draw.rect(surface_head, color, (170, 18, largura, 28))

        #Blit front
        front_progresso(surface_head, rect_barra_tempo)
        
    ### Troca de play pelo tempo da barra
    def bar_time(run, blit_play_atual, count_bar_time):
        status_bar = read_json(path_json)['status_bar']
        
        if status_bar['termino'] and run:
            jogada = read_json(path_json)['jogada']
            player_atual = jogada['player_atual']
            player_anterior = jogada['player_anterior']
            
            jogada['player_atual'] = player_anterior
            jogada['player_anterior'] = player_atual
            write_json(path_json, 'jogada', jogada)
             
            print(f'TROCA DE TURNO: {jogada["player_atual"]}')
                
            blit_play_atual(back_player_atual = back_player_atual,
                            surface_head = surface_head)
            
            count_bar_time(status_bar = status_bar, 
                           reset = True)
    
    ## Orquestramento da parte visual da tela 'jogo'
    def update_display_game(count_background):
        
        display.blit(surface_game, (offset_x_game, offset_y_game))
        display.blit(surface_head, (0, 0))
        display.blit(surface_point, (0, 600))
        
        """Esta função é chamada a cada quadro para desenhar e animar."""
        if count_background == 0: 
            background_display(display)
            background_surface_game(screen=surface_game,
                            matriz=matriz_k)
            
                # Desenha os elementos estáticos
           
        ## Exibir a pontuação em baixo, e o nome do jogar ao lado da barra
        atualizacao_points( surface=surface_point, background_points=back_points )
        blit_play_atual(back_player_atual = back_player_atual, surface_head = surface_head)
            
        
        # Funções que rodam continuamente
        status_bar = read_json(path_json)['status_bar']
        count_bar_time(status_bar, reset=None)
        bar_time(run, blit_play_atual, count_bar_time)
        
          
    ###############
    max_jogadas = 16
    history_rects = [] # Quais rects já foram clicados
    ###############
      
    ### Responsáveis por orquestrar 
    blit_elements_click = {'status': 0, 'validacao': False, 'qtd_bau': None, 'rect_element': None, 'screen': None, 'animation': None}
    
    ## É para deslocar a surface do game, deixando ela centralizada
    offset_x_game, offset_y_game = 100, 70
    path_json = os.getenv("PATH_JSON")
    path_json_restart = os.getenv("PATH_JSON_RESTART")
    
    ## --------------------------------------------------------------------
    ### Retorna os rect para os botões para retornar, start...
    from configs.rect_button_and_player import rect_button, rect_player
    button_start, bot_retorno, bot_avançar = rect_button()
    campo_player1, campo_player2 = rect_player()

    ### Rian
    from logic.troca_de_tela import troca_tela
    
    from logic.name_user import barrinha_da_tela_de_nomes, input_text_user


    def verificacao_quantidade_partidas():
        # Verificando se já acabou o jogo
        path_json = os.getenv("PATH_JSON")
        total_jogadas = read_json(path_json)['total_jogos']
        
        if total_jogadas >= max_jogadas:
            tela_atual = read_json(path_json)['tela_atual']
            tela_atual = 'final'
            write_json(path_json, 'tela_atual', tela_atual)
            
            return False
        return True
    
    def game(event, blit_elements_click, history_rects):
       
        status_bar = read_json(path_json)['status_bar']
        count_bar_time(status_bar = status_bar, reset = None)
        
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
                                    reset = True )

                    ## Atualiza a pontuação no rodapé
                    atualizacao_points( surface = surface_point, 
                                        background_points = back_points)

    event = ''
    count_background = 0
    
    click_restart = False
    while run:
        
        clock.tick(30)
        
        tela_atual = read_json(path_json)['tela_atual']
               
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            troca_tela(event, button_start, bot_retorno, bot_avançar, campo_player1, campo_player2)
            input_text_user(event)
            
            if verificacao_quantidade_partidas():
                if tela_atual == "jogo" and event.type == MOUSEBUTTONDOWN:               
                    game(event, blit_elements_click, history_rects)
                    
            if tela_atual == "final":
                rect_return = pygame.Rect(538, 469, 41, 37)
                if event.type == MOUSEBUTTONDOWN:
                    if rect_return.collidepoint(event.pos):
                        click_restart = True
                        print("Botão de reiniciar clicado!")
                        write_json_restart(path_json, path_json_restart)   

            
        if tela_atual == "menu":
            background_display_menu(display)

        if tela_atual == "tela_escolha_nome":
            barrinha_da_tela_de_nomes(display, campo_player1, campo_player2)

        if tela_atual == "jogo":
            update_display_game(count_background)
            count_background+=1
        
        if blit_elements_click['validacao']:
            animation(run, blit_elements_click)
            
        if tela_atual == "final" and not blit_elements_click['validacao']:
            background_final(display)
            blit_tabela_final(display) 
            
            if click_restart:
                history_rects = []
                blit_elements_click = {'status': 0, 'validacao': False, 'qtd_bau': None, 'rect_element': None, 'screen': None, 'animation': None}

                click_restart = False
                count_background = 0
                    
        
        
            
        pygame.display.update()

if __name__ == '__main__':
    main()
    