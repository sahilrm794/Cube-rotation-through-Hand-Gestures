# File to rotate the cube
import pygame
from math import *
import json

SCREEN_SIZE = 800
ROTATION_SPEED = 0.05
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
game_clock = pygame.time.Clock()

projection_matrix = [[1,0,0],
                     [0,1,0],
                     [0,0,0]]

cube_vertices = [n for n in range(8)]
cube_vertices[0] = [[-1], [-1], [1]]
cube_vertices[1] = [[1],[-1],[1]]
cube_vertices[2] = [[1],[1],[1]]
cube_vertices[3] = [[-1],[1],[1]]
cube_vertices[4] = [[-1],[-1],[-1]]
cube_vertices[5] = [[1],[-1],[-1]]
cube_vertices[6] = [[1],[1],[-1]]
cube_vertices[7] = [[-1],[1],[-1]]


def multiply_matrices(mat_a, mat_b):
    a_rows = len(mat_a)
    a_cols = len(mat_a[0])

    b_rows = len(mat_b)
    b_cols = len(mat_b[0])

    # Dot product matrix dimensions = a_rows x b_cols
    product_matrix = [[0 for _ in range(b_cols)] for _ in range(a_rows)]

    if a_cols == b_rows:
        for i in range(a_rows):
            for j in range(b_cols):
                for k in range(b_rows):
                    product_matrix[i][j] += mat_a[i][k] * mat_b[k][j]
    else:
        print("INCOMPATIBLE MATRIX SIZES")
    return product_matrix


def draw_line(i, j, points):
    pygame.draw.line(screen, (255, 255, 255), (points[i][0], points[i][1]), (points[j][0], points[j][1]))

# Main Loop
scale_factor = 100
x_angle = y_angle = z_angle = 0
while True:
    game_clock.tick(60)
    screen.fill((0, 0, 0))
    
    rotation_matrix_x = [[1, 0, 0],
                         [0, cos(x_angle), -sin(x_angle)],
                         [0, sin(x_angle), cos(x_angle)]]

    rotation_matrix_y = [[cos(y_angle), 0, sin(y_angle)],
                         [0, 1, 0],
                         [-sin(y_angle), 0, cos(y_angle)]]

    rotation_matrix_z = [[cos(z_angle), -sin(z_angle), 0],
                         [sin(z_angle), cos(z_angle), 0],
                         [0, 0, 1]]

    transformed_points = [0 for _ in range(len(cube_vertices))]
    idx = 0
    for vertex in cube_vertices:
        rotated_x = multiply_matrices(rotation_matrix_x, vertex)
        rotated_y = multiply_matrices(rotation_matrix_y, rotated_x)
        rotated_z = multiply_matrices(rotation_matrix_z, rotated_y)
        projected_2d = multiply_matrices(projection_matrix, rotated_z)
    
        x_pos = (projected_2d[0][0] * scale_factor) + SCREEN_SIZE / 2
        y_pos = (projected_2d[1][0] * scale_factor) + SCREEN_SIZE / 2

        transformed_points[idx] = (x_pos, y_pos)
        idx += 1

        rot_x = 0
        rot_y = 0
        try:
            with open("angle.json", "r") as file:
                data = json.load(file)
                rot_x = data["deviation_y"]
                rot_y = data["deviation_x"]
        except: pass

        x_angle += rot_x * 0.001
        y_angle += rot_y * 0.001

        pygame.draw.circle(screen, (255, 0, 0), (x_pos, y_pos), 5)

    draw_line(0, 1, transformed_points)
    draw_line(0, 3, transformed_points)
    draw_line(0, 4, transformed_points)
    draw_line(1, 2, transformed_points)
    draw_line(1, 5, transformed_points)
    draw_line(2, 6, transformed_points)
    draw_line(2, 3, transformed_points)
    draw_line(3, 7, transformed_points)
    draw_line(4, 5, transformed_points)
    draw_line(4, 7, transformed_points)
    draw_line(6, 5, transformed_points)
    draw_line(6, 7, transformed_points)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # Retrieving x_angle and y_angle from the JSON file
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            x_angle = y_angle = z_angle = 0
        if keys[pygame.K_a]:
            y_angle += ROTATION_SPEED
        if keys[pygame.K_d]:
            y_angle -= ROTATION_SPEED
        if keys[pygame.K_w]:
            x_angle += ROTATION_SPEED
        if keys[pygame.K_s]:
            x_angle -= ROTATION_SPEED
        if keys[pygame.K_q]:
            z_angle -= ROTATION_SPEED
        if keys[pygame.K_e]:
            z_angle += ROTATION_SPEED

    pygame.display.update()
