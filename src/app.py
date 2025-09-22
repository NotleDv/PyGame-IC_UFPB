import pygame
import sys
import random

## x, y
## largura. altura
def main():
    pygame.init()

    ## Tela global
    w_display, h_display = 1000, 800
    
    ## Tela do Game
    w_game, h_game = (w_display - 200), h_display
    surface_game = pygame.Surface( (w_game, h_game) )
    
    ## Tela da Pontuação
    w_point, h_point = (w_display - w_game), h_display
    surface_point = pygame.Surface( (w_point, h_point) )
    surface_point.fill((255, 255, 255))
    
    display = pygame.display.set_mode( (w_display, h_display) )
    
    ## 
    def matriz_probabilidade(q_bau:int = 6, q_buraco:int = 3, dimesao:int = 4):
        import numpy as np
        
        lista = [0]*( (dimesao**2) - (q_bau + q_buraco) ) + [1]*q_bau + [-1]*q_buraco
        
        random.shuffle(lista)
        lista = np.array(lista)
        
        matriz_prob = lista.reshape(-1, 4)
        return matriz_prob
       
    def background(width:int, height:int, screen, dimensao:int = 4):
        ## Criando Baus, Buracos e espaços vazios
        matriz_prob = matriz_probabilidade()
        
        ## Matriz Crua
        matriz = []
        for i in range(dimensao):
            matriz.append([None]*dimensao)

        var_w = int(width/dimensao)
        var_h = int(height/dimensao)
                
        ## Preenchendo com as coordenadas
        posic_relativa = 0
        for index, i in enumerate(matriz):    
            
            for index_j, j in enumerate(i):        
                
                posicao_tupla = (var_w*(index_j), var_h*(index))
                elemento = pygame.Rect(posicao_tupla , (var_w, var_h ))
                
                matriz[index][index_j] = {'posicao': posicao_tupla, 
                                          'valor': matriz_prob[index][index_j].item(), 'posicao_relativa': posic_relativa, 
                                          'rect': elemento}
                
                ## Preenchendo com as cores
                rgb = ( random.randint(0,255) , random.randint(0,255) , random.randint(0,255))
                pygame.draw.rect( screen, rgb, elemento)
                
                posic_relativa+=1
        
        ## Preenchendo com as cores
        # for index, i in enumerate(matriz):    
        #     for index_j, j in enumerate(i):        
        #         rgb = ( random.randint(0,255) , random.randint(0,255) , random.randint(0,255))
        #         elemento = matriz[index][index_j]['rect']
        #         pygame.draw.rect( screen, rgb, elemento)
                
        
        return matriz
    
    
    def click (click_user:tuple, matriz):
        
        for index, i in enumerate(matriz):    
            for index_j, j in enumerate(i):   
                elemento = matriz[index][index_j]['rect'] 
                
                if elemento.collidepoint(click_user):
                    posicao = matriz[index][index_j]['posicao_relativa'] 
                    print(f"Clicou no elemento {posicao}")
        
        
        
        # import math
        
        # dists_relativas = []
        # dist_relativa = 0
        
        # for index, i in enumerate(matriz):    
    
        #     for index_j, j in enumerate(i):
        #         dist_relativa = math.dist(click_user, matriz[index][index_j]['posicao'])  
        #         dists_relativas.append({'dist': dist_relativa, 'posicao_relativa': matriz[index][index_j]['posicao_relativa']})
        
        
        # menor = dists_relativas[0]['dist']
        # chunck_click = 0
        # for i in dists_relativas:
        #     if menor > i['dist']:
        #         menor = i['dist']
        #         chunck_click = i['posicao_relativa']
                
        # print(chunck_click)
        
        
        
    matriz = background(w_game, h_game, surface_game)
    
    run = True
    while run:
        
        ## For de eventos
        for event in pygame.event.get():
            ## Fechamento
            if event.type == pygame.QUIT:
                run = False
                exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                click(click_user=pos, matriz=matriz)
                            
            
        display.blit( surface_game, (0, 0))
        display.blit( surface_point, (w_game , 0) )
        
        
        
        # pygame.draw.rect( surface_game, (255, 255, 255), rect=( (0,0 ) , (100, 100 )) )
        # pygame.draw.rect( surface_game, (0, 255, 255), rect=( (100,0 ) , (100, 100 )) )

        # pygame.draw.rect( surface_game, (0, 0, 255), rect=( (200,0 ) , (100, 100 )) )

        # pygame.draw.rect( screen, (255, 255, 255), rect=( (screen_largura - screen_p_largura), 0, 
        #                                                  screen_p_largura, screen_p_altura) ) #react (posição) (dimensão)
        pygame.display.update()

    pygame.quit()
    

main()

