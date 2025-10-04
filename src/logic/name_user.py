import os, pygame
from utils.json_manager import read_json, write_json
from utils.fonts import main as fonts
from utils.background import background_display_escolha_nomes
from logic.blit_elements import blit_name_player

def tela_nomes(display, campo_player1, campo_player2):
    path_json = os.getenv("PATH_JSON")
    
    campo_ativo = read_json(path_json)['campo_ativo_name'] 

    background_display_escolha_nomes(display)
    blit_name_player(display, campo_player1, campo_player2)

    name_player = read_json(path_json)['name_player']
    
    font = fonts(50)
    fonte = pygame.font.SysFont(None, 50)
    if campo_ativo == 1:
        # Calcula a largura usando o texto ATUAL do JSON
        largura_texto = font.size(name_player['play_01'])[0]
        
        # Coordenadas para desenhar a linha
        x_cursor = campo_player1.x + 12 + largura_texto
        y_inicio = campo_player1.y + 10
        y_fim = campo_player1.y + 50
        pygame.draw.line(display, (60, 60, 60), (x_cursor, y_inicio), (x_cursor, y_fim), 2)
        
    if campo_ativo == 2:
        # Calcula a largura usando o texto ATUAL do JSON
        largura_texto = font.size(name_player['play_02'])[0]
        
        # Coordenadas para desenhar a linha
        x_cursor = campo_player2.x + 12 + largura_texto
        y_inicio = campo_player2.y + 10
        y_fim = campo_player2.y + 50
        pygame.draw.line(display, (60, 60, 60), (x_cursor, y_inicio), (x_cursor, y_fim), 2)

def input_text_user(event):
    path_json = os.getenv("PATH_JSON")
    
    tela_atual = read_json(path_json)['tela_atual']
    campo_ativo = read_json(path_json)['campo_ativo_name']
    
    ## Verifica se o jogador dois apertou o Enter 
    if event.type == pygame.KEYDOWN and tela_atual == "tela_escolha_nome" and campo_ativo == 2:
        if event.key == pygame.K_RETURN:
            tela_atual = "jogo"
            write_json(path_json, 'tela_atual', tela_atual)

    
    if event.type == pygame.KEYDOWN and tela_atual == "tela_escolha_nome":
        
        ## Verifica se foi apertado ENTER
        if event.key == pygame.K_RETURN:
            campo_ativo = 2 if campo_ativo == 1 else 1
            write_json(path_json, 'campo_ativo_name', campo_ativo)
        
        ## Apagar a escrita se necessário
        campo_ativo = read_json(path_json)['campo_ativo_name']
        if event.key == pygame.K_BACKSPACE:
            name_player = read_json(path_json)['name_player']
            
            if campo_ativo == 1:
                name_player['play_01'] = name_player['play_01'][:-1]
            else:
                name_player['play_02'] = name_player['play_02'][:-1]
                
            write_json(path_json, 'name_player', name_player)
        
        ##  Aqui é aonde ocorre a escrita
        campo_ativo = read_json(path_json)['campo_ativo_name']
            ##unicode.isprintable() garante que o 'Enter' não seja convertido em texto
        if event.unicode.isprintable() and len(event.unicode) > 0:
            name_player = read_json(path_json)['name_player']
            
            if campo_ativo == 1 and len(name_player['play_01']) < 8:
                name_player['play_01'] += event.unicode
            if campo_ativo == 2 and len(name_player['play_02']) < 8:
                name_player['play_02'] += event.unicode
                
            write_json(path_json, 'name_player', name_player)