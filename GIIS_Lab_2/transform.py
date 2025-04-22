import numpy as np

def translation_matrix(dx, dy, dz):
    M = np.eye(4)
    M[0, 3] = dx
    M[1, 3] = dy
    M[2, 3] = dz
    return M


def scaling_matrix(sx, sy, sz):
    M = np.eye(4)
    M[0, 0] = sx
    M[1, 1] = sy
    M[2, 2] = sz
    return M


def rotation_matrix_x(angle):
    M = np.eye(4)
    c, s = np.cos(angle), np.sin(angle)
    M[1, 1] = c
    M[1, 2] = -s
    M[2, 1] = s
    M[2, 2] = c
    return M


def rotation_matrix_y(angle):
    M = np.eye(4)
    c, s = np.cos(angle), np.sin(angle)
    M[0, 0] = c
    M[0, 2] = s
    M[2, 0] = -s
    M[2, 2] = c
    return M


def rotation_matrix_z(angle):
    M = np.eye(4)
    c, s = np.cos(angle), np.sin(angle)
    M[0, 0] = c
    M[0, 1] = -s
    M[1, 0] = s
    M[1, 1] = c
    return M


def reflection_matrix(axis):
    M = np.eye(4)
    if axis == 'xy':
        M[2, 2] = -1
    elif axis == 'yz':
        M[0, 0] = -1
    elif axis == 'xz':
        M[1, 1] = -1
    return M


def apply_transform(vertices, M):
    return [M.dot(v) for v in vertices]