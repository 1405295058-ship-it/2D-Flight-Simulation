import numpy as np
class Node2d:
    
    #有parent时自动切位local_position
    def __init__(self, position:list, theta:float):
        
        self.parent = None
        self.children = []
        
        self.position = np.array(position, dtype = float)
        self.theta = theta
        
        
        self.render_item = None
    
    def add_child(self, child:"Node2d"):
        self.children.append(child)
        child.parent = self
        print("加入child", child)

    #返回此node的转换矩阵       
    def get_world_transform(self)-> np.array:
        theta = np.deg2rad(self.theta)
        c, s = np.cos(theta), np.sin(theta)
        x, y = self.position

        local_transform = np.array([
            [c, -s, x],
            [s,  c, y],
            [0,  0, 1],
        ])

        if self.parent is None:
            return local_transform

        return self.parent.get_world_transform() @ local_transform    
    
        