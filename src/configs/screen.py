import pygame

def main(w_display:int = 800, h_display:int = 800):

    ## Tela do Game
    w_game, h_game = (w_display - 200), h_display
    surface_game = pygame.Surface( (w_game, h_game) )
    
    ## Tela da Pontuação
    w_point, h_point = (w_display - w_game), h_display
    surface_point = pygame.Surface( (w_point, h_point) )
    surface_point.fill((255, 255, 255))
    
    display = pygame.display.set_mode( (w_display, h_display) )
    
    return [[display, surface_game, surface_point],
            [w_game, h_game, w_point, h_point]]