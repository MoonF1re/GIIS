# Коэффициент размера пикселей
PIXEL_SIZE = 10

def draw_pixel(canvas, x, y, color="black"):
    canvas.create_rectangle(x * PIXEL_SIZE, y * PIXEL_SIZE,
                            (x + 1) * PIXEL_SIZE, (y + 1) * PIXEL_SIZE,
                            outline=color, fill=color)

def draw_grid(canvas):
    w = int(canvas['width'])*3
    h = int(canvas['height'])*3
    for x in range(0, w, PIXEL_SIZE):
        canvas.create_line(x, 0, x, h, fill='lightgray')
    for y in range(0, h, PIXEL_SIZE):
        canvas.create_line(0, y, w, y, fill='lightgray')

def intensity_to_color(intensity):
    value = int(255 * (1 - intensity))
    return f"#{value:02x}{value:02x}{value:02x}"
