def click (click_user:tuple, matriz, search_elements):
    
    for index, i in enumerate(matriz):    
        for index_j, j in enumerate(i):   
            elemento = matriz[index][index_j]['rect'] 
            print(f'{elemento.collidepoint(click_user)}')
            
            if elemento == click_user:
                if elemento.collidepoint(click_user):
                    
                    posicao = matriz[index][index_j]['posicao_relativa'] 
                    qtd_bau, status = search_elements(posicao_relativa=posicao, matriz=matriz)
                    return qtd_bau, status, elemento
                    
            else:
                return [None]*3
            # else:
            #     return [None]*3