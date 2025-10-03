import pygame

def config_screens(w_display:int = 800, h_display:int = 800):

    head_height = 55
    ## Cabeçalho
    w_head, h_head = (w_display), head_height
    surface_head = pygame.Surface( (w_head, h_head) ,pygame.SRCALPHA)
    
    ## Tela do Game
    w_game, h_game = (w_display - 200), h_display - (head_height+100)
    surface_game = pygame.Surface( (w_game, h_game) ,pygame.SRCALPHA )
    
    ## Tela da Pontuação
    w_point, h_point = w_display, 100
    surface_point = pygame.Surface( (w_point, h_point) ,pygame.SRCALPHA )
    
    display = pygame.display.set_mode( (w_display, h_display) )
    
    return [[display, surface_game, surface_point, surface_head],
            [w_game, h_game]]