import math


# ---Алгоритмы для линий ---

def dda_line(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    steps = int(max(abs(dx), abs(dy)))
    if steps == 0:
        yield (x0, y0)
        return
    x_inc = dx / steps
    y_inc = dy / steps
    x = x0
    y = y0
    for i in range(steps + 1):
        yield (round(x), round(y))
        x += x_inc
        y += y_inc


def bresenham_line(x0, y0, x1, y1):
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        yield (x0, y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def wu_line(x0, y0, x1, y1):
    def fpart(x):
        return x - math.floor(x)

    def rfpart(x):
        return 1 - fpart(x)

    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0
    gradient = dy / dx if dx != 0 else 1

    xend = round(x0)
    yend = y0 + gradient * (xend - x0)
    xgap = rfpart(x0 + 0.5)
    xpxl1 = xend
    ypxl1 = int(math.floor(yend))
    if steep:
        yield (ypxl1, xpxl1, rfpart(yend) * xgap)
        yield (ypxl1 + 1, xpxl1, fpart(yend) * xgap)
    else:
        yield (xpxl1, ypxl1, rfpart(yend) * xgap)
        yield (xpxl1, ypxl1 + 1, fpart(yend) * xgap)
    intery = yend + gradient

    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = fpart(x1 + 0.5)
    xpxl2 = xend
    ypxl2 = int(math.floor(yend))
    if steep:
        yield (ypxl2, xpxl2, rfpart(yend) * xgap)
        yield (ypxl2 + 1, xpxl2, fpart(yend) * xgap)
    else:
        yield (xpxl2, ypxl2, rfpart(yend) * xgap)
        yield (xpxl2, ypxl2 + 1, fpart(yend) * xgap)

    if steep:
        for x in range(xpxl1 + 1, xpxl2):
            y = int(math.floor(intery))
            yield (y, x, rfpart(intery))
            yield (y + 1, x, fpart(intery))
            intery += gradient
    else:
        for x in range(xpxl1 + 1, xpxl2):
            y = int(math.floor(intery))
            yield (x, y, rfpart(intery))
            yield (x, y + 1, fpart(intery))
            intery += gradient


# --- Алгоритмы для кривых второго порядка ---

def circle_curve(cx, cy, r):
    if r < 0:
        return
    steps = int(2 * math.pi * r)
    if steps == 0:
        steps = 1
    for i in range(steps + 1):
        theta = 2 * math.pi * i / steps
        x = cx + r * math.cos(theta)
        y = cy + r * math.sin(theta)
        yield (round(x), round(y))


def ellipse_curve(cx, cy, rx, ry):
    steps = int(2 * math.pi * max(rx, ry))
    if steps == 0:
        steps = 1
    for i in range(steps + 1):
        theta = 2 * math.pi * i / steps
        x = cx + rx * math.cos(theta)
        y = cy + ry * math.sin(theta)
        yield (round(x), round(y))


def parabola_curve(vx, vy, a, range_val=100):
    #y = a * (x - vx)^2 + vy
    for t in range(-range_val, range_val + 1):
        x = vx + t
        y = vy + a * t * t
        yield (round(x), round(y))


def hyperbola_curve(cx, cy, a, b, range_val=100):
    """
    (x-cx)^2/a^2 - (y-cy)^2/b^2 = 1.
    Функция возвращает 4 списка точек:
      right_upper, right_lower, left_upper, left_lower
    Каждый список представляет контур дуги гиперболы.
    """
    right_upper = []
    right_lower = []
    left_upper = []
    left_lower = []
    # Правая ветвь
    for x in range(int(cx + a), int(cx + range_val)):
        try:
            val = ((x - cx) ** 2) / (a ** 2) - 1
            if val < 0:
                continue
            y_offset = b * math.sqrt(val)
        except ValueError:
            continue
        right_upper.append((x, round(cy + y_offset)))
        right_lower.append((x, round(cy - y_offset)))
    # Левая ветвь
    for x in range(int(cx - range_val), int(cx - a) + 1):
        try:
            val = ((x - cx) ** 2) / (a ** 2) - 1
            if val < 0:
                continue
            y_offset = b * math.sqrt(val)
        except ValueError:
            continue
        left_upper.append((x, round(cy + y_offset)))
        left_lower.append((x, round(cy - y_offset)))

    right_upper.sort(key=lambda p: p[0])
    right_lower.sort(key=lambda p: p[0])
    left_upper.sort(key=lambda p: p[0])
    left_lower.sort(key=lambda p: p[0])
    return right_upper, right_lower, left_upper, left_lower
