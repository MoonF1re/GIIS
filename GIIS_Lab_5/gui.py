import tkinter as tk
from geometry import delaunay_triangulation, voronoi_diagram

class VoronoiApp:
    def __init__(self):
        self.points = []
        self.root = tk.Tk()
        self.root.title("Диаграмма Вороного и триангуляция Делоне")
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Button-3>", self.compute)

    def add_point(self, event):
        self.points.append((event.x, event.y))
        self.canvas.create_oval(event.x - 2, event.y - 2, event.x + 2, event.y + 2, fill="black")

    def compute(self, event):
        self.canvas.delete("all")
        for x, y in self.points:
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")

        triangles = delaunay_triangulation(self.points)
        for a, b, c in triangles:
            self.canvas.create_line(a, b, fill="blue")
            self.canvas.create_line(b, c, fill="blue")
            self.canvas.create_line(c, a, fill="blue")

        edges = voronoi_diagram(self.points, bounds=(0, 0, self.canvas_width, self.canvas_height))
        for p1, p2 in edges:
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="red")

    def run(self):
        self.root.mainloop()
