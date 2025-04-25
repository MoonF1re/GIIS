class Polygon:
    def __init__(self):
        self.points = []
        self.closed = False

    def add_point(self, x, y):
        if self.closed:
            self.points = []
            self.closed = False
        self.points.append((x, y))

    def close(self):
        if len(self.points) > 2:
            self.closed = True