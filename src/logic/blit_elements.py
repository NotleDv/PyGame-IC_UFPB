from utils.fonts import main as fonts
import pygame
from utils.pallet_color import pallet_color

def blit_play_atual (jogada, name_player, pallet_color, back_player_atual, surface_head):
        rect_play_atual = pygame.Rect((20, 10, 135, 50))
        
        font = fonts(30)
        player_atual = jogada['player_atual']
        print(player_atual)
        texto = font.render(str(name_player[player_atual]), True, pallet_color['cinza'])
        texto_rect = texto.get_rect(center=rect_play_atual.center)
        back_player_atual(surface_head)
        surface_head.blit(texto, texto_rect)

def blit_element(status:int , qtd_baus:int, rect_element, screen, font_set:str = fonts):
    encontrou_nada_sound = pygame.mixer.Sound('../assets/Sounds/encontrou_nada.wav')
    bau_sound = pygame.mixer.Sound('../assets/Sounds/bau.wav')
    buraco_sound = pygame.mixer.Sound('../assets/Sounds/buraco.wav')
    
    
    font_set = font_set(size_font=40, type_font='point_negrito')
    pallet_color_ = pallet_color()
    if status == 0:    
        text_surface = font_set.render(str(qtd_baus), True, pallet_color_['cinza'])  # True = antialiasing
        text_rect = text_surface.get_rect(center=rect_element.center)
        screen.blit(text_surface, text_rect)
        encontrou_nada_sound.set_volume(0.1)
        encontrou_nada_sound.play()
        
    if status == 1:              
        img = pygame.image.load(f'../assets/Bau.png')
        img.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        img_w = img.get_width()
        img_h = img.get_height()
        img = pygame.transform.scale(img, (img_w/2.7, img_h/2.7))
        
        img_rect = img.get_rect()
        img_rect.center = rect_element.center
        
        screen.blit(img, img_rect)
        bau_sound.set_volume(0.5)
        bau_sound.play()

    if status == -1:    
        img = pygame.image.load(f'../assets/buraco.png')
        img.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        img_w = img.get_width()
        img_h = img.get_height()
        img = pygame.transform.scale(img, (img_w/3, img_h/3))
        
        img_rect = img.get_rect()
        img_rect.center = rect_element.center
        
        screen.blit(img, img_rect)
        buraco_sound.set_volume(0.1)
        buraco_sound.play()
        
def atualizacao_points(surface, history_points, name_player, back_points,  pallet_color):
        rect_point = pygame.Rect((0, 0, 700, 100))
        back_points(surface, rect_point)
        
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
                    color= pallet_color['branco'],
                    type_font='point_normal') 
            
        rect_play_02 = pygame.Rect((0,0,140,40))
        rect_play_02.left = 483
        rect_play_02.top = 47 
        create_text(size_font= 30,
                    info_text=name_player['play_02'],
                    rect_center=rect_play_02,
                    surface=surface,
                    color=pallet_color['branco'],
                    type_font='point_normal')
        #pp
        rect_point_p1 = pygame.Rect((0,0,93,40))
        rect_point_p1.left = 247
        rect_point_p1.top = 47    
        create_text(size_font= 40,
                    info_text=history_points['play_01'],
                    rect_center=rect_point_p1,
                    surface=surface,
                    color=pallet_color['alaranjado'],
                    type_font='point_negrito')
        
        rect_point_p2 = pygame.Rect((0,0,93,40))
        rect_point_p2.left = 378
        rect_point_p2.top = 47 
        create_text(size_font= 40,
                    info_text=history_points['play_02'],
                    rect_center=rect_point_p2,
                    surface=surface,
                    color=pallet_color['alaranjado'],
                    type_font='point_negrito')