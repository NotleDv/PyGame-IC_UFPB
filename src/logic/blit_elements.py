from utils.fonts import main as fonts
import pygame
from utils.pallet_color import main as pallet_color_

def blit_element(status:int , qtd_baus:int, rect_element, screen, font_set):
    pallet_color = pallet_color_()
    if status == 0:    
        text_surface = font_set.render(str(qtd_baus), True, pallet_color['cinza'])  # True = antialiasing
        text_rect = text_surface.get_rect(center=rect_element.center)
        screen.blit(text_surface, text_rect)
        
    if status == 1:              
        img = pygame.image.load(f'../assets/Bau.png')
        img.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        img_w = img.get_width()
        img_h = img.get_height()
        img = pygame.transform.scale(img, (img_w/2.7, img_h/2.7))
        
        img_rect = img.get_rect()
        img_rect.center = rect_element.center
        
        screen.blit(img, img_rect)
        
        # text_surface = font_set.render('Bau!!!', True, (255,255,255))  # True = antialiasing
        # text_rect = text_surface.get_rect(center=rect_element.center)
        # screen.blit(text_surface, text_rect)

    if status == -1:    
        img = pygame.image.load(f'../assets/buraco.png')
        img.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        img_w = img.get_width()
        img_h = img.get_height()
        img = pygame.transform.scale(img, (img_w/3, img_h/3))
        
        img_rect = img.get_rect()
        img_rect.center = rect_element.center
        
        screen.blit(img, img_rect)
        

def main(status:int , qtd_baus:int, rect_element, screen, font_set:str = fonts):    
    
    
    blit_element(status= status , qtd_baus=qtd_baus, rect_element=rect_element, screen=screen, font_set=font_set(size_font=40, type_font='point_negrito'))
