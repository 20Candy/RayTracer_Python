from ray import *
    
r = Raytracer(800,800)
r.dense = 1
r.point(100,100)
r.render()

r.write('r.bmp')