from lib import *
from sphere import *
from math import *
from color import *

MAX_RECURSION_DEPTH = 3

class Raytracer (object):
    def __init__ (self, width, height):
        self.width = width
        self.height = height
        self.background_color = color(109,157,197)
        self.current_color = color(255,255,255)
        self.clear_color = color(0,0,0)
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
    def cast_ray(self, origin, direction, recursion = 0):

        if(recursion == MAX_RECURSION_DEPTH):
            return self.background_color

        material, intersect = self.scene_intersect(origin, direction)

        if material is None:
            return self.background_color
        
        l_dir = norm(sub(self.light.position, intersect.point))

        #shadow
        shadow_bias = 1.1
        shadow_origin = sum(intersect.point, mul(intersect.normal, shadow_bias))
        shadow_material, shadow_intersect = self.scene_intersect(shadow_origin, l_dir)
        shadow_intensity = 0.75 if (shadow_material is not None) else 0
 
        #diffuse
        diffuse_intensity = dot( l_dir, intersect.normal)

        #specular
        light_reflection = reflect(l_dir, intersect.normal)
        reflection_intensity = max(0, dot(light_reflection, direction))
        specular_intensity = (reflection_intensity ** material.spec) * self.light.intensity
        specular = self.light.color * specular_intensity * material.albedo[1]

        # reflection
        if material.albedo[2] > 0:
            reverse_direction = mul(direction, -1)
            reflect_direction = reflect(reverse_direction, intersect.normal)
            reflection_bias = -0.5 if dot(reflect_direction, intersect.normal) < 0 else 0.5
            reflect_origin = sum(intersect.point, mul(intersect.normal, reflection_bias))
            reflect_color = self.cast_ray(reflect_origin, reflect_direction, recursion + 1)
        else:
            reflect_color = color(0,0,0)

        # refraction
        if (material.albedo[3] > 0):
            refraction_direction = refract(direction, intersect.normal, material.refractive_index)
            refraction_bias = -0.5 if dot(refraction_direction, intersect.normal) < 0 else 0.5
            refraction_origin = sum(intersect.point, mul(intersect.normal, refraction_bias))
            refract_color = self.cast_ray(refraction_origin, refraction_direction, recursion + 1)
        else:
            refract_color = color(0, 0, 0)


        reflection= reflect_color * material.albedo[2]
        refraction = refract_color * material.albedo[3]

        diffuse = material.diffuse * diffuse_intensity * material.albedo[0] * (1- shadow_intensity) + specular + reflection + refraction

        #return
        return diffuse
    

    def scene_intersect(self, origin, direction):
        zbuffer = 999999
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
  

    def render (self):
        fov = int(pi/2)  #apertura del angulo de la camara
        ar = self.width/self.height #aspect ratio
        tana = tan(fov/2) #tan del angulo de la camara

        for y in range(self.height):
            for x in range(self.width):
                i = ((2 * (x + 0.5) / self.width) - 1) * ar * tana
                j = (1 - 2 * (y + 0.5) / self.height) * tana

                direction = V3(i, j, -1).norm()
                origin = V3(0,0,0)

                c = self.cast_ray(origin, direction)

                self.point(x, y, c)
