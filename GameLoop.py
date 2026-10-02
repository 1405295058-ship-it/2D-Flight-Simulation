# Example file showing a basic pygame "game loop"
from aircraft.AirCraft import AirCraft
from Simulation.Atmosphere import Atmosphere
from Simulation.Physics import Physics 
from aircraft.Wing import Wing
from Rendering.Render import Render
from Simulation.InputManager import InputManager
import numpy as np
import pygame
from Scene.Scene import Scene
# pygame setup

pygame.init()
font = pygame.font.Font(None, 20)

#resolution

screen = pygame.display.set_mode((1280, 720))

#get clock

clock = pygame.time.Clock()


#start run

running = True

#大气层初始化

atmosphere = Atmosphere()

#翅膀初始化

wing = Wing(10, "NACA2412", [30.0, 0.0], 0)#surface area, 编号, 相对位置

#飞机初始化

plane = AirCraft(
    [10,100],#position
    [100,0],#velocity
    10,#theta
    10000#mass
    )

plane.wing = wing

plane.thrust = 2000.0 # N

plane.add_child(wing)

#输入管理器初始化

inputmanager = InputManager()

#物理初始化
physics = Physics()

#渲染器初始化

SCREEN_HEIGHT = 720
render = Render(screen, SCREEN_HEIGHT)


#场景初始化

scene = Scene()

scene.add_node2d(plane)
    

# func process
try:
    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
                
        #input
        
        inputmanager.update()
        
        plane.handle_head_change(inputmanager.input_pitch, dt)

        # physics
        
        physics.update(plane, atmosphere, dt)
        
        # render
        screen.fill((20, 20, 30))

        render.draw_scene(scene)

        pygame.display.flip()
        
except Exception as e:
    print("程序出错：", e)

finally:
    pygame.quit()
    print("game loop end")
   


