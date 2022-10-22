from math import atan2, acos, pi
import struct
from lib import norm
from color import color

class Envmap(object):
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        with open(self.path, "rb") as image:
            image.seek(2 + 4 + 4) 
            header_size = struct.unpack("=l", image.read(4))[0] 
            image.seek(2 + 4 + 4 + 4 + 4)
            
            self.width = struct.unpack("=l", image.read(4))[0]
            self.height = struct.unpack("=l", image.read(4))[0]

            image.seek(header_size)

            self.pixels = [
                [ bytes([0, 0, 0]) for y in range(self.height)]
                for x in range(self.width) 
            ]

            for y in reversed(range(self.height)):
                self.pixels.append([])
                for x in reversed(range(self.width)):
                    b = ord(image.read(1))
                    g = ord(image.read(1))
                    r = ord(image.read(1))

                    c = color(r,g,b)

                    try:
                        self.pixels[y][x] = c
                    except:
                        pass


    def get_color(self, direction):
        direction = norm(direction)

        x = min((atan2(direction.z, direction.x) / (2 * pi) + 0.5)*2, 1)
        y = min((acos(-direction.y) / pi)*2, 1)

        x = int(x * self.width)
        y = int(y * self.height)

        if (x > 0):
            x -= 1 
        else: 0
        
        if (y > 0):
            y -= 1 
        else: y=0

        return self.pixels[y][x]




