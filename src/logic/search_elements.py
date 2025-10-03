def search_elements (posicao_relativa:int, matriz):
    status = 0
    qtd_bau = 0
        
    posicao_h = 0
    posicao_v = 0
    for i in matriz:
        for j in i:
            if j['posicao_relativa'] == posicao_relativa: ## Pega o item na matriz com a mesma posição relativa
                posicao_h = j['posicao_ralativa_h_matriz'] ## Pega a posição horizontal, 1 a 4
                posicao_v = j['posicao_ralativa_v_matriz'] ## Pega a posição vertical, 1 a 4
                
                status = j['valor'] ## Pega o valor do rect
                break

    if status != 1 or status != -1:
        #print('posição n: ',posicao_h, posicao_v)     
        qtd_bau += search_matriz(posicao_h+1, posicao_v, matriz) # O elemento a direita
        qtd_bau += search_matriz(posicao_h-1, posicao_v, matriz) # O elemento a esquerda
        qtd_bau += search_matriz(posicao_h, posicao_v-1, matriz) # O elemento em baixo
        qtd_bau += search_matriz(posicao_h, posicao_v+1, matriz) # O elemento em cima
    
    return qtd_bau, status


def search_matriz(p_horizontal:int, p_vertical:int, matriz) -> int: 
        
        ## Isso é importante para não travar o código se a pessoa clicar nos elementos presentes em H0, H3, além das bordas
        h_min = matriz[0][0]['posicao_ralativa_h_matriz']
        h_max = matriz[0][-1]['posicao_ralativa_h_matriz']
        v_min = matriz[0][0]['posicao_ralativa_v_matriz']
        v_max = matriz[-1][-1]['posicao_ralativa_v_matriz']
        
        result = 0
        ## Verifico se essa posição que eu fiz na chamada da função, está nos limites da matriz
        if (p_horizontal >= h_min and p_vertical >= v_min):
            if (p_horizontal <= h_max and p_vertical <= v_max):
                ## Por fim, é verificado se o valor 1 está presente, ai é bau
                if matriz[p_vertical][p_horizontal]['valor'] == 1:
                    result = 1

        return result