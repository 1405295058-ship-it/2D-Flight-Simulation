from pathlib import Path
import numpy as np
from Rendering.RenderItem import RenderItem

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

class Wing:
    
    def __init__(self , surface_area: float, airfoil_type: str ,local_position):
        
        self.shape  = []
        self.AoA = []
        self.lift_coe = []
        self.drag_coe = []
        self.moment_coe = []
        
        #位置信息
        self.local_position = local_position
        self.local_theta = 0.0
        self.surface_area = surface_area
        
        self.airfoil_type = airfoil_type
        
        shape_path = DATA_DIR / airfoil_type / "WingShape.txt"
        aero_data_path = DATA_DIR / airfoil_type / "AERODynamicData.txt"
        
        
        with open(shape_path , "r") as file:#将形状数据搞到shape里面去
            lines = file.readlines()
            for line in lines[1:]:
                values = line.split()
                if len(values) == 2:
                    self.shape.append(np.array([float(values[0]) * -60,float(values[1]) * 60]))
                    
        
        
        with open(aero_data_path , "r") as file:
            lines = file.readlines()
            
            for line in lines[12:]:
                values = line.split()
                
                self.AoA.append(float(values[0]))
                self.lift_coe.append(float(values[1]))
                self.drag_coe.append(float(values[2]))
                self.moment_coe.append(float(values[4]))
        
        self.render_item = RenderItem(
            self.shape, 
            (173, 216, 230)
            )
        
            
    def get_lift_coe(self , angle:float)->float:
        return np.interp(angle, self.AoA, self.lift_coe)
        
    def get_drag_coe(self , angle:float)->float:
        return np.interp(angle, self.AoA, self.drag_coe)
    
    def get_moment_coe(self , angle:float)->float:
        return np.interp(angle, self.AoA, self.moment_coe)
    
    def get_render_item(self)->RenderItem:
        return self.render_item
        
                