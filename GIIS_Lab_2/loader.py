def load_object(file_path):
    vertices = []
    edges = []
    with open(file_path, 'r') as f:
        n, m = map(int, f.readline().split()) #количество вершин n и ребер m
        for _ in range(n):
            x, y, z = map(float, f.readline().split()) #читаем координаты вершин
            vertices.append([x, y, z, 1.0])  # однородные координаты
        for _ in range(m):
            i, j = map(int, f.readline().split()) #читаем рёбра \ от вершины А к Б
            edges.append((i, j))
    return vertices, edges