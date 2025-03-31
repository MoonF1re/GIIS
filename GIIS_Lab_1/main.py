import tkinter as tk
from drawing import PIXEL_SIZE, draw_pixel, draw_grid, intensity_to_color
from algorithms import (dda_line, bresenham_line, wu_line,
                        circle_curve, ellipse_curve, parabola_curve, hyperbola_curve,
                        hermite_curve, bezier_curve, bspline_curve, mat_mult, vec_mult)
import math

class LineEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Элементарный графический редактор")
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        draw_grid(self.canvas)

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        # Меню для отрезков
        self.line_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Отрезки", menu=self.line_menu)
        self.line_menu.add_command(label="ЦДА", command=lambda: self.set_line("DDA"))
        self.line_menu.add_command(label="Брезенхем", command=lambda: self.set_line("Bresenham"))
        self.line_menu.add_command(label="Ву", command=lambda: self.set_line("Wu"))

        # Меню для кривых второго порядка
        self.curve2_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Линии 2 порядка", menu=self.curve2_menu)
        self.curve2_menu.add_command(label="Окружность", command=lambda: self.set_curve2("circle"))
        self.curve2_menu.add_command(label="Эллипс", command=lambda: self.set_curve2("ellipse"))
        self.curve2_menu.add_command(label="Парабола", command=lambda: self.set_curve2("parabola"))
        self.curve2_menu.add_command(label="Гипербола", command=lambda: self.set_curve2("hyperbola"))

        # Меню для кривых третьего порядка
        self.curve3_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Кривые 3 порядка", menu=self.curve3_menu)
        self.curve3_menu.add_command(label="Эрмит", command=lambda: self.set_cubic("hermite"))
        self.curve3_menu.add_command(label="Безье", command=lambda: self.set_cubic("bezier"))
        self.curve3_menu.add_command(label="B-сплайн", command=lambda: self.set_cubic("bspline"))
        self.curve3_menu.add_command(label="Построить кривую 3 порядка", command=self.draw_cubic_curve)
        self.curve3_menu.add_command(label="Удалить последнюю точку", command=self.remove_last_cubic_point)
        self.curve3_menu.add_command(label="Очистить опорные точки", command=self.clear_cubic_points)

        # Отладочный режим и очистка Canvas
        self.debug_mode = tk.BooleanVar(value=False)
        self.menu.add_checkbutton(label="Отладочный режим", onvalue=True, offvalue=False, variable=self.debug_mode)
        self.menu.add_command(label="Очистить", command=self.clear_canvas)

        # Режимы:
        # "line" - отрезки; "curve2" - кривые второго порядка; "cubic" - кривые третьего порядка.
        self.current_mode = "line"
        self.current_algorithm = "DDA"    # для линий
        self.current_curve2 = None         # для кривых 2 порядка
        self.current_cubic_method = None   # для кривых 3 порядка

        self.start_point = None
        self.temp_marker = None  # временный маркер для первой точки

        # Для кривых 3 порядка накапливаем список опорных точек
        self.cubic_points = []

        # Задержка в отладочном режиме (мс)
        self.debug_delay = 10

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    # Режимы для линий и кривых 2 порядка
    def set_line(self, algorithm):
        self.current_mode = "line"
        self.current_algorithm = algorithm
        self.start_point = None

    def set_curve2(self, curve_type):
        self.current_mode = "curve2"
        self.current_curve2 = curve_type
        self.start_point = None

    # Режим для кривых 3 порядка
    def set_cubic(self, method):
        self.current_mode = "cubic"
        self.current_cubic_method = method
        self.cubic_points = []
        self.start_point = None
        self.canvas.delete("cubic_marker")

    def remove_last_cubic_point(self):
        if self.cubic_points:
            self.cubic_points.pop()
            self.canvas.delete("cubic_marker")
            # Перерисовываем оставшиеся маркеры
            for pt in self.cubic_points:
                grid_x, grid_y = pt
                marker_radius = 2
                cx = grid_x * PIXEL_SIZE + PIXEL_SIZE // 2
                cy = grid_y * PIXEL_SIZE + PIXEL_SIZE // 2
                self.canvas.create_oval(cx - marker_radius, cy - marker_radius,
                                        cx + marker_radius, cy + marker_radius,
                                        outline="green", fill="green", tag="cubic_marker")

    def clear_cubic_points(self):
        self.cubic_points = []
        self.canvas.delete("cubic_marker")

    def clear_canvas(self):
        self.canvas.delete("all")
        draw_grid(self.canvas)

    def on_canvas_click(self, event):
        grid_x = event.x // PIXEL_SIZE
        grid_y = event.y // PIXEL_SIZE
        if self.current_mode in ["line", "curve2"]:
            if self.start_point is None:
                self.start_point = (grid_x, grid_y)
                marker_radius = 2
                cx = grid_x * PIXEL_SIZE + PIXEL_SIZE // 2
                cy = grid_y * PIXEL_SIZE + PIXEL_SIZE // 2
                self.temp_marker = self.canvas.create_oval(cx - marker_radius, cy - marker_radius,
                                                           cx + marker_radius, cy + marker_radius,
                                                           outline="red", fill="red")
            else:
                end_point = (grid_x, grid_y)
                if self.temp_marker:
                    self.canvas.delete(self.temp_marker)
                    self.temp_marker = None
                if self.current_mode == "line":
                    self.draw_line(self.start_point[0], self.start_point[1],
                                   end_point[0], end_point[1])
                elif self.current_mode == "curve2":
                    self.draw_curve2(self.start_point, end_point)
                self.start_point = None
        elif self.current_mode == "cubic":
            # Добавляем опорную точку для кривой 3 порядка
            self.cubic_points.append((grid_x, grid_y))
            marker_radius = 2
            cx = grid_x * PIXEL_SIZE + PIXEL_SIZE // 2
            cy = grid_y * PIXEL_SIZE + PIXEL_SIZE // 2
            self.canvas.create_oval(cx - marker_radius, cy - marker_radius,
                                    cx + marker_radius, cy + marker_radius,
                                    outline="green", fill="green", tag="cubic_marker")

    def draw_line(self, x0, y0, x1, y1):
        debug = self.debug_mode.get()
        if self.current_algorithm == "DDA":
            pixel_gen = dda_line(x0, y0, x1, y1)
            color_func = lambda intensity: "black"
        elif self.current_algorithm == "Bresenham":
            pixel_gen = bresenham_line(x0, y0, x1, y1)
            color_func = lambda intensity: "black"
        elif self.current_algorithm == "Wu":
            pixel_gen = wu_line(x0, y0, x1, y1)
            color_func = intensity_to_color
        else:
            return

        if debug:
            self.animate_pixels(pixel_gen, color_func, self.debug_delay)
        else:
            for p in pixel_gen:
                if self.current_algorithm == "Wu":
                    x, y, intensity = p
                    color = color_func(intensity)
                else:
                    x, y = p
                    color = color_func(None)
                draw_pixel(self.canvas, x, y, color)

    def draw_curve2(self, start, end):
        debug = self.debug_mode.get()
        if self.current_curve2 == "circle":
            cx, cy = start
            r = math.sqrt((end[0] - cx) ** 2 + (end[1] - cy) ** 2)
            points = list(circle_curve(cx, cy, r))
            color = "blue"
            self._draw_points_with_stitch(points, color, debug)
        elif self.current_curve2 == "ellipse":
            cx, cy = start
            rx = abs(end[0] - cx)
            ry = abs(end[1] - cy)
            points = list(ellipse_curve(cx, cy, rx, ry))
            color = "blue"
            self._draw_points_with_stitch(points, color, debug)
        elif self.current_curve2 == "parabola":
            vx, vy = start
            t = end[0] - vx
            if t == 0:
                t = 1
            a = (end[1] - vy) / (t * t)
            range_val = 50 if debug else 100
            points = list(parabola_curve(vx, vy, a, range_val))
            color = "blue"
            self._draw_points_with_stitch(points, color, debug)
        elif self.current_curve2 == "hyperbola":
            cx, cy = start
            a = abs(end[0] - cx)
            b = abs(end[1] - cy)
            if a == 0: a = 1
            if b == 0: b = 1
            ru, rl, lu, ll = hyperbola_curve(cx, cy, a, b)
            color = "blue"
            self._draw_points_with_stitch(ru, color, debug)
            self._draw_points_with_stitch(rl, color, debug)
            self._draw_points_with_stitch(lu, color, debug)
            self._draw_points_with_stitch(ll, color, debug)
        else:
            return

    def _draw_points_with_stitch(self, points, color, debug):
        if not points:
            return
        if debug:
            prev = points[0]
            draw_pixel(self.canvas, prev[0], prev[1], color)
            self.canvas.update()
            self.root.after(self.debug_delay)
            for p in points[1:]:
                for q in bresenham_line(prev[0], prev[1], p[0], p[1]):
                    draw_pixel(self.canvas, q[0], q[1], color)
                    self.canvas.update()
                    self.root.after(self.debug_delay)
                prev = p
        else:
            prev = points[0]
            draw_pixel(self.canvas, prev[0], prev[1], color)
            for p in points[1:]:
                for q in bresenham_line(prev[0], prev[1], p[0], p[1]):
                    draw_pixel(self.canvas, q[0], q[1], color)
                prev = p

    def animate_pixels(self, pixel_gen, color_func, delay):
        try:
            p = next(pixel_gen)
            if isinstance(p, tuple) and len(p) == 3:
                x, y, intensity = p
                color = color_func(intensity)
            else:
                x, y = p
                color = color_func(None)
            draw_pixel(self.canvas, x, y, color)
            self.canvas.update()
            self.root.after(delay, lambda: self.animate_pixels(pixel_gen, color_func, delay))
        except StopIteration:
            return

    def draw_cubic_curve(self):
        """
        Построение кривой третьего порядка по накопленным опорным точкам.
        Метод "hermite" требует минимум 3 точки.
        После построения опорные точки очищаются.
        """
        if self.current_mode != "cubic" or not self.cubic_points:
            return
        method = self.current_cubic_method
        steps = 100  # число точек кривой
        points = []
        if method == "hermite":
            if len(self.cubic_points) < 3:
                print("Для кривой Эрмита требуется минимум 3 точки")
                return
            P0 = self.cubic_points[0]
            P1 = self.cubic_points[-1]
            # Вычисляем касательные: T0 = вектор от первой к второй точке, T1 = вектор от предпоследней к последней
            T0 = (self.cubic_points[1][0] - P0[0], self.cubic_points[1][1] - P0[1])
            T1 = (P1[0] - self.cubic_points[-2][0], P1[1] - self.cubic_points[-2][1])
            print("Построение кривой Эрмита:")
            print("P0 =", P0, "P1 =", P1, "T0 =", T0, "T1 =", T1)
            points = hermite_curve(P0, P1, T0, T1, steps)
        elif method == "bezier":
            if len(self.cubic_points) != 4:
                print("Для кривой Безье требуется ровно 4 точки")
                return
            P0, P1, P2, P3 = self.cubic_points
            points = bezier_curve(P0, P1, P2, P3, steps)
        elif method == "bspline":
            if len(self.cubic_points) < 4:
                print("Для B-сплайна требуется минимум 4 точки")
                return
            points = bspline_curve(self.cubic_points, steps)
        else:
            return
        points = list(points)
        color = "red"
        self._draw_points_with_stitch(points, color, self.debug_mode.get())
        self.clear_cubic_points()

    def remove_last_cubic_point(self):
        if self.cubic_points:
            self.cubic_points.pop()
            self.canvas.delete("cubic_marker")
            for pt in self.cubic_points:
                grid_x, grid_y = pt
                marker_radius = 2
                cx = grid_x * PIXEL_SIZE + PIXEL_SIZE // 2
                cy = grid_y * PIXEL_SIZE + PIXEL_SIZE // 2
                self.canvas.create_oval(cx - marker_radius, cy - marker_radius,
                                        cx + marker_radius, cy + marker_radius,
                                        outline="green", fill="green", tag="cubic_marker")

    def clear_cubic_points(self):
        self.cubic_points = []
        self.canvas.delete("cubic_marker")

if __name__ == "__main__":
    root = tk.Tk()
    app = LineEditor(root)
    root.mainloop()
