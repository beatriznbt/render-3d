import pygame
import os
import math
from render import matrix_multiplication

os.environ["SDL_VIDEO_CENTERED"] = '1'
width, height = 1920, 1080
black, white, blue = (20, 20, 20), (230, 230, 230), (0, 154, 255)

pygame.init()
pygame.display.set_caption("3D cube interactive rotation")
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 60

angleX, angleY = 0, 0
auto_rotate_speed = 0.01  
cube_position = [width // 2, height // 2]
scale = 600

points = [n for n in range(8)]
points[0] = [[-1], [-1], [1]]
points[1] = [[1], [-1], [1]]
points[2] = [[1], [1], [1]]
points[3] = [[-1], [1], [1]]
points[4] = [[-1], [-1], [-1]]
points[5] = [[1], [-1], [-1]]
points[6] = [[1], [1], [-1]]
points[7] = [[-1], [1], [-1]]

def connect_point(i, j, k):
    a = k[i]
    b = k[j]
    pygame.draw.line(screen, black, (a[0], a[1]), (b[0], b[1]), 4)

is_rotating = False
last_mouse_x, last_mouse_y = 0, 0
projected_points = []

run = True
while run:
    clock.tick(fps)
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  
                run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            is_rotating = True
            last_mouse_x, last_mouse_y = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            is_rotating = False
        elif event.type == pygame.MOUSEMOTION and is_rotating:
            mx, my = event.pos
            angleX += (my - last_mouse_y) * 0.005
            angleY += (mx - last_mouse_x) * 0.005
            last_mouse_x, last_mouse_y = mx, my

    angleY += auto_rotate_speed  

    projected_points = []
    rotation_x = [[1, 0, 0],
                  [0, math.cos(angleX), -math.sin(angleX)],
                  [0, math.sin(angleX), math.cos(angleX)]]

    rotation_y = [[math.cos(angleY), 0, math.sin(angleY)],
                  [0, 1, 0],
                  [-math.sin(angleY), 0, math.cos(angleY)]]

    rotation_z = [[math.cos(angleY), -math.sin(angleY), 0],
                  [math.sin(angleY), math.cos(angleY), 0],
                  [0, 0, 1]]
    
    for point in points:
        rotated_2d = matrix_multiplication(rotation_y, point)
        rotated_2d = matrix_multiplication(rotation_x, rotated_2d)
        rotated_2d = matrix_multiplication(rotation_z, rotated_2d)

        distance = 5
        z = 1/(distance - rotated_2d[2][0])
        projection_matrix = [[z, 0, 0],
                             [0, z, 0]]
        projected2d = matrix_multiplication(projection_matrix, rotated_2d)
        x = int(projected2d[0][0] * scale) + cube_position[0]
        y = int(projected2d[1][0] * scale) + cube_position[1]

        projected_points.append([x, y])
        pygame.draw.circle(screen, blue, (x, y), 10)

    for m in range(4):
        connect_point(m, (m+1)%4, projected_points)
        connect_point(m+4, (m+1)%4+4, projected_points)
        connect_point(m, m+4, projected_points)

    pygame.display.update()

pygame.quit()
