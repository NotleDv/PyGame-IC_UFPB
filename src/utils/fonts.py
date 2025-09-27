import pygame

def main (size_font:int, type_font:str = 'default'):
    font_ = ''
    pygame.font.init()
    if type_font == 'default':
        font_ = pygame.font.SysFont('arial', size_font)
    
    if type_font == 'point_negrito':
        font_ = pygame.font.SysFont('arial', size_font, bold=True)
    
    if type_font == 'point_normal':
        font_ = pygame.font.SysFont('arial', size_font)
    
    return font_
    
    