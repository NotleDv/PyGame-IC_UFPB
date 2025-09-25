def click (click_user:tuple, matriz, search_elements):
    
    condicion = False
    posicao = ''
    element_ = ''
    validacao = False
    
    for index, i in enumerate(matriz):    
        for index_j, j in enumerate(i):   
            elemento = matriz[index][index_j]['rect'] 
            
            if elemento.collidepoint(click_user):
                element_ = elemento
                condicion = True
                posicao = matriz[index][index_j]['posicao_relativa']
                break

    if condicion:
        qtd_bau, status = search_elements(posicao_relativa=posicao, matriz=matriz)
        
        validacao = True
        
        return qtd_bau, status, element_, validacao     
   
    else:
        return [None]*3       
            