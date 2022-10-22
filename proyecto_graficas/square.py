from lib import *
from intersect import *
from plane import Plane

class Square(object):
    def __init__(self, center, size, material):
        self.center = center
        self.size = size
        self.material = material

        self.planes = []

        w, h = size[0] / max(1, abs(center.z)), size[1] / max(1, abs(center.z))

        self.planes.append( Plane(V3((w/2)-center.x, -center.y, center.z), w, h, "x", material, V3(1,0,0)))
        self.planes.append( Plane(V3(-(w/2)-center.x, -center.y, center.z), w, h, "x", material, V3(-1,0,0)))

        self.planes.append( Plane(V3(center.x, center.y+(h/2), center.z), w, h,"y", material, V3(0,1,0)))
        self.planes.append( Plane(V3(center.x, center.y-(h/2), center.z), w, h,"y", material, V3(0,1,0)))

        self.planes.append( Plane(V3(center.x, -center.y, (w/2)-center.z), w, h, "z", material, V3(0,0,1)))
        self.planes.append( Plane(V3(center.x, -center.y, -center.z-(w/2)), w, h, "z", material, V3(0,0,1)))

