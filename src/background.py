import pygame

def background(screen, matriz):
        
        for index, i in enumerate(matriz):    
            for index_j, element in enumerate(i):        
                
                rgb = ( random.randint(0,255) , random.randint(0,255) , random.randint(0,255))
                pygame.draw.rect( screen, rgb, element['rect'], border_radius=10)
                
            
    font_a = pygame.font.SysFont('arial', 30)
    
def main(screen, matriz):
    background(screen=screen,
               matriz=matriz)

    