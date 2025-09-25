import pygame
import sys
import random
from rich.traceback import install
install()
## x, y
## largura. altura
def main():
    
    name_01 = 'Elton_A1'
    name_02 = 'Etlon_A2'
    
    pygame.init()
    pygame.font.init()
    
    w_display, h_display = 1000, 800
    
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
    from utils.background import main as background
    background(screen=surface_game,
               matriz=matriz_k)

    ##
    from utils.fonts import main as fonts                
      
    ##
    from logic.blit_elements import main as blit_elements  
    
    ##
    from logic.click import click
      
    ##
    from logic.search_elements import search_elements  
    background(screen=surface_game, matriz=matriz_k)
    
    for i in matriz_k:
        print('| ', end='')
        for j in i:
            print(j['valor'], end=' ')
        print(' |')
        
    run = True
    
    ###############
    
    max_jogadas = 15
    history_points = {'play_01': 0, 'play_02':0}
    
    jogada = {'jogada_atual':0 , 'player_atual': 'play_01', 'name_play': name_01,'jogada_anterior':0 , 'player_anterior': 'play_02'}
    total_jogadas = 0
    
    def jogadas(click_point, total_jogadas, max_jogadas, history_points, jogada):
        if total_jogadas <= max_jogadas:
            player_atual = jogada['player_atual']
            player_anterior = jogada['player_anterior']
            if player_atual != player_anterior:
                
                qtd_bau, status, element, validacao = click(click_user=click_point, matriz=matriz_k,search_elements=search_elements)
                
                blit_elements(status=status, 
                                qtd_baus=qtd_bau,
                                rect_element=element,
                                screen=surface_game)
                potucao = 0
                if status == 1:
                    potucao = 100
                if status == -1:
                    potucao = -50
                    
                if validacao:
                    for key, value_ in history_points.items():
                        if player_atual == key:
                            history_points[key] += potucao
                            verificao_points = history_points[key]
                            if verificao_points < 0:
                                history_points[key] = 0
                                
                    jogada['player_atual'] = player_anterior
                    jogada['player_anterior'] = player_atual
                    total_jogadas+=1
                print(history_points)
                print(jogada)
        else:
            pontucao_total_play_01 = history_points['play_01']
            pontucao_total_play_02 = history_points['play_02']
            print(f'>>>> Fim de jogo!! Play_01: {pontucao_total_play_01} | Play_02: {pontucao_total_play_02}')  
       
        return total_jogadas  
                

            
    
    ###############
    while run:
        
        ## For de eventos
        for event in pygame.event.get():
            ## Fechamento
            if event.type == pygame.QUIT:
                run = False
                exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posicao_click = pygame.mouse.get_pos()
                
                total_jogadas = jogadas(posicao_click, total_jogadas, max_jogadas, history_points, jogada)
                print(total_jogadas)
                
                # print(posicao_click)
                # qtd_bau, status, element = click(click_user=posicao_click,
                #                                  matriz=matriz_k,
                #                                  search_elements=search_elements)
                # print(f'{qtd_bau} | {status} | {element}')
                # blit_elements(status=status, 
                #               qtd_baus=qtd_bau,
                #               rect_element=element,
                #               screen=surface_game)
                            
        display.blit( surface_head, (0, 0) ) 
        pygame.draw.rect(surface_head, (255,255,0), rect=((0,0) , (1000,1000)))
        #pygame.draw.rect( surface_head, (255,255,0) )
        #display.blit( surface_game, (1, 1))
        display.blit( surface_point, (w_game , h_head) )
        
        
        
        # pygame.draw.rect( surface_game, (255, 255, 255), rect=( (0,0 ) , (100, 100 )) )
        # pygame.draw.rect( surface_game, (0, 255, 255), rect=( (100,0 ) , (100, 100 )) )

        # pygame.draw.rect( surface_game, (0, 0, 255), rect=( (200,0 ) , (100, 100 )) )

        # pygame.draw.rect( screen, (255, 255, 255), rect=( (screen_largura - screen_p_largura), 0, 
        #                                                  screen_p_largura, screen_p_altura) ) #react (posição) (dimensão)
        pygame.display.update()

    pygame.quit()
    

if __name__ == '__main__':
    main()

