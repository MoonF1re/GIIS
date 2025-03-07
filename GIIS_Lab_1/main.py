import tkinter as tk
from drawing import PIXEL_SIZE, draw_pixel, draw_grid, intensity_to_color
from algorithms import (dda_line, bresenham_line, wu_line,
                        circle_curve, ellipse_curve, parabola_curve, hyperbola_curve)
import math


class LineEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Элементарный графический редактор")
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Рисуем сетку при инициализации
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
        self.curve_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Линии второго порядка", menu=self.curve_menu)
        self.curve_menu.add_command(label="Окружность", command=lambda: self.set_curve("circle"))
        self.curve_menu.add_command(label="Эллипс", command=lambda: self.set_curve("ellipse"))
        self.curve_menu.add_command(label="Парабола", command=lambda: self.set_curve("parabola"))
        self.curve_menu.add_command(label="Гипербола", command=lambda: self.set_curve("hyperbola"))

        # Отладочный режим и команда очистки
        self.debug_mode = tk.BooleanVar(value=False)
        self.menu.add_checkbutton(label="Отладочный режим", onvalue=True, offvalue=False, variable=self.debug_mode)
        self.menu.add_command(label="Очистить", command=self.clear_canvas)

        # Режимы по умолчанию
        self.current_mode = "line"
        self.current_algorithm = "DDA"
        self.current_curve = None

        self.start_point = None
        self.temp_marker = None

        # Задержка / Скорость режима откладки (мс)
        self.debug_delay = 10

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def set_line(self, algorithm):
        self.current_mode = "line"
        self.current_algorithm = algorithm

    def set_curve(self, curve_type):
        self.current_mode = "curve"
        self.current_curve = curve_type

    def clear_canvas(self):
        self.canvas.delete("all")
        draw_grid(self.canvas)

    def on_canvas_click(self, event):
        #Преобразую клик в точку
        grid_x = event.x // PIXEL_SIZE
        grid_y = event.y // PIXEL_SIZE
        if self.start_point is None:
            self.start_point = (grid_x, grid_y)
            # Рисуем временный маркер
            marker_radius = 2
            cx = grid_x * PIXEL_SIZE + PIXEL_SIZE // 2
            cy = grid_y * PIXEL_SIZE + PIXEL_SIZE // 2
            self.temp_marker = self.canvas.create_oval(cx - marker_radius, cy - marker_radius,
                                                       cx + marker_radius, cy + marker_radius,
                                                       outline="red", fill="red")
        else:
            end_point = (grid_x, grid_y)

            if self.temp_marker is not None:
                self.canvas.delete(self.temp_marker)
                self.temp_marker = None
            if self.current_mode == "line":
                self.draw_line(self.start_point[0], self.start_point[1],
                               end_point[0], end_point[1])
            elif self.current_mode == "curve":
                self.draw_curve(self.start_point, end_point)
            self.start_point = None

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

    def draw_curve(self, start, end):
        debug = self.debug_mode.get()
        if self.current_curve == "circle":
            cx, cy = start
            r = math.sqrt((end[0] - cx) ** 2 + (end[1] - cy) ** 2)
            points = list(circle_curve(cx, cy, r))
            color = "blue"
            self._draw_points_with_stitch(points, color, debug)
        elif self.current_curve == "ellipse":
            cx, cy = start
            rx = abs(end[0] - cx)
            ry = abs(end[1] - cy)
            points = list(ellipse_curve(cx, cy, rx, ry))
            color = "blue"
            self._draw_points_with_stitch(points, color, debug)
        elif self.current_curve == "parabola":
            vx, vy = start
            t = end[0] - vx
            if t == 0:
                t = 1
            a = (end[1] - vy) / (t * t)
            # Для отладки сокращаем диапазон для ускорения анимации
            range_val = 50 if debug else 100
            points = list(parabola_curve(vx, vy, a, range_val))
            color = "blue"
            self._draw_points_with_stitch(points, color, debug)
        elif self.current_curve == "hyperbola":
            cx, cy = start
            a = abs(end[0] - cx)
            b = abs(end[1] - cy)
            if a == 0: a = 1
            if b == 0: b = 1

            ru, rl, lu, ll = hyperbola_curve(cx, cy, a, b)
            color = "blue"
            # Отрисовываем каждую дугу с «сшивкой» соседних точек
            self._draw_points_with_stitch(ru, color, debug)
            self._draw_points_with_stitch(rl, color, debug)
            self._draw_points_with_stitch(lu, color, debug)
            self._draw_points_with_stitch(ll, color, debug)
        else:
            return

    def _draw_points_with_stitch(self, points, color, debug):
        """Отрисовывает последовательность точек, соединяя соседние отрезками Брезенхэма."""
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


if __name__ == "__main__":
    root = tk.Tk()
    app = LineEditor(root)
    root.mainloop()
