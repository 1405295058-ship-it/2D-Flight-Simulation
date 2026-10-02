# 2D Flight Simulation

## Overview
This is a real-time 2D flight simulation demo written in Python.

The project aims to simulate aircraft motion using aerodynamic data and a modular physics system.  
The current version uses XFoil-generated aerodynamic coefficients, with the possibility of incorporating CFD-generated data in the future.

Pygame is used for real-time rendering and input handling, while pytest is used for unit testing.

## Screenshot

![Runing screenshot](docs/image/running.png)

## Current Features
- Real-time physics simulation with state updates every frame.
- Simple aircraft pitch control using keyboard input.
- Standard atmosphere data lookup and interpolation.
- Aerodynamic coefficient interpolation based on airfoil data.
- Basic unit testing using pytest.

## Current Architecture
- `Node2d`: Stores basic transform information such as position and rotation, and handles parent-child coordinate transformations.
- `Scene`: Manages root `Node2d` objects in the scene.
- `RenderItem`: Stores rendering-related information such as shape, color, and render type.
- `AirCraft`: Inherits from `Node2d` and stores aircraft state such as velocity, mass, thrust, and attached components.
- `Wing`: Loads aerodynamic and geometry data and provides lift, drag, and moment coefficient lookup.
- `Render`: Traverses the scene hierarchy and renders `Node2d` objects.
- `Physics`: Calculates aerodynamic forces and updates aircraft motion.
- `InputManager`: Handles keyboard input.
- `GameLoop`: Coordinates input, physics updates, scene rendering, and the real-time simulation loop.


## Physical Model
###Dynamic pressure
```python
dynamic_pressure = 0.5 * rho * plane_speed**2 
```

###Lift 
```python
Lift = dynamic_pressure * surface_area * lift_coe
```
###Drag 
```python
Drag = dynamic_pressure * surface_area * drag_coe
```
###Net Force
```python
net_force = (drag_vector + lift_vector + gravity_vector + thrust_vector)
```
###Numerical Integration
```python
net_acceleration = net_force/plane.mass
plane_velocity += net_acceleration * dt
plane_position += plane_velocity * dt
```

###Additional details:
- Angle of attack is calculated from aircraft attitude and velocity direction.
- Aerodynamic coefficients are interpolated from airfoil data.
- The current simulation uses a 2D point-mass translational dynamics model.

## Data
- Atmosphere: https://www.engineerlaboratory.com/tables/air-density-vs-altitude
- Airfoil geometry: NASA airfoil coordinate data
- Aerodynamic coefficients: generated using XFoil
- Current airfoil NACA2412

## Controls
- W  : pitch up
- S  : pitch down
  
## Running the Project
###Activate the Conda environment:
- conda activate flight
###Run the simulation:
- python GameLoop.py
###Testing:
- pytest -v
