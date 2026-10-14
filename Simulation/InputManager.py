import pygame
class InputManager:
    def __init__(self):
        self.input_pitch = 0.0
        
    
    def update(self):
        
        keys = pygame.key.get_pressed()
        #print("正常运作")
        
        self.input_pitch = 0.0
        
        if keys[pygame.K_w]:
            self.input_pitch += 1.0
            #print("检测到按下")
            
        if keys[pygame.K_s]:
            self.input_pitch -= 1.0
            
    