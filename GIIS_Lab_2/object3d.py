class Object3D:
    def __init__(self, vertices, edges):
        self.vertices = vertices  # список однородных векторов
        self.edges = edges

    def transform(self, M):
        self.vertices = [M.dot(v) for v in self.vertices]