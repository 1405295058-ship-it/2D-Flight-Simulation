from aircraft.AirCraft import AirCraft
from Simulation.Atmosphere import Atmosphere
import numpy as np 
class Physics:
    def update(self , plane:AirCraft , atmosphere:Atmosphere , dt):
        
        g = 9.81
        
        # 得到大气数据
        rho = atmosphere.get_density(plane.position[1] / 1000)
        
        #飞机的基础数据
        plane_position = plane.position
        plane_velocity = plane.velocity
        plane_speed = np.sqrt(plane_velocity[0]**2 + plane_velocity[1]**2)
        if plane_speed < 1e-6:
            return
        
        #计算AoA
        #风速水平夹角
        gamma = np.arctan2(plane_velocity[1] , plane_velocity[0])
        gamma_deg = np.rad2deg(gamma)
        
        #飞机水平仰角
        theta_deg = plane.theta
        theta = np.deg2rad(theta_deg)
        
        AoA_deg_pre = theta_deg - gamma_deg
        AoA_deg = (180 + AoA_deg_pre) % 360 - 180
        AoA = np.deg2rad(AoA_deg)
        
        
        #找coe
        if plane.wing.AoA[0] <= AoA_deg <= plane.wing.AoA[-1]:
            lift_coe = plane.wing.get_lift_coe(AoA_deg)
            drag_coe = plane.wing.get_drag_coe(AoA_deg)
            moment_coe = plane.wing.get_moment_coe(AoA_deg)
        else:
            return
        
        
        dynamic_pressure = 0.5 * rho * plane_speed**2 
        Lift = dynamic_pressure * plane.wing.surface_area * lift_coe
        Drag = dynamic_pressure * plane.wing.surface_area * drag_coe
        
        
        #运动状态更新
        drag_vector = np.array([
            -Drag * np.cos(gamma),
            -Drag * np.sin(gamma)
        ])
        
        lift_vector = np.array([
            -Lift * np.sin(gamma),
            Lift * np.cos(gamma)
            ])
        
        gravity_vector = np.array([
            0,
            - g * plane.mass
            ])
        
        thrust_vector = np.array([
            plane.thrust * np.cos(theta),
            plane.thrust * np.sin(theta)
            ])
        
        net_force = (drag_vector + lift_vector + gravity_vector + thrust_vector)
        
        net_acceleration = net_force/plane.mass
        
        plane_velocity += net_acceleration * dt
        plane_position += plane_velocity * dt
        plane.sync_with_wing()
        
    
        
        
        
        
        
        