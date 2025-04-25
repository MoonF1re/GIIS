import pygame
import sys
from geometry.polygon import Polygon
from geometry.convex_hull import graham_scan, jarvis_march
from graphics.lines import draw_line_dda, draw_line_bresenham, draw_line_wu
from ui.menu import Menu


def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Polygon Editor")
    clock = pygame.time.Clock()

    polygon = Polygon()
    menu = Menu(["Draw", "Graham", "Jarvis", "Normals"])      # кнопки
    mode = "Draw"
    line_algo = "Bresenham"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu.handle_click(event.pos):
                    mode = menu.get_mode()
                else:
                    if mode == "Draw":
                        polygon.add_point(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    polygon.close()
                elif event.key == pygame.K_c:
                    polygon.clear()
                elif event.key == pygame.K_n:
                    polygon.calculate_normals()
                elif event.key == pygame.K_h:
                    pts = polygon.points
                    if mode == "Graham":
                        hull = graham_scan(pts)
                        polygon.set_points(hull)
                    elif mode == "Jarvis":
                        hull = jarvis_march(pts)
                        polygon.set_points(hull)
                elif event.key == pygame.K_1:
                    line_algo = "DDA"
                elif event.key == pygame.K_2:
                    line_algo = "Bresenham"
                elif event.key == pygame.K_3:
                    line_algo = "Wu"

        screen.fill((255, 255, 255))
        menu.draw(screen)
        # отрисовка полигона с выбранным алгоритмом
        if line_algo == "DDA":
            polygon.draw(screen, draw_line_dda)
        elif line_algo == "Bresenham":
            polygon.draw(screen, draw_line_bresenham)
        else:
            polygon.draw(screen, draw_line_wu)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()