import pygame, random
import numpy as np

def matriz_probabilidade(q_bau:int = 6, q_buraco:int = 3, dimesao:int = 4):
       
    lista = [0]*( (dimesao**2) - (q_bau + q_buraco) ) + [1]*q_bau + [-1]*q_buraco
    
    random.shuffle(lista)
    lista = np.array(lista)
    
    matriz_prob = lista.reshape(-1, 4)
    return matriz_prob
       
def matriz_kernel(width:int, height:int, dimensao:int = 4, size_elements:int = 1200):
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
            elemento_ = pygame.Rect(posicao_tupla , (100, 100 ))
            elemento_.center = elemento.center
            
            matriz[index][index_j] = {'posicao': posicao_tupla, 
                                        'valor': matriz_prob[index][index_j].item(),
                                        'posicao_relativa': posic_relativa,
                                        'posicao_ralativa_h_matriz': index_j, 'posicao_ralativa_v_matriz': index, 
                                        'rect': elemento_,
                                        'rect_2': elemento}
            
            
            posic_relativa+=1
    return matriz

def main(width:int, height:int, dimensao:int, size_elements):
    return matriz_kernel(width = width,
                         height = height,
                         dimensao = dimensao,
                         size_elements = size_elements)

