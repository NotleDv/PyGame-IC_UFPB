import pygame
import sys, threading
import random
from rich.traceback import install
install()
## x, y
## largura. altura
def main():
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
    from utils.background import background_surface_game, background_display
    background_surface_game(screen=surface_game,
               matriz=matriz_k)

    background_display(display)
    ##
    from utils.fonts import main as fonts                
      
    ##
    from logic.blit_elements import main as blit_elements  
    
    ##
    from logic.click import click
      
    ##
    from logic.search_elements import search_elements  
    #background(screen=surface_game, matriz=matriz_k)
    
    for i in matriz_k:
        print('| ', end='')
        for j in i:
            print(j['valor'], end=' ')
        print(' |')
        
    run = True
    
    ###############
    status_bar = {'progresso': 0, 'termino': False}
    max_trabalho = 300
    import time
    # def trabalhar():
    #     for i in range(max_trabalho):
    #         status_bar["progresso"] = i
    #         pygame.time.delay(20)
    #     status_bar["terminou"] = True
    
    pygame.draw.rect(surface_head, (255, 255, 255), (170, 10, 530, 40))
    
    ###############
    
    max_jogadas = 15
    history_points = {'play_01': 0, 'play_02':0}
    history_rects = []
    
    jogada = {'jogada_atual':0 , 'player_atual': 'play_01','jogada_anterior':0 , 'player_anterior': 'play_02'}
    total_jogadas = 0
    
    def jogadas(click_point, total_jogadas, max_jogadas, history_points, jogada):
        if total_jogadas <= max_jogadas:
            player_atual = jogada['player_atual']
            player_anterior = jogada['player_anterior']
            
            if player_atual != player_anterior:
                
                qtd_bau, status, element, validacao = click(click_user=click_point, matriz=matriz_k,search_elements=search_elements)
                
                               
                validacao_2 = False
                if not element in history_rects: validacao_2 = True
                
                print('>>>>>>>>>> ', element)
                potucao = 0
                if status == 1:
                    potucao = 100
                if status == -1:
                    potucao = -50
                    
                if validacao and validacao_2:
                    blit_elements(status=status, 
                                    qtd_baus=qtd_bau,
                                    rect_element=element,
                                    screen=surface_game)
                    
                    for key, value_ in history_points.items():
                        if player_atual == key:
                            history_points[key] += potucao
                            verificao_points = history_points[key]
                            if verificao_points < 0:
                                history_points[key] = 0
                                
                    jogada['player_atual'] = player_anterior
                    jogada['player_anterior'] = player_atual
                    total_jogadas+=1
                    
                    history_rects.append(element)
                    
                print(history_points)
                print(jogada)
                
        else:
            pontucao_total_play_01 = history_points['play_01']
            pontucao_total_play_02 = history_points['play_02']
            print(f'>>>> Fim de jogo!! Play_01: {pontucao_total_play_01} | Play_02: {pontucao_total_play_02}')  
       
        return total_jogadas  
                

            
    #threading.Thread(target=trabalhar).start()
    ###############
    while run:
        
        display.blit( surface_game, (offset_x_game, offset_y_game))
        ## For de eventos
        for event in pygame.event.get():
            ## Fechamento
            if event.type == pygame.QUIT:
                run = False
                exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                mouse_x, mouse_y = pygame.mouse.get_pos()
                posicao_click = ( (mouse_x-offset_x_game), (mouse_y-offset_y_game))
                total_jogadas = jogadas(posicao_click, total_jogadas, max_jogadas, history_points, jogada)
                print(total_jogadas)
                            
        display.blit( surface_head, (0, 0) ) 
        
        # pygame.draw.rect(surface_head, (255,255,0), rect=((0,0) , (1000,1000)))
        #surface_game = surface_game.convert_alpha()
        # display.blit( surface_point, (0 , 700) )
        # calcula largura da barra de acordo com progresso
        largura = int((status_bar['progresso'] / max_trabalho) * 400)  
        #pygame.draw.rect(surface_head, (255, 255, 255), (0, 0, largura, 40))

    # if status_bar['termino']:
    #     font = pygame.font.SysFont("Arial", 40)
    #     txt = font.render("Concluído!", True, (0, 255, 0))
    #     surface_head.blit(txt, (300, 320))
        
        pygame.display.update()

    pygame.quit()
    

if __name__ == '__main__':
    main()

