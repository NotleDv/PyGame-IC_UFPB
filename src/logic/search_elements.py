def search_elements (posicao_relativa:int, matriz):
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