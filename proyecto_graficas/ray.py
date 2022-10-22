from importlib.util import spec_from_file_location
import random
from lib import *
from sphere import *
from material import *
from light import *
from color import *
from math import *

MAX_RECURSION_DEPTH = 3

class Raytracer(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_color = color(0,0,100)
        self.current_color = color(0,0,0)
        self.scene = []
        self.light = Light(V3(0,0,0), 1, color(255,255,255))
        self.envmap = None

        self.density = 1
        self.clear()

    def clear(self):
        self.framebuffer = [
            [ self.background_color for y in range(self.height)]
            for x in range(self.width) 
        ]

    def point(self, x, y, c = None):
        if y >= 0 and y < self.height and x >= 0 and x < self.width:
            self.framebuffer[x][y] = c or self.current_color

    def write(self, filename='out.bmp'):
        writebmp(filename, self.width, self.height, self.framebuffer)

    def render(self):
        fov = int(pi/2)
        ar = self.width/self.height
        tana = tan(fov/2)
        
        for y in range(self.height):
            for x in range(self.width):

                rand = random.uniform(0, 1)
                if rand < self.density:
                    i = (2 * (x + 0.5) / self.width - 1) * ar * tana
                    j = (1 - (2 * (y + 0.5) / self.height)) * tana

                    origin = V3(0,0,0)
                    direction = norm(V3(i, j, -1))

                    c = self.cast_ray(origin, direction)
                    self.point(x,y,c)

    def get_background(self, direction):
        if self.envmap:
            return self.envmap.get_color(direction)
        else:
            return self.background_color

    def cast_ray(self, origin, direction, recursion = 0):
        if recursion > MAX_RECURSION_DEPTH:
            return self.get_background(direction)

        material, intersect = self.scene_intersect(origin, direction)

        if material is None:
            return self.get_background(direction)
        
        l_dir = norm(sub(self.light.position, intersect.point))
        diffuse_intensity = dot( l_dir, intersect.normal)

        if material.albedo[2] > 0:

            reflect_dir = reflect(direction, intersect.normal)
            reflect_bias = -0.5 if dot(reflect_dir, intersect.normal) < 0 else 0.5
            reflect_origin = intersect.point + (intersect.normal * reflect_bias) 
            reflect_color = self.cast_ray(reflect_origin, reflect_dir, recursion + 1)
        else:
            reflect_color = color(0, 0, 0)
        
        
        if material.albedo[3] > 0:
            refract_dir = refract(direction, intersect.normal, material.refractive_index)
            refract_bias = -0.5 if dot(refract_dir, intersect.normal) < 0 else 0.5
            refract_origin = intersect.point + (intersect.normal * refract_bias)
            refract_color = self.cast_ray(refract_origin, refract_dir, recursion + 1)

        else:
            refract_color = color(0, 0, 0)
        
        refraction = refract_color * material.albedo[3]
        shadow_bias = 1.1
        shadow_origin = intersect.point + (intersect.normal * shadow_bias)
        shadow_material, shadow_intersect = self.scene_intersect(shadow_origin, l_dir)
        shadow_intensity = 1
        if shadow_material:
            shadow_intensity = 1

        
        diffuse = material.diffuse * diffuse_intensity * material.albedo[0] * shadow_intensity
        light_reflection = reflect(l_dir, intersect.normal)
        reflection_intensity =  max(0, dot(light_reflection, direction))
        specular_intensity = self.light.intensity * reflection_intensity**material.spec
        specular = self.light.color * specular_intensity * material.albedo[1]
        reflection = reflect_color * material.albedo[2]

        return diffuse + specular + reflection + refraction


    def scene_intersect(self, origin, direction):
        zbuffer = 9999
        material = None
        intersect = None

        for o in self.scene:
            object_intersect = o.ray_intersect(origin, direction)

            if object_intersect:
                if object_intersect.distance < zbuffer:
                    zbuffer = object_intersect.distance
                    material = o.material
                    intersect = object_intersect
            
        return material, intersect