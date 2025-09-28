import pygame

def main (size_font:int = 20, type_font:str = 'default'):
    
    font_ = ''
    pygame.font.init()
    if type_font == 'default':
        font_ = pygame.font.SysFont('Jersey15-Regular', size_font)
    
    if type_font == 'point_negrito':
        font_ = pygame.font.SysFont('Jersey15-Regular', size_font, bold=True)
    
    if type_font == 'point_normal':
        font_ = pygame.font.SysFont('Jersey15-Regular', size_font)
    
    return font_
    
    