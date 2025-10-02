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

def blit_element(status:int , qtd_baus:int, rect_element, screen,  animation:list, frame_animation, font_set:str = fonts):
    
       
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
    
        img.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        img_w = img.get_width()
        img_h = img.get_height()
        img = pygame.transform.scale(img, (img_w/7, img_h/7))
        
        img_rect = img.get_rect()
        img_rect.center = element.center
        
        screen.blit(img, img_rect)
        
    
    if status == 0:    
        font_set = font_set(size_font=40, type_font='point_negrito')
        pallet_color_ = pallet_color()
        text_surface = font_set.render(str(qtd_baus), True, pallet_color_['cinza'])  # True = antialiasing
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