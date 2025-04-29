import math
from collections import defaultdict

def circumcircle(a, b, c):
    ax, ay = a
    bx, by = b
    cx, cy = c
    d = 2 * (ax*(by - cy) + bx*(cy - ay) + cx*(ay - by))
    if d == 0:
        return None, float('inf')
    ux = ((ax**2 + ay**2)*(by - cy) + (bx**2 + by**2)*(cy - ay) + (cx**2 + cy**2)*(ay - by)) / d
    uy = ((ax**2 + ay**2)*(cx - bx) + (bx**2 + by**2)*(ax - cx) + (cx**2 + cy**2)*(bx - ax)) / d
    r = math.hypot(ax - ux, ay - uy)
    return (ux, uy), r

def in_circle(p, center, radius):
    return math.hypot(p[0] - center[0], p[1] - center[1]) < radius

def delaunay_triangulation(points):
    super_triangle = [(-10000, -10000), (0, 20000), (20000, -10000)]
    triangles = [tuple(super_triangle)]

    for p in points:
        bad = []
        for tri in triangles:
            center, radius = circumcircle(*tri)
            if center and in_circle(p, center, radius):
                bad.append(tri)
        edge_buffer = []
        for tri in bad:
            for i in range(3):
                edge = (tri[i], tri[(i + 1) % 3])
                if edge[::-1] in edge_buffer:
                    edge_buffer.remove(edge[::-1])
                else:
                    edge_buffer.append(edge)
        for tri in bad:
            triangles.remove(tri)
        for e in edge_buffer:
            triangles.append((e[0], e[1], p))

    final = [tri for tri in triangles if not any(v in super_triangle for v in tri)]
    return final

def voronoi_diagram(points, bounds=(0, 0, 800, 600)):
    triangles = delaunay_triangulation(points)
    edge_to_centers = defaultdict(list)
    triangle_centers = {}

    for tri in triangles:
        center, _ = circumcircle(*tri)
        triangle_centers[tri] = center
        for i in range(3):
            edge = frozenset((tri[i], tri[(i + 1) % 3]))
            edge_to_centers[edge].append(center)

    edges = []
    for edge, centers in edge_to_centers.items():
        if len(centers) == 2:
            edges.append((centers[0], centers[1]))
        elif len(centers) == 1:
            pts = list(edge)
            midx = (pts[0][0] + pts[1][0]) / 2
            midy = (pts[0][1] + pts[1][1]) / 2
            dx = pts[1][0] - pts[0][0]
            dy = pts[1][1] - pts[0][1]
            nx, ny = -dy, dx
            length = math.hypot(nx, ny)
            if length == 0:
                continue
            nx /= length
            ny /= length
            far_point = (midx + nx * 1000, midy + ny * 1000)
            x0, y0, x1, y1 = bounds
            cx, cy = centers[0]
            clipped = clip_line((cx, cy), far_point, x0, y0, x1, y1)
            if clipped:
                edges.append(((cx, cy), clipped))

    return edges

def clip_line(p1, p2, x_min, y_min, x_max, y_max):
    """
    Простая обрезка линии по границам прямоугольника.
    """
    def inside(x, y):
        return x_min <= x <= x_max and y_min <= y <= y_max

    x1, y1 = p1
    x2, y2 = p2

    dx = x2 - x1
    dy = y2 - y1

    for t in [i / 100 for i in range(1, 101)]:
        x = x1 + dx * t
        y = y1 + dy * t
        if not inside(x, y):
            return (x - dx * 0.01, y - dy * 0.01)

    return None
