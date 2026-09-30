import numpy as np
from Rendering.RenderItem import RenderItem
class AirCraft:
    
    
    
    def __init__(self, position , velocity , theta , mass):
        
        #渲染的
        
        
        
        self.render_item = RenderItem(
            np.array([[40,5] ,[ -40, 5], [-40, -5], [40, -5], [50, 0] ], dtype = float),
            (255, 255, 255)
            )
        
        
        #位置信息
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.theta = theta #degree
        
        
        self.mass = mass
        
        self.pitch_rate = 5.0 #degree
        
        self.thrust = None
        
        self.wing = None
        
    def sync_with_wing(self):
        self.wing.position = self.position
        self.wing.theta = self.theta
        
    def get_render_item(self)->RenderItem:
        return self.render_item
    
    def handle_head_change(self, input_pitch:float):
        self.theta += input_pitch * self.pitch_rate
        
        
    

    