from ast import cmpop
from tkinter import font
import pygame
from pygame.locals import * 
from sys import exit

pygame.init()
pygame.key.set_repeat(300, 30)

largura = 700
altura = 700

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Caça ao Tesouro!')
tela_ini = pygame.image.load("../ryan/telaini.png")
tela_ini = pygame.transform.scale(tela_ini, (largura, altura))

cor_normal = (100,100,200)
cor_hover = (127,0,128)
tamanho_botao = (250,60)
tamanho_botaor = (150,50)
telaini = pygame.image.load("../ryan/img1.png")
bot_start = pygame.Rect(230,390, tamanho_botao[0], tamanho_botao[1])
caixa = pygame.Rect(230,390, tamanho_botao[0], tamanho_botao[1])
bot_retorno = pygame.Rect(100,610, tamanho_botaor[0], tamanho_botaor[1])
tela_players = pygame.image.load("../ryan/tplayers.png")
tela_players = pygame.transform.scale(tela_players, (largura, altura))
bot_ret = pygame.image.load("../ryan/botret.png")
bot_r = pygame.transform.scale(bot_ret, (tamanho_botaor[0], tamanho_botaor[1]))
bot_avançar = pygame.image.load("../ryan/bot_avançar.png")
bot_a = pygame.transform.scale(bot_avançar, (120, 90))
bot_avançar = pygame.Rect(480,610,tamanho_botaor[0], tamanho_botaor[1])
tela_atual = "menu"

campo_player1 = pygame.Rect(137,338,430,60)
campo_player2 = pygame.Rect(137,500,430,60)
campo_ativo = 1

player1 = ""
player2 = ""
fonte = pygame.font.SysFont(None, 50)

cursor_visivel = True
ultimo_tempo_alternancia = pygame.time.get_ticks()
tempo_alternancia = 500 



while True:
    ## Animação da barra de escrita
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ultimo_tempo_alternancia >= tempo_alternancia:
        cursor_visivel = not cursor_visivel
        ultimo_tempo_alternancia = tempo_atual
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == MOUSEBUTTONDOWN:
            
            ## Alterar entre as telas
            if tela_atual == "menu":
                if bot_start.collidepoint(event.pos):
                    tela_atual = "tela_escolha"
            
            elif tela_atual == "tela_escolha":
                if bot_retorno.collidepoint(event.pos):
                    tela_atual = "menu"
                if campo_player1.collidepoint(event.pos):
                    campo_ativo = 1
                elif campo_player2.collidepoint(event.pos):
                    campo_ativo = 2
                if bot_avançar.collidepoint(event.pos):
                    tela_atual = "jogo"
                    
        
            ## Verifica se o jogador dois apertou o Enter 
            if event.type == pygame.KEYDOWN and tela_atual == "tela_escolha" and campo_ativo == 2:
                if event.key == pygame.K_RETURN:
                        tela_atual = "jogo"

            
            if event.type == pygame.KEYDOWN and tela_atual == "tela_escolha":
                ## Verifica se foi apertado ENTER
                if event.key == pygame.K_RETURN:
                    campo_ativo = 2 if campo_ativo == 1 else 1
                
                ## Apagar a escrita se necessário
                if event.key == pygame.K_BACKSPACE:
                    if campo_ativo == 1:
                        player1 = player1[:-1]
                    else:
                        player2 = player2[:-1]
                
                ## 
                if event.unicode.isprintable() and len(event.unicode) > 0:
                    if campo_ativo == 1:
                        player1 += event.unicode
                    else:
                        player2 += event.unicode
    if tela_atual == "menu":
        tela.blit(tela_ini, (0,0))
        #pygame.draw.rect(tela, (128,0,127),(230,390,tamanho_botao[0],tamanho_botao[1]))  #hitbox do botão de iniciar
    elif tela_atual == "tela_escolha":
        tela.fill((0,0,100))
        tela.blit(tela_players, (0,0))
        texto_p1 = fonte.render(player1, True, (60, 60, 60))
        texto_p2 = fonte.render(player2, True, (60, 60, 60))
        tela.blit(texto_p1, (campo_player1.x + 10, campo_player1.y + 8))
        tela.blit(texto_p2, (campo_player2.x + 10, campo_player2.y + 8))
        tela.blit(bot_r,(100,610))
        tela.blit(bot_a, (480,595))
       
        if campo_ativo == 1 and cursor_visivel:
            largura_textop1 = fonte.size(player1)[0]
            x_cursor = campo_player1.x + 10 + largura_textop1
            y_inicio = campo_player1.y + 10
            y_fim = campo_player1.y + campo_player1.height - 10
            pygame.draw.line(tela, (60, 60, 60), (x_cursor, y_inicio), (x_cursor, y_fim), 2)
        if campo_ativo == 2  and cursor_visivel:
            largura_textop2 = fonte.size(player2)[0]
            x_cursor = campo_player2.x + 10 + largura_textop2
            y_inicio = campo_player2.y + 10
            y_fim = campo_player2.y + campo_player2.height - 10
            pygame.draw.line(tela, (60, 60, 60), (x_cursor, y_inicio), (x_cursor, y_fim), 2)

        
    elif tela_atual == "jogo":
        tela.blit(telaini, (0,0))  

    pygame.display.update()
    