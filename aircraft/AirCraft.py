import numpy as np
from Rendering.RenderItem import RenderItem
from Rendering.RenderItem import RenderType
from Scene.Node2d import Node2d
class AirCraft(Node2d):
    
    
    
    def __init__(self, position , velocity , theta , mass):
        
        # 初始化 Node2d 的位置、角度、parent、children 等属性
        super().__init__(position, theta)
        
        
        
        #渲染的
    
        self.render_item = RenderItem(
            RenderType.POLYGON,
            shape = np.array([[40,5] ,[ -40, 5], [-40, -5], [40, -5], [50, 0] ], dtype = float),
            color = (255, 255, 255),
            )
        
        
        #位置信息
        self.velocity = np.array(velocity, dtype=float)
        
        
        self.mass = mass
        
        self.pitch_rate = 5.0 #degree
        
        self.thrust = None
        
        self.wing = None
        
    def get_render_item(self)->RenderItem:
        return self.render_item
    
    def handle_head_change(self, input_pitch:float, dt:float):
        self.theta += input_pitch * self.pitch_rate * dt
        
        
    

    