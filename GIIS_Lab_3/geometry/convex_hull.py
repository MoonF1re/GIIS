import math

def graham_scan(points):
    # базовый Graham scan
    pts = sorted(points)
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lower=[]
    for p in pts:
        while len(lower)>=2 and cross(lower[-2], lower[-1], p)<=0:
            lower.pop()
        lower.append(p)
    upper=[]
    for p in reversed(pts):
        while len(upper)>=2 and cross(upper[-2], upper[-1], p)<=0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]
"""
https://habrastorage.org/storage2/250/253/036/25025303603cad0f561224ed1e065412.gif
"""

def jarvis_march(points):
    # базовый Jarvis march
    if not points: return []
    hull=[]
    start=min(points)
    point=start
    while True:
        hull.append(point)
        candidate = points[0]
        for p in points[1:]:
            if candidate==point or ((p[0]-point[0])*(candidate[1]-point[1]) - (p[1]-point[1])*(candidate[0]-point[0]))>0:
                candidate = p
        point = candidate
        if point==start: break
    return hull

"""
Как он работает:
Берём самую левую нижнюю точку — она точно на оболочке.

Из неё "смотрим" на все остальные точки и выбираем ту, которая:

образует самый левый поворот (или наименьший угол против часовой стрелки).

Добавляем её в оболочку и повторяем алгоритм уже с неё.

Продолжаем, пока не вернёмся в начальную точку.
"""
