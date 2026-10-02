from Scene.Node2d import Node2d
class Scene:
    def __init__(self):
        
        self.roots = []
        
    def add_node2d(self, node2d:Node2d):
        if node2d.parent is not None:
            raise ValueError("只能把根节点直接加入 Scene")
        self.roots.append(node2d)
    
    
