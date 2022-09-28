import random
from lib import *
from sphere import *
from math import *

class Raytracer (object):
    def __init__ (self, width, height):
        self.width = width
        self.height = height
        self.background_color = color(0,0,0)
        self.current_color = color(255,255,255)
        self.scene = []
        self.clear()

    def clear(self):
        self.framebuffer = [
            [self.background_color for x in range(self.width)]
            for y in range(self.height)
        ]

    def point (self, x, y, color = None):
        if y >= 0 and y < self.height and x >= 0 and x < self.width:
            self.framebuffer[y][x] = color or self.current_color

    def write (self,filename):
        writebmp(filename, self.width, self.height, self.framebuffer)

    #rayo inifinitio
    def cast_ray(self, origin, direction):
        material = self.scene_intersect(origin, direction)

        if material:
            return material.diffuse
        else:
            return self.background_color

    def scene_intersect(self, origin, direction):
        zbuffer = 999999
        material = None
        
        for o in self.scene:
            intersect = o.ray_intersect(origin, direction)
            if intersect:
                if intersect.distance < zbuffer:
                    zbuffer = intersect.distance
                    material = o.material
        return material


    def render (self):
        fov = int(pi/2)  #apertura del angulo de la camara
        ar = self.width/self.height #aspect ratio
        tana = tan(fov/2) #tan del angulo de la camara

        for y in range(self.height):
            for x in range(self.width):
                r = random.uniform(0,1)
                if r < self.dense:
                    i = ((2 * (x + 0.5) / self.width) - 1) * ar * tana
                    j = (1 - 2 * (y + 0.5) / self.height) * tana
    
                    direction = V3(i, j, -1).norm()
                    origin = V3(0,0,0)
    
                    c = self.cast_ray(origin, direction)
    
                    self.point(x, y, c)
