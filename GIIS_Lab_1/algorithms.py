import math

# --- Линейные алгоритмы ---

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

# --- Кривые второго порядка ---

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
    for t in range(-range_val, range_val + 1):
        x = vx + t
        y = vy + a * t * t
        yield (round(x), round(y))

def hyperbola_curve(cx, cy, a, b, range_val=100):
    right_upper = []
    right_lower = []
    left_upper = []
    left_lower = []
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

# --- Функции для матричных вычислений ---

def mat_mult(A, B):
    result = [[0 for j in range(len(B[0]))] for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def vec_mult(M, v):
    result = [0 for i in range(len(M))]
    for i in range(len(M)):
        for j in range(len(v)):
            result[i] += M[i][j] * v[j]
    return result

# --- Кривые третьего порядка ---

def hermite_curve(P0, P1, T0, T1, steps):
    """
    Построение кривой Эрмита с использованием параметрического уравнения:
      P(t) = h00(t)*P0 + h10(t)*T0 + h01(t)*P1 + h11(t)*T1,
    где базисные функции задаются как:
      h00(t) = 2t^3 - 3t^2 + 1,
      h10(t) = t^3 - 2t^2 + t,
      h01(t) = -2t^3 + 3t^2,
      h11(t) = t^3 - t^2.
    Для вычисления коэффициентов используется матричный метод.

    P0, P1 – конечные точки; T0, T1 – касательные в точках P0 и P1.
    Возвращает список точек кривой.
    """
    # Определяем матрицу Hermite таким образом, чтобы при умножении на вектор [t^3, t^2, t, 1]^T
    # получались коэффициенты [h00, h10, h01, h11].
    H = [
        [2, -3, 0, 1],  # коэффициент h00
        [1, -2, 1, 0],  # коэффициент h10
        [-2, 3, 0, 0],  # коэффициент h01
        [1, -1, 0, 0]  # коэффициент h11
    ]
    points = []
    for i in range(steps + 1):
        t = i / steps
        T = [t ** 3, t ** 2, t, 1]
        #coeffs = H * [t^3, t^2, t, 1]^T
        coeffs = vec_mult(H, T)
        # В соответствии с формулой Эрмита:
        # P(t) = h00*P0 + h10*T0 + h01*P1 + h11*T1
        x = coeffs[0] * P0[0] + coeffs[1] * T0[0] + coeffs[2] * P1[0] + coeffs[3] * T1[0]
        y = coeffs[0] * P0[1] + coeffs[1] * T0[1] + coeffs[2] * P1[1] + coeffs[3] * T1[1]
        points.append((round(x), round(y)))
    return points


def bezier_curve(P0, P1, P2, P3, steps):
    points = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1 - t
        b0 = mt**3
        b1 = 3 * mt**2 * t
        b2 = 3 * mt * t**2
        b3 = t**3
        x = b0 * P0[0] + b1 * P1[0] + b2 * P2[0] + b3 * P3[0]
        y = b0 * P0[1] + b1 * P1[1] + b2 * P2[1] + b3 * P3[1]
        points.append((round(x), round(y)))
    return points

def bspline_curve(control_points, steps):
    n = len(control_points)
    if n < 4:
        return []
    points = []
    for i in range(n - 3):
        for j in range(steps + 1):
            t = j / steps
            b0 = ((1 - t)**3) / 6
            b1 = (3 * t**3 - 6 * t**2 + 4) / 6
            b2 = (-3 * t**3 + 3 * t**2 + 3 * t + 1) / 6
            b3 = t**3 / 6
            x = b0 * control_points[i][0] + b1 * control_points[i+1][0] + b2 * control_points[i+2][0] + b3 * control_points[i+3][0]
            y = b0 * control_points[i][1] + b1 * control_points[i+1][1] + b2 * control_points[i+2][1] + b3 * control_points[i+3][1]
            points.append((round(x), round(y)))
    return points
