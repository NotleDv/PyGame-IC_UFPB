import pygame

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