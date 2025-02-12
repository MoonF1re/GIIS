import tkinter as tk
from drawing import PIXEL_SIZE, draw_pixel, draw_grid, intensity_to_color
from algorithms import dda_line, bresenham_line, wu_line


class LineEditor:
    def __init__(self, root, w, h):
        self.root = root
        self.root.title("Элементарный графический редактор")
        self.canvas = tk.Canvas(root, bg="white", width=w, height=h)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        draw_grid(self.canvas)

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        self.algorithm_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Отрезки", menu=self.algorithm_menu)
        self.algorithm_menu.add_command(label="ЦДА", command=lambda: self.set_algorithm("DDA"))
        self.algorithm_menu.add_command(label="Брезенхем", command=lambda: self.set_algorithm("Bresenham"))
        self.algorithm_menu.add_command(label="Ву", command=lambda: self.set_algorithm("Wu"))

        self.debug_mode = tk.BooleanVar(value=False)
        self.menu.add_checkbutton(label="Отладочный режим", onvalue=True, offvalue=False, variable=self.debug_mode)

        self.menu.add_command(label="Очистить", command=self.clear_canvas)

        self.current_algorithm = "DDA"  # Алгоритм по умолчанию
        self.start_point = None  # Первая точка отрезка

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def set_algorithm(self, algorithm):
        self.current_algorithm = algorithm

    def clear_canvas(self):
        self.canvas.delete("all")
        draw_grid(self.canvas)

    def on_canvas_click(self, event):
        # Переводим координаты мыши в координаты сетки
        if self.start_point is None:
            self.start_point = (event.x // PIXEL_SIZE, event.y // PIXEL_SIZE)
        else:
            end_point = (event.x // PIXEL_SIZE, event.y // PIXEL_SIZE)
            self.draw_line(self.start_point[0], self.start_point[1],
                           end_point[0], end_point[1])
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
            self.animate_pixels(pixel_gen, color_func, delay=50)
        else:
            for p in pixel_gen:
                if self.current_algorithm == "Wu":
                    x, y, intensity = p
                    color = color_func(intensity)
                else:
                    x, y = p
                    color = color_func(None)
                draw_pixel(self.canvas, x, y, color)

    def animate_pixels(self, pixel_gen, color_func, delay):
        try:
            p = next(pixel_gen)
            if self.current_algorithm == "Wu":
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
    app = LineEditor(root, 1000, 700)
    root.mainloop()
