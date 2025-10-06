import pygame, random

def matriz_probabilidade():
    lista = [0]*(7) + [1]*6 + [-1]*3
    random.shuffle(lista)

    matriz = []
    count = 0
    for i in range(4):
        matriz.append([None]*4)
        
    for i in range(4):
        for k in range(4):
            matriz[i][k] = lista[count]
            count+=1

    return matriz
       
def matriz_kernel(width:int, height:int):
    ## Criando Baus, Buracos e espaços vazios
    matriz_prob = matriz_probabilidade()
    
    ## Matriz Crua
    matriz = []
    for i in range(4):
        matriz.append([None]*4)

    var_w = int(width/4)
    var_h = int(height/4)
    
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
                                        'valor': matriz_prob[index][index_j],
                                        'posicao_relativa': posic_relativa,
                                        'posicao_ralativa_h_matriz': index_j, 'posicao_ralativa_v_matriz': index, 
                                        'rect': elemento_}
            
            
            posic_relativa+=1
    return matriz

def main(width:int, height:int):
    return matriz_kernel(width = width,
                         height = height)

if __name__ == '__main__':
    main()