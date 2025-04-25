import pygame
import math

class Polygon:
    def __init__(self):
        self.points = []
        self.closed = False
        self.normals = []

    def add_point(self, pt):
        if not self.closed:
            self.points.append(pt)

    def close(self):
        if len(self.points) > 2:
            self.closed = True

    def clear(self):
        self.points = []
        self.closed = False
        self.normals = []

    def calculate_normals(self):
        self.normals = []
        if not self.closed: return
        n = len(self.points)
        for i in range(n):
            x1,y1 = self.points[i]
            x2,y2 = self.points[(i+1)%n]
            dx,dy = x2-x1, y2-y1
            # внутренняя нормаль: (-dy, dx), нормируем:
            length = math.hypot(dx, dy)
            nx, ny = -dy/length, dx/length
            self.normals.append(((x1+x2)/2, (y1+y2)/2, nx, ny))

    def is_convex(self):
        # проверка знаков поворота
        if not self.closed: return False
        n = len(self.points)
        prev = 0
        for i in range(n):
            x1,y1 = self.points[i]
            x2,y2 = self.points[(i+1)%n]
            x3,y3 = self.points[(i+2)%n]
            z = (x2-x1)*(y3-y2) - (y2-y1)*(x3-x2)
            """
            Это векторное произведение — оно показывает, в какую сторону поворачивает угол между двумя сторонами:

                0 — поворот налево

                <0 — поворот направо

                =0 — точки на одной прямой
            """
            if z != 0:
                if prev*z < 0:
                    return False
                prev = z
        return True

    def contains_point(self, pt):
        # лучевой метод
        x0,y0 = pt
        count = 0
        n = len(self.points)
        for i in range(n):
            x1,y1 = self.points[i]
            x2,y2 = self.points[(i+1)%n]
            if ((y1>y0) != (y2>y0)) and (x0 < (x2-x1)*(y0-y1)/(y2-y1)+x1):
                count += 1
        return count%2==1

    def draw(self, screen, draw_line):
        # рисуем ребра
        if len(self.points)>1:
            pts = self.points + ([self.points[0]] if self.closed else [])
            for i in range(len(pts)-1):
                draw_line(screen, pts[i], pts[i+1])
        # рисуем точки
        for x,y in self.points:
            pygame.draw.circle(screen, (0,0,0), (int(x),int(y)), 3)
        # рисуем нормали
        for cx,cy,nx,ny in self.normals:
            end = (cx+nx*20, cy+ny*20)
            pygame.draw.line(screen, (255,0,0), (cx,cy), end, 2)

    def set_points(self, points):
        self.points = points
        self.closed = True
        self.normals = []
