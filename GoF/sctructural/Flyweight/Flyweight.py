from colorama import Fore, Back, Style, init
import pygame
from pygame.rect import Rect
import sys
import time


class GraphicsType:

    def __init__(self, img_path: str):
        self.img = pygame.image.load(img_path)
        self.size = self.img.get_size()

    def draw(self, canvas: Rect, speed: list[float]):
        screen.blit(ball, canvas)


pygame.init()

size = width, height = 1600, 900
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)


ball = pygame.image.load("img/rose.png")
size = ball.get_size()
canvas = pygame.rect.Rect(800, 450, *size)
# canvas = ball.get_rect()
# canvas.x = 800
# canvas.y = 450
ball2 = pygame.image.load("img/blue.png")
canvas2 = pygame.rect.Rect(200, 200, *size)


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    canvas = canvas.move(speed)
    canvas2 = canvas2.move(speed)
    if canvas.left < 0 or canvas.right > width:
        speed[0] = -speed[0]
    if canvas.top < 0 or canvas.bottom > height:
        speed[1] = -speed[1]
    time.sleep(0.05)

    screen.fill(black)
    screen.blit(ball, canvas)
    screen.blit(ball, canvas2)
    pygame.display.flip()
