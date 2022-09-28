from material import Material
from ray import *

red = Material(diffuse=color(255,0,0))
white = Material(diffuse=color(255,255,255))

    
r = Raytracer(800,800)
<<<<<<< Updated upstream
=======
r.scene = [
    Sphere(V3(-3,0,-16), 2, red),
    Sphere(V3(-2.8,0,-10), 2, white)
]

r.dense = 0.3
>>>>>>> Stashed changes
r.point(100,100)
r.render()

r.write('r.bmp')