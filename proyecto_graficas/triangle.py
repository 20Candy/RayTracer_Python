from lib import *
from intersect import *
from obj import *
from math import *

class Triangle(object):
    def __init__(self,  A,B,C, material=None):
        self.v0 = A
        self.v1 = B
        self.v2 = C
        self.material = material


    def ray_intersect(self, origin, direction):
        normal = cross(sub(self.v1, self.v0), sub(self.v2, self.v0))
        determinant = dot(normal, direction)

        if abs(determinant) < 0.0001:
            return None

        distance = dot(normal, self.v0)
        t = (dot(normal, origin) + distance) / determinant
        if t < 0:
            return None

        point = sum(origin, mul(direction, t))
        u, v, w = barycentric(self.v0, self.v1, self.v2, point)

        x = self.v0.x * u + self.v1.x * v + self.v2.x * w
        y = self.v0.y * u + self.v1.y * v + self.v2.y * w
        z = self.v0.z * u + self.v1.z * v + self.v2.z * w

        point = V3(x, y, z)
        
        distance = (point.x - origin.x) * (point.x - origin.x) + (point.y - origin.y) * (point.y - origin.y) + (point.z - origin.z) * (point.z - origin.z)
        distance = sqrt(distance)


        if w < 0 or v < 0 or u < 0:
            return None
                
        
        return Intersect(distance = distance,
                         point = point,
                         normal = norm(normal))



