import pygame, os
from utils.json_manager import read_json, write_json
from logic.blit_elements import blit_element

def load_animation_bau():
    list_paths = []
    for i in range(30):
        if i < 10: path = f'../assets/bau/bau_0000{i}.png'
        else: path = f'../assets/bau/bau_000{i}.png'
        
        #img = pygame.image.load(path)
        img = path
        list_paths.append(img)
    return list_paths

def load_animation_buraco():
    list_paths = []
    for i in range(30):
        if i < 10: path = f'../assets/buraco/buraco_0000{i}.png'
        else: path = f'../assets/buraco/buraco_000{i}.png'
        
        #img = pygame.image.load(path)
        img = path
        list_paths.append(img)
    return list_paths

def animation(run, blit_elements_click):
    path_json = os.getenv("PATH_JSON")
    
    frame_animation = read_json(path_json)['frame_animation']
    
    
    if blit_elements_click['validacao'] and run:
        
        blit_element( rect_element=blit_elements_click['rect_element'],
                    screen=blit_elements_click['screen'],
                    animation =blit_elements_click['animation'],
                    frame_animation = frame_animation )
        
        if frame_animation['concluido'] == False:
            frame_animation['frame_atual'] += 1
            write_json(path_json, 'frame_animation', frame_animation)
        
        lista_animation = blit_elements_click['animation']
        if frame_animation['frame_atual'] >= len(lista_animation) -1:
            frame_animation['frame_atual'] = len(lista_animation) -1
            frame_animation['frame_atual'] = 0
            write_json(path_json, 'frame_animation', frame_animation)
            
            blit_elements_click['validacao'] = False