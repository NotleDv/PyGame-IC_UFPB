import pygame, random

def back_points(screen, rect_point):
    img_back = pygame.image.load('../assets/Back_Rodape.png')
    img_back_w = img_back.get_width()
    img_back_h = img_back.get_height()
    img_back = pygame.transform.scale(img_back, (img_back_w/1.5, img_back_h/1.5))
    img_back_rect = img_back.get_rect()
    img_back_rect.center = rect_point.center
    img_back_rect.top = 15
    screen.blit(img_back, img_back_rect)

def back_player_atual(screen):
    img_back = pygame.image.load('../assets/Back_player_atual.png')
    img_back_w = img_back.get_width()
    img_back_h = img_back.get_height()
    img_back = pygame.transform.scale(img_back, (img_back_w/1.4, img_back_h/1.4))
    #img_back_rect = img_back.get_rect()
    #img_back_rect.center = rect_base.center
    screen.blit(img_back, (0,0))

def back_progresso(screen, rect_base):
    img_back = pygame.image.load('../assets/Back_Progresso.png')
    img_back_w = img_back.get_width()
    img_back_h = img_back.get_height()
    img_back = pygame.transform.scale(img_back, (img_back_w/1.4, img_back_h/1.4))
    img_back_rect = img_back.get_rect()
    img_back_rect.center = rect_base.center
    screen.blit(img_back, img_back_rect)
    
def front_progresso(screen, rect_base):
    img_front = pygame.image.load('../assets/Front_Progresso.png')
    img_front_w = img_front.get_width()
    img_front_h = img_front.get_height()
    img_front = pygame.transform.scale(img_front, (img_front_w/1.4, img_front_h/1.4))
    img_front_rect = img_front.get_rect()
    img_front_rect.center = rect_base.center
    img_front_rect.top = -4
    screen.blit(img_front, img_front_rect)

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

    