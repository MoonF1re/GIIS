import pygame
import sys
from loader import load_object
from object3d import Object3D
from renderer import draw
from input_handler import handle_input


def main():
    # Инициализация Pygame
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # Загрузка модели
    vertices, edges = load_object('model.txt')
    obj = Object3D(vertices, edges)
    d = 500  # фокусное расстояние

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        handle_input(obj, keys)

        screen.fill((0, 0, 0))
        draw(screen, obj, width, height, d)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()