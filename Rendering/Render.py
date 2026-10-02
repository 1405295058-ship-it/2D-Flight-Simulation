import pygame
import numpy as np
from Scene.Node2d import Node2d
from Scene.Scene import Node2d
from Rendering.RenderItem import RenderType
class Render:
    def __init__(self , screen , screen_hight):
        self.screen  = screen
        self.screen_hight = screen_hight
    def draw_scene(self, scene):
        for root in scene.roots:
            self.draw_node2d(root)
        
    def draw_node2d(self, node2d:Node2d):   
        if node2d.render_item == None:
            return
        
        render_item = node2d.render_item
        
        world_transform = node2d.get_world_transform()
        
        if render_item.render_type == RenderType.POLYGON:
            color = render_item.color
            
            shape = render_item.shape
            
            local_points = np.column_stack([
            shape,
            np.ones(len(shape)),
            ])
            
            world_points = (world_transform @ local_points.T).T[:, :2]
            
            screen_points = world_points.copy()
            screen_points[:, 1] = self.screen_hight - screen_points[:, 1]
            
            pygame.draw.polygon(
            self.screen,
            color,
            np.rint(screen_points).astype(int)
        )
    
        if len(node2d.children) == 0:
            return
        
        for child in node2d.children:
            self.draw_node2d(child)
            
    
    def draw_polygon_item(self , item):
        if not hasattr(item, "render_item"):
            return
        
        final_points = self.fix_displacement_and_rotation(item)
        
        color = item.render_item.color
        
        
        pygame.draw.polygon(self.screen, color, final_points)
        
    
   
       
       
       
       
       
       
   