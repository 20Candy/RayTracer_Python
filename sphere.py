from lib import *
from intersect import *

class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        L = sub(self.center, orig)
        tca = dot(L, dir)
        l = L.length()

        d2 = l**2 - tca**2

        if(d2 > self.radius**2):
            return None

        thc = (self.radius**2 - d2)**0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        
        if t1 < 0:
            return None

        impact_point = sum(orig, mul(dir, t0))
        normal = norm(sub(impact_point, self.center))

        return Intersect(
            distance = t0,
            point = impact_point,
            normal = normal
        )


