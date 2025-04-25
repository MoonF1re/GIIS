import pygame
import math

def draw_line_dda(screen, p1, p2):
    x1,y1 = p1; x2,y2 = p2
    dx, dy = x2-x1, y2-y1
    steps = int(max(abs(dx), abs(dy)))
    x_inc = dx/steps; y_inc = dy/steps
    x,y = x1,y1
    for _ in range(steps+1):
        screen.set_at((int(x),int(y)), (0,0,0)); x+=x_inc; y+=y_inc

def draw_line_bresenham(screen, p1, p2):
    x1,y1 = map(int,p1); x2,y2 = map(int,p2)
    dx, dy = abs(x2-x1), abs(y2-y1)
    sx = 1 if x2>=x1 else -1; sy = 1 if y2>=y1 else -1
    err = dx-dy
    while True:
        screen.set_at((x1,y1),(0,0,0))
        if x1==x2 and y1==y2: break
        e2 = 2*err
        if e2> -dy: err-=dy; x1+=sx
        if e2<  dx: err+=dx; y1+=sy

def draw_line_wu(screen, p1, p2):
    # упрощённый алгоритм Ву
    x1,y1 = p1; x2,y2 = p2
    steep = abs(y2-y1)>abs(x2-x1)
    if steep: x1,y1=y1,x1; x2,y2=y2,x2
    if x1>x2: x1,x2=x2,x1; y1,y2=y2,y1
    dx = x2-x1; dy = y2-y1
    gradient = dy/dx if dx else 1
    y = y1+gradient
    for x in range(int(x1)+1, int(x2)):
        if steep:
            screen.set_at((int(y),x),(0,0,0))
        else:
            screen.set_at((x,int(y)),(0,0,0))
        y+=gradient