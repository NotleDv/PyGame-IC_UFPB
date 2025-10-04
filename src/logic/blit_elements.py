from utils.fonts import main as fonts
import pygame
from utils.pallet_color import pallet_color

from utils.json_manager import read_json
import os
from dotenv import load_dotenv

def blit_play_atual (back_player_atual, surface_head):
    rect_play_atual = pygame.Rect((20, 10, 135, 50))
    
    load_dotenv()
    path_json = os.getenv("PATH_JSON")
    jogada = read_json(path_json)['jogada']
    player_atual = jogada['player_atual']
    name_player = read_json(path_json)['name_player']
    
    
    font = fonts(30)
    pallet_color_ = pallet_color()
    #print(player_atual)
    texto = font.render(str(name_player[player_atual]), True, pallet_color_['cinza'])
    texto_rect = texto.get_rect(center=rect_play_atual.center)
    back_player_atual(surface_head)
    surface_head.blit(texto, texto_rect)

def blit_element(rect_element, screen, animation:list, frame_animation, font_set:str = fonts):
    load_dotenv()
    path_json = os.getenv("PATH_JSON")
    return_click = read_json(path_json)['return_click']   
    
    ## Funciont de renderização
    def render(lista_animation, screen, element, frame_animation):
        img = pygame.image.load('../assets/Background_game.png')
        img_w = img.get_width()
        img_h = img.get_height()
        img = pygame.transform.scale(img, (img_w/2.5, img_h/2.5))
        img_rect = img.get_rect()
        img_rect.center = element.center
        screen.blit(img, img_rect)


        img = pygame.image.load(lista_animation[frame_animation['frame_atual']]).convert_alpha()
    
        #img.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        img_w = img.get_width()
        img_h = img.get_height()
        img = pygame.transform.scale(img, (img_w/7, img_h/7))
        
        img_rect = img.get_rect()
        img_rect.center = element.center
        
        screen.blit(img, img_rect)
        
    status = return_click['status']
    if status == 0:    
        font_set = font_set(size_font=40, type_font='point_negrito')
        pallet_color_ = pallet_color()
        text_surface = font_set.render(str(return_click['qtd_bau']), True, pallet_color_['cinza'])  # True = antialiasing
        text_rect = text_surface.get_rect(center=rect_element.center)
        screen.blit(text_surface, text_rect)
        
    if status == 1:              
        render(lista_animation = animation, 
               screen = screen,
               element = rect_element,
               frame_animation = frame_animation)

    if status == -1:   
        render(lista_animation = animation, 
               screen = screen,
               element = rect_element,
               frame_animation = frame_animation)
        
def atualizacao_points(surface, background_points):
        load_dotenv()
        path_json = os.getenv("PATH_JSON")

        history_points = read_json(path_json)['history_points']
        name_player = read_json(path_json)['name_player']

        
        rect_point = pygame.Rect((0, 0, 700, 100))
        background_points(surface, rect_point)
        
        pallet_color_ = pallet_color()
        
        def create_text(size_font, info_text, rect_center, surface, color, type_font='default'):
            font = fonts(size_font, type_font)
            texto = font.render(str(info_text), True, color)
            texto_rect = texto.get_rect(center=rect_center.center)
            surface.blit(texto, texto_rect)
        
        #p
        rect_play_01 = pygame.Rect((0,0,140,40))
        rect_play_01.left = 95
        rect_play_01.top = 47    
        create_text(size_font= 30,
                    info_text=name_player['play_01'],
                    rect_center=rect_play_01,
                    surface=surface,
                    color= pallet_color_['branco'],
                    type_font='point_normal') 
            
        rect_play_02 = pygame.Rect((0,0,140,40))
        rect_play_02.left = 483
        rect_play_02.top = 47 
        create_text(size_font= 30,
                    info_text=name_player['play_02'],
                    rect_center=rect_play_02,
                    surface=surface,
                    color=pallet_color_['branco'],
                    type_font='point_normal')
        #pp
        rect_point_p1 = pygame.Rect((0,0,93,40))
        rect_point_p1.left = 247
        rect_point_p1.top = 47    
        create_text(size_font= 40,
                    info_text=history_points['play_01'],
                    rect_center=rect_point_p1,
                    surface=surface,
                    color=pallet_color_['alaranjado'],
                    type_font='point_normal')
        
        rect_point_p2 = pygame.Rect((0,0,93,40))
        rect_point_p2.left = 378
        rect_point_p2.top = 47 
        create_text(size_font= 40,
                    info_text=history_points['play_02'],
                    rect_center=rect_point_p2,
                    surface=surface,
                    color=pallet_color_['alaranjado'],
                    type_font='point_normal')
        
def blit_name_player(screen, rect_player_1, rect_player_2):
    load_dotenv()
    path_json = os.getenv("PATH_JSON")
    
    font = fonts(50)
    name_player = read_json(path_json)['name_player']
    
    texto_p1 = font.render(name_player['play_01'], True, (60, 60, 60))
    texto_p2 = font.render(name_player['play_02'], True, (60, 60, 60))
    
    screen.blit(texto_p1, (rect_player_1.x + 10, rect_player_1.y + 8))
    screen.blit(texto_p2, (rect_player_2.x + 10, rect_player_2.y + 8))
    
    img_button_retornar = pygame.image.load("../assets/botret.png")
    bot_retornar = pygame.transform.scale(img_button_retornar, (150, 50))
    
    img_button_avanca = pygame.image.load("../assets/bot_avançar.png")
    bot_avanca = pygame.transform.scale(img_button_avanca, (120, 90))
    
    screen.blit(bot_retornar,(100,610))
    screen.blit(bot_avanca, (480,595))