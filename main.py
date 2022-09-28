from material import Material
from ray import *

red = Material(diffuse=color(255,0,0))
white = Material(diffuse=color(255,255,255))

    
r = Raytracer(800,800)
r.light = Light(
    position = V3(0,0,0),
    intensity = 1
)
r.scene = [
    Sphere(V3(-3,0,-16), 2, red),
    Sphere(V3(-5,0,-10), 2, white)
]

r.dense = 1
r.point(100,100)
r.render()

r.write('r.bmp')