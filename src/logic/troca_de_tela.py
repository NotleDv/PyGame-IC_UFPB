from utils.json_manager import read_json, write_json
import os
from utils.background import background_display
from pygame import MOUSEBUTTONDOWN
import pygame


def troca_tela(event, button_start, bot_retorno, bot_avançar, campo_player1, campo_player2):
    path_json = os.getenv("PATH_JSON")

    if event.type == MOUSEBUTTONDOWN:
        tela_atual = read_json(path_json)['tela_atual']
        
        ## Alterar entre as telas
        if tela_atual == "menu":
            if button_start.collidepoint(event.pos):
                tela_atual = "tela_escolha_nome"
                write_json(path_json, 'tela_atual', tela_atual)
        
        if tela_atual == "tela_escolha_nome":
            if bot_retorno.collidepoint(event.pos):
                tela_atual = "menu"
                write_json(path_json, 'tela_atual', tela_atual)
                
            if campo_player1.collidepoint(event.pos):
                campo_ativo = 1
                write_json(path_json, 'campo_ativo_name', campo_ativo)
            
            elif campo_player2.collidepoint(event.pos):
                campo_ativo = 2
                write_json(path_json, 'campo_ativo_name', campo_ativo)
                
            if bot_avançar.collidepoint(event.pos):
                tela_atual = "jogo"
                write_json(path_json, 'tela_atual', tela_atual)