from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent

ATM_DIR = BASE_DIR / "data" / "atmosphere.txt"

class Atmosphere:
    
    def __init__(self):
        self.altitude = []
        self.temperature = []
        self.pressure = []
        self.density = []
        self.density_ratio = []

        with open(ATM_DIR, "r") as file:

            lines = file.readlines()

            for line in lines[2:]:
                values = line.split("\t")

                self.altitude.append(float(values[0]))
                self.temperature.append(float(values[2]))
                self.pressure.append(float(values[3]))
                self.density.append(float(values[4]))
                self.density_ratio.append(float(values[5]))
    
    
    
    
    def get_temperature(self, hight:float)->float:
        return np.interp(hight/1000, self.altitude, self.temperature)
    
    def get_pressure(self, hight:float)->float:
        return np.interp(hight/1000, self.altitude, self.pressure)
    
    def get_density(self, hight:float)->float:
        return np.interp(hight/1000, self.altitude, self.density)
    
    def get_density_ratio(self, hight:float)->float:
        return np.interp(hight/1000, self.altitude, self.density_ratio)
    
    
        
        
        