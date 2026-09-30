import AirCraft
import Wing
import Physics
from Simulation.Atmosphere import Atmosphere
import Render
import numpy as np
render = Render.Render()
atmosphere = Atmosphere.Atmosphere()
physics = Physics.Physics()
wing = Wing.Wing(10)
plane = AirCraft.AirCraft(
   np.array([10,10] , dtype = float),
   np.array([100,0] , dtype = float),
   10,
   1000
    
    )

plane.wing = wing



render.draw_polygon_item(plane)

