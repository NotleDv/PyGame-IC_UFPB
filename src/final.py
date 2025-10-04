from ast import cmpop
from tkinter import font
import pygame
from pygame.locals import * 
from sys import exit
from json_manager import read_json

pygame.init()


tela = pygame.display.set_mode((700,700))
fonte = pygame.font.SysFont(None, 50)
pontuação = read_json("parametros_restart.json")["history_points"]
name_players = read_json("parametros_restart.json")["name_player"]



def tela_fim():
    tela_final = pygame.image.load("fundo.png")
    tela_final = pygame.transform.scale(tela_final, (700,700))
    tela.blit(tela_final,(0,0))
    icon_return = pygame.image.load("return.png")
    tela.blit(icon_return, (538,469))
    rect_return = pygame.Rect(538,469,41,37)
    
    #alterar o ícone do mouse e leve sombreamento ao passar com o cursor do mouse por cima do botão de retorno
    mouse_pos = pygame.mouse.get_pos()
    if rect_return.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        overlay = pygame.Surface(rect_return.size, pygame.SRCALPHA)
        overlay.fill((0,0,0,50))
        tela.blit(overlay, (538, 469))
    
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)                 
def tabela():
    #placar com pontuação e nomes dos jogadores, com a maior pontuação sendo sempre a primeira

    if pontuação["play_01"] >= pontuação["play_02"]:
        play_01 = fonte.render(name_players["player_01"], True, (0,0,0))
        play_02 = fonte.render(name_players["player_02"], True, (0,0,0))
        tela.blit(play_01,(175,265))
        tela.blit(play_02,(200,350))
        p1 = fonte.render(str(pontuação["play_01"]), True, (0,0,0))
        p2 = fonte.render(str(pontuação["play_02"]), True, (0,0,0))
        tela.blit(p1,(435,265))
        tela.blit(p2,(432,350))
    else:
        play_01 = fonte.render(name_players["player_01"], True, (0,0,0))
        play_02 = fonte.render(name_players["player_02"], True, (0,0,0))
        tela.blit(play_02,(175,265))
        tela.blit(play_01,(200,350))
        p1 = fonte.render(str(pontuação["play_01"]), True, (0,0,0))
        p2 = fonte.render(str(pontuação["play_02"]), True, (0,0,0))
        tela.blit(p2,(435,265))
        tela.blit(p1,(432,350))

    
    
    

while True:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    tela_fim()
    tabela()
    
   
   
    

        
    
    pygame.display.update()
        