import math
from PyQt5.QtGui import qRgb

def scanline_fill(points, image, debug=False):
    if not points:
        return
    edges = []
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        if y1 != y2:
            edges.append(((x1, y1), (x2, y2)))
    ys = [y for _, y in points]
    min_y = int(math.ceil(min(ys)))
    max_y = int(math.floor(max(ys)))
    for y in range(min_y, max_y + 1):
        xints = []
        for (x1, y1), (x2, y2) in edges:
            if (y1 <= y < y2) or (y2 <= y < y1):
                x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                xints.append(x)
        xints.sort()
        for i in range(0, len(xints), 2):
            x_start = int(math.ceil(xints[i]))
            x_end = int(math.floor(xints[i+1]))
            for x in range(x_start, x_end + 1):
                if 0 <= x < image.width() and 0 <= y < image.height():
                    image.setPixel(x, y, qRgb(0, 0, 255))
        if debug:
            yield y


def seed_fill(points, image, debug=False):
    if not points:
        return
    x0 = sum(x for x, _ in points) / len(points)
    y0 = sum(y for _, y in points) / len(points)
    seed = (int(x0), int(y0))
    target_color = image.pixel(seed[0], seed[1])
    fill_color = qRgb(255, 0, 0)
    stack = [seed]
    visited = set()
    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        if not (0 <= x < image.width() and 0 <= y < image.height()):
            continue
        if image.pixel(x, y) != target_color:
            continue
        image.setPixel(x, y, fill_color)
        visited.add((x, y))
        if debug:
            yield (x, y)
        stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])