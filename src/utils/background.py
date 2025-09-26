import pygame, random

def background_display(screen):
    img = pygame.image.load('../assets/background.png')
    img_w = img.get_width()
    img_h = img.get_height()
    img = pygame.transform.scale(img, (img_w/1.4, img_h/1.4))
    screen.blit(img, (0, 0))
    
def background_surface_game(screen, matriz):
        
    for index, i in enumerate(matriz):    
        for index_j, element in enumerate(i): 
            #screen_rect = screen.get_rect()
            rgb = ( random.randint(0,255) , random.randint(0,255) , random.randint(0,255))
            
            img = pygame.image.load('../assets/Background_game.png')
            img_w = img.get_width()
            img_h = img.get_height()
            img = pygame.transform.scale(img, (img_w/3, img_h/3))
            img_rect = img.get_rect()
            
            element_ = element['rect']
            img_rect.center = element_.center
            screen.blit(img, img_rect)
            # mascara_img = pygame.Surface(element['rect']).convert()
            #pygame.draw.rect( screen, rgb, element['rect'], border_radius=10)
            #pygame.draw.rect( screen, (255,255,255), element['rect_2'], border_radius=10)
            # circle = pygame.Surface([500,300]).convert()
            # circle.fill((255,0,255)) #make abnormal bg color
            # circle.set_colorkey((255,0,255)) #hide bg
            # pygame.draw.circle(circle, (200,200,0), screen_rect.center, 25, 0)
            # circle_rect = circle.get_rect()
                
            
def main(screen, matriz):
    background_game(screen=screen,
                    matriz=matriz)

    