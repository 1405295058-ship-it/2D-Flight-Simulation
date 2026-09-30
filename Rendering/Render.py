import pygame
import numpy as np
class Render:
    def __init__(self , screen , screen_hight):
        self.screen  = screen
        self.screen_hight = screen_hight
    def fix_rotation(self, item)->np.array:
        rotated_points = []
        
        theta = item.theta
        theta_rad = np.deg2rad(theta)
        
        render_item = item.render_item
    
        rotation_matrix = np.array([
            [np.cos(theta_rad), -np.sin(theta_rad)],
            [np.sin(theta_rad),  np.cos(theta_rad)]
        ])
        
        for point in render_item.shape:
            
            rotated_point = rotation_matrix @ point
            
            rotated_points.append(rotated_point)
        
        return np.array(rotated_points)
        
    def fix_displacement_and_rotation(self, item)-> np.array:

        final_points = []
        
        position = item.position
        
        rotated_points = self.fix_rotation(item)
        
        for rotated_point in rotated_points:
            world_position = rotated_point + position
            
            screen_position = np.array([
            world_position[0],
            self.screen_hight - world_position[1]
                ])
            
            
            final_points.append(screen_position)
        
        return np.array(final_points)
    
    def fix_child_position(self, parent, child)->np.array:

        final_points = []
    
        render_item = child.render_item
    
        # child local rotation
        child_theta_rad = np.deg2rad(child.local_theta)
    
        child_rotation = np.array([
            [np.cos(child_theta_rad), -np.sin(child_theta_rad)],
            [np.sin(child_theta_rad),  np.cos(child_theta_rad)]
        ])
    
        # parent rotation
        parent_theta_rad = np.deg2rad(parent.theta)
    
        parent_rotation = np.array([
            [np.cos(parent_theta_rad), -np.sin(parent_theta_rad)],
            [np.sin(parent_theta_rad),  np.cos(parent_theta_rad)]
        ])
    
        for point in render_item.shape:
    
            # 1. child自身旋转
            local_point = child_rotation @ point
    
            # 2. child在parent坐标系中的位置
            parent_space_point = (
                local_point + child.local_position
            )
    
            # 3. 跟着parent整体旋转
            rotated_with_parent = (
                parent_rotation @ parent_space_point
            )
    
            # 4. 加parent世界位置
            world_position = (
                rotated_with_parent + parent.position
            )
    
            # 5. world -> screen
            screen_position = np.array([
                world_position[0],
                self.screen_hight - world_position[1]
            ])
    
            final_points.append(screen_position)

        return np.array(final_points)
    
    
    def draw_polygon_item(self , item):
        if not hasattr(item, "render_item"):
            return
        
        final_points = self.fix_displacement_and_rotation(item)
        
        color = item.render_item.color
        
        
        pygame.draw.polygon(self.screen, color, final_points)
        
    
    def draw_child_polygon_item(self, parent, child):
        if not hasattr(parent, "render_item"):
            return
        
        final_points = self.fix_child_position(parent, child)
        
        color = child.render_item.color
        
        pygame.draw.polygon(self.screen, color, final_points)
        
       
       
       
       
       
       
   