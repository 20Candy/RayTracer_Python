from lib import *
from intersect import *

class Plane(object):
    def __init__(self, center, w=1, h=1, xyz = "y", material=None, normal = V3(0, 1, 0)):
        self.center = center
        self.w = w
        self.h = h
        self.material = material
        self.normal = normal
        self.xyz = xyz

    def ray_intersect(self, origin, direction):
        distance = 0  

        if self.xyz == "x":
            distance = -(((self.center.x + origin.x)) / direction.x)


            hit_point = sum(mul(direction, distance), origin)

            if distance <= 0 or hit_point.y > (self.center.y + self.w/2) or hit_point.y < (self.center.y - self.w/2) or hit_point.z > (self.center.z + self.h/2) or hit_point.z < (self.center.z - self.h/2):
                return None

            # Retorno de la función.
            return Intersect(distance, hit_point, self.normal)

        elif self.xyz == "y":
            distance = -(((self.center.y + origin.y)) / direction.y)

            hit_point = sum(mul(direction, distance), origin)

            if ((distance <= 0) or (hit_point.x > (self.center.x + (self.w / 2))) or (hit_point.x < (self.center.x - (self.w / 2))) or (hit_point.z > (self.center.z + (self.h / 2))) or (hit_point.z < (self.center.z - (self.h / 2)))):
                return None

            # Retorno de la función.
            return Intersect(distance, hit_point, self.normal)

        elif self.xyz == "z":
            distance = -(((self.center.z + origin.z)) / direction.z)

            hit_point = sum(mul(direction, distance), origin)

            if distance <= 0 or hit_point.x > (self.center.x + self.w/2) or hit_point.x < (self.center.x - self.w/2) or hit_point.y > (self.center.y + self.h/2) or hit_point.y < (self.center.y - self.h/2):
                return None

            # Retorno de la función.
            return Intersect(distance, hit_point, self.normal)
