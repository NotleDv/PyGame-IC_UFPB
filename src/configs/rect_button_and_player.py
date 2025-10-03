import pygame

def rect_button():
    tamanho_botao = (250,60)
    tamanho_botaor = (150,50)
    
    bot_start = pygame.Rect(230,390, tamanho_botao[0], tamanho_botao[1])
    
    bot_retorno = pygame.Rect(100,610, tamanho_botaor[0], tamanho_botaor[1])
    
    bot_avançar = pygame.Rect(480,610,tamanho_botaor[0], tamanho_botaor[1])
    
    return bot_start, bot_retorno, bot_avançar

def rect_player():
    campo_player1 = pygame.Rect(137,338,430,60)
    campo_player2 = pygame.Rect(137,500,430,60)
    
    return campo_player1, campo_player2
    