from lib import *
from triangle import *
from obj import *

def trans(vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
    return V3(
        round((vertex[0] + translate[0]) * scale[0]),
        round((vertex[1] + translate[1]) * scale[1]),
        round((vertex[2] + translate[2]) * scale[2])
    )


def cargar(filename, translate=(0, 0, 0), scale=(1, 1, 1), material= None):
    triangles = []
    model = Obj(filename)

    light = V3(0, 0, 1)

    for face in model.faces:
        vcount = len(face)

        if vcount == 3:
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1

            a = trans(model.vertices[f1], translate, scale)
            b = trans(model.vertices[f2], translate, scale)
            c = trans(model.vertices[f3], translate, scale)

            normal = norm(cross(sub(b, a), sub(c, a)))
            intensity = dot(normal, light)

            if intensity < 0:
                continue

            triangles.append(Triangle(a, b, c, material))
        else:
            # assuming 4
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1
            f4 = face[3][0] - 1

            vertices = [
                trans(model.vertices[f1], translate, scale),
                trans(model.vertices[f2], translate, scale),
                trans(model.vertices[f3], translate, scale),
                trans(model.vertices[f4], translate, scale)
            ]

            normal = norm(cross(sub(vertices[0], vertices[1]), sub(
                vertices[1], vertices[2])))  
            intensity = dot(normal, light)
            grey = round(255 * intensity)
            if grey < 0:
                continue  


            A, B, C, D = vertices

            triangles.append(Triangle(A, B, C, material))
            triangles.append(Triangle(A, D, C, material))

    return triangles
