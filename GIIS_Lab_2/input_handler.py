import pygame
import numpy as np
from transform import *

def handle_input(obj, keys, angle_step=0.05, move_step=10, scale_step=0.1):
    #keys: Массив Клавиш которые мы нажимаем
    M = np.eye(4)
    # Перемещение
    if keys[pygame.K_LEFT]:   M = translation_matrix(-move_step, 0, 0).dot(M)
    if keys[pygame.K_RIGHT]:  M = translation_matrix(move_step, 0, 0).dot(M)
    if keys[pygame.K_UP]:     M = translation_matrix(0, move_step, 0).dot(M)
    if keys[pygame.K_DOWN]:   M = translation_matrix(0, -move_step, 0).dot(M)
    # Повороты
    if keys[pygame.K_q]:      M = rotation_matrix_x(angle_step).dot(M)
    if keys[pygame.K_w]:      M = rotation_matrix_y(angle_step).dot(M)
    if keys[pygame.K_e]:      M = rotation_matrix_z(angle_step).dot(M)
    # Масштабирование
    if keys[pygame.K_a]:      M = scaling_matrix(1 + scale_step, 1 + scale_step, 1 + scale_step).dot(M)
    if keys[pygame.K_s]:      M = scaling_matrix(1 - scale_step, 1 - scale_step, 1 - scale_step).dot(M)
    # Отражение по плоскости XY
    if keys[pygame.K_r]:      M = reflection_matrix('xy').dot(M)
    obj.transform(M)