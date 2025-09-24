import pygame

def main (size_font:int, type_font:str = 'default'):
    font_ = ''
    
    if type_font == 'default':
        font_ = pygame.font.SysFont('arial', size_font)
    
    return font_
    
    