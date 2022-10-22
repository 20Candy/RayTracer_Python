from plane import Plane
from square import Square
from ray import *
from lib import *
from material import *
from light import *
from envmap import *
from cargar import *
from color import *


r = Raytracer(500,500)
r.light = Light(V3(-20, 40, 20), 3, color(255, 255, 255))
r.density = 1

#MATERIALES -- 5materiales === 25 puntos
grass = Material(diffuse = color(53,104,45), albedo = [0.9,  0.1, 0, 0], spec = 10)
white = Material(diffuse= color(255,255,255), albedo = [0.8,0.2,0,0], spec = 0)
black = Material(diffuse= color(0,0,0), albedo = [0.9,0.1,0,0], spec = 0)
red = Material(diffuse= color(255,0,0), albedo = [0.9,0.1,0,0], spec = 0)

# #ENVMAP
r.envmap = Envmap('./sky.bmp')

# #OBJETOS ---50 puntos
r.scene = cargar(filename='./corazon.obj', translate=(0, 0, -15), scale=(10, 10, 1),material =red)

#FIGURAS == plano, cuadrado, triangulo = 30 puntos
r.scene.extend([
    Plane(V3(0, -5, -15), 25, 15, "y", grass),


    *(Square(V3(-5, -3, -15), (30,30), white)).planes,
    *(Square(V3(-4, -3, -15), (30,30), black)).planes,
    *(Square(V3(-2.5, -3.1, -15), (25,25), white)).planes,
    *(Square(V3(-5.1, -4.5, -15), (10,10), black)).planes,
    *(Square(V3(-3.2, -4.5, -15), (10,10), black)).planes,
    *(Square(V3(-1.5, -3.5, -15), (15,15), white)).planes,
    *(Square(V3(-2.2,-2, -14.5), (5,5), black)).planes,
    *(Square(V3(-2.3,-2, -13.5), (5,5), black)).planes,

    *(Square(V3(4.5, -3, -15), (30,30), white)).planes,
    *(Square(V3(3.5, -3, -15), (30,30), black)).planes,
    *(Square(V3(2, -3.1, -15), (25,25), white)).planes,
    *(Square(V3(5, -4.5, -15), (10,10), black)).planes,
    *(Square(V3(3, -4.5, -15), (10,10), black)).planes,
    *(Square(V3(1, -3.5, -15), (15,15), white)).planes,
    *(Square(V3(1.9,-2, -14.5), (5,5), black)).planes,
    *(Square(V3(2,-2, -13.5), (5,5), black)).planes,

])


r.render()
r.write()