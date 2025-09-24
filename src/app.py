import pygame
import sys
import random
from rich.traceback import install
install()
## x, y
## largura. altura
def main():
    pygame.init()
    pygame.font.init()
    
    w_display, h_display = 1000, 800
    
    ##
    from configs.screen import main as screens
    config_screen = screens(w_display=w_display,
                            h_display=h_display)
    
    w_game, h_game, w_point, h_point = config_screen[1]
    
    display, surface_game, surface_point = config_screen[0]
    
    
    
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
    while run:
        
        ## For de eventos
        for event in pygame.event.get():
            ## Fechamento
            if event.type == pygame.QUIT:
                run = False
                exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posicao_click = event.pos
                print(posicao_click)
                qtd_bau, status, element = click(click_user=posicao_click,
                                                 matriz=matriz_k,
                                                 search_elements=search_elements)
                blit_elements(status=status, 
                              qtd_baus=qtd_bau,
                              rect_element=element,
                              screen=surface_game)
                            
            
        display.blit( surface_game, (0, 0))
        display.blit( surface_point, (w_game , 0) )
        
        
        
        # pygame.draw.rect( surface_game, (255, 255, 255), rect=( (0,0 ) , (100, 100 )) )
        # pygame.draw.rect( surface_game, (0, 255, 255), rect=( (100,0 ) , (100, 100 )) )

        # pygame.draw.rect( surface_game, (0, 0, 255), rect=( (200,0 ) , (100, 100 )) )

        # pygame.draw.rect( screen, (255, 255, 255), rect=( (screen_largura - screen_p_largura), 0, 
        #                                                  screen_p_largura, screen_p_altura) ) #react (posição) (dimensão)
        pygame.display.update()

    pygame.quit()
    

if __name__ == '__main__':
    main()

