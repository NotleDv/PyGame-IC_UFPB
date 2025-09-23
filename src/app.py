import pygame
import sys
import random

## x, y
## largura. altura
def main():
    pygame.init()
    pygame.font.init()
    ## Tela global
    w_display, h_display = 600, 600
    
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
       
    def matriz_kernel(width:int, height:int, dimensao:int = 4):
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
                
                ##
                elemento = pygame.Rect(posicao_tupla , (var_w, var_h ))
                
                ##
                elemento_ = pygame.Rect(posicao_tupla , (var_w/1.5, var_h/1.5 ))
                elemento_.center = elemento.center
                
                matriz[index][index_j] = {'posicao': posicao_tupla, 
                                          'valor': matriz_prob[index][index_j].item(),
                                          'posicao_relativa': posic_relativa,
                                          'posicao_ralativa_h_matriz': index_j, 'posicao_ralativa_v_matriz': index, 
                                          'rect': elemento_ }
                
                
                posic_relativa+=1
        return matriz
    
    def background(screen, matriz):
        
        for index, i in enumerate(matriz):    
            for index_j, element in enumerate(i):        
                
                rgb = ( random.randint(0,255) , random.randint(0,255) , random.randint(0,255))
                pygame.draw.rect( screen, rgb, element['rect'], border_radius=10)
                
            
    font_a = pygame.font.SysFont('arial', 30)
    
    def blit_element(status:int , qtd_baus:int, rect_element, screen):
        
        if status == 0:    
            text_surface = font_a.render(str(qtd_baus), True, (255,255,255))  # True = antialiasing
            text_rect = text_surface.get_rect(center=rect_element.center)
            screen.blit(text_surface, text_rect)
            
        if status == 1:    
            text_surface = font_a.render('Bau!!!', True, (255,255,255))  # True = antialiasing
            text_rect = text_surface.get_rect(center=rect_element.center)
            screen.blit(text_surface, text_rect)
    
        if status == -1:    
            text_surface = font_a.render('Buraco', True, (255,255,255))  # True = antialiasing
            text_rect = text_surface.get_rect(center=rect_element.center)
            screen.blit(text_surface, text_rect)
            
            
    def search_elements (element, posicao_relativa:int, matriz) -> tuple[int, int]:
        status = 0
        qtd_trofeu = 0
        
        def search_matriz(p_horizontal:int, p_vertical:int, matriz=matriz) -> int: 
            h_min = matriz[0][0]['posicao_ralativa_h_matriz']
            h_max = matriz[0][-1]['posicao_ralativa_h_matriz']
            v_min = matriz[0][0]['posicao_ralativa_v_matriz']
            v_max = matriz[-1][-1]['posicao_ralativa_v_matriz']
            
            result = 0
            if (p_horizontal >= h_min and p_vertical >= v_min):
                if (p_horizontal <= h_max and p_vertical <= v_max):
                    if matriz[p_vertical][p_horizontal]['valor'] == 1:
                        result = 1

            return result
            
        posicao_h = 0
        posicao_v = 0
        for i in matriz:
            for j in i:
                if j['posicao_relativa'] == posicao_relativa:
                    posicao_h = j['posicao_ralativa_h_matriz']
                    posicao_v = j['posicao_ralativa_v_matriz']
                    
                    status = j['valor']
                    break
        
        if status != 1 or status != -1:
            #print('posição n: ',posicao_h, posicao_v)     
            qtd_trofeu += search_matriz(posicao_h+1, posicao_v)
            qtd_trofeu += search_matriz(posicao_h-1, posicao_v)
            qtd_trofeu += search_matriz(posicao_h, posicao_v-1)
            qtd_trofeu += search_matriz(posicao_h, posicao_v+1)
        
        return qtd_trofeu, status

    
    def click (click_user:tuple, matriz):
        
        for index, i in enumerate(matriz):    
            for index_j, j in enumerate(i):   
                elemento = matriz[index][index_j]['rect'] 
                
                if elemento.collidepoint(click_user):
                    posicao = matriz[index][index_j]['posicao_relativa'] 
                    qtd_bau, status = search_elements(element=elemento, posicao_relativa=posicao, matriz=matriz)
                    return qtd_bau, status, elemento
                    
        
        
    matriz_k = matriz_kernel(width = w_game, height = h_game)
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
                qtd_bau, status, element = click(click_user=posicao_click, matriz=matriz_k)
                blit_element(status=status , qtd_baus=qtd_bau, rect_element=element, screen=surface_game)
                            
            
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

