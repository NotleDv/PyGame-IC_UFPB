from utils.fonts import main as fonts

def blit_element(status:int , qtd_baus:int, rect_element, screen, font_set):
        
        if status == 0:    
            text_surface = font_set.render(str(qtd_baus), True, (255,255,255))  # True = antialiasing
            text_rect = text_surface.get_rect(center=rect_element.center)
            screen.blit(text_surface, text_rect)
            
        if status == 1:    
            text_surface = font_set.render('Bau!!!', True, (255,255,255))  # True = antialiasing
            text_rect = text_surface.get_rect(center=rect_element.center)
            screen.blit(text_surface, text_rect)
    
        if status == -1:    
            text_surface = font_set.render('Buraco', True, (255,255,255))  # True = antialiasing
            text_rect = text_surface.get_rect(center=rect_element.center)
            screen.blit(text_surface, text_rect)
            
def main(status:int , qtd_baus:int, rect_element, screen, font_set:str = fonts):    

    blit_element(status= status , qtd_baus=qtd_baus, rect_element=rect_element, screen=screen, font_set=font_set(size_font=20))
