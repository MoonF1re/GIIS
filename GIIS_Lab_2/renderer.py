import pygame #Рендерит за нас)
import numpy as np

def project(vertices, width, height, d): #d - фокусное расстояние

    projected = []
    for v in vertices:
        x, y, z, w = v
        # Перспективное деление
        factor = d / (d + z) if (d + z) != 0 else 1
        px = x * factor + width / 2
        py = -y * factor + height / 2
        projected.append((int(px), int(py)))
    return projected


def draw(screen, obj, width, height, d):
    pts = project(obj.vertices, width, height, d)
    for i, j in obj.edges:
        pygame.draw.line(screen, (255, 255, 255), pts[i], pts[j], 1)