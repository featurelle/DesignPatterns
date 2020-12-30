from __future__ import annotations
import sys
import time
import random

import pygame
from pygame.rect import Rect


class GraphicsType:

    # Не храню размеры в своем Легковесе, потому что в Пайтоне небольшие int - уже легковесы (как и строки)
    # Например x = 5 \ y = 5 \ print(x is y) выведет True
    def __init__(self, img_path: str):
        self.img = pygame.image.load(img_path)

    def size(self):
        return self.img.get_size()

    def draw(self, screen, canvas: Rect):
        screen.blit(self.img, canvas)


class Graphics:

    def __init__(self, type: GraphicsType, canvas: Rect, speed_x: int, speed_y: int):
        self.type = type
        self.canvas = canvas
        self.speed_x = speed_x
        self.speed_y = speed_y

    def draw(self, screen):
        self.type.draw(screen, self.canvas)

    def move(self):
        self.canvas = self.canvas.move(self.speed_x, self.speed_y)

    @property
    def left(self):
        return self.canvas.left

    @property
    def right(self):
        return self.canvas.right

    @property
    def top(self):
        return self.canvas.top

    @property
    def bottom(self):
        return self.canvas.bottom


class GraphicsFactory:

    __particles = dict()

    @classmethod
    def get_template(cls, img_path: str):
        if img_path not in cls.__particles:
            cls.__particles[img_path] = GraphicsType(img_path)
        return cls.__particles[img_path]


class Game:

    IMG_ADDRESSES = 'img/green.png', 'img/blue.png', 'img/rose.png'

    def __init__(self, particles_amount: int):

        self.particles_amount = particles_amount
        self.particles: set[Graphics] = set()
        self.size = self.width, self.height = 1600, 900
        self.screen = None
        self.black = 0, 0, 0

    def load(self):

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        for _ in range(self.particles_amount):
            self.create_particle()

    def create_particle(self):

        random.seed(random.randint(-9999999999, 9999999999))

        img_path = random.choice(self.__class__.IMG_ADDRESSES)
        type = GraphicsFactory.get_template(img_path)

        x = random.randint(50, self.width - 50)
        y = random.randint(50, self.height - 50)
        canvas = Rect(x, y, *type.size())

        speed = []

        for _ in range(2):
            abs_speed = random.randint(1, 9)
            speed.append(random.choice([-abs_speed, abs_speed]))

        self.particles.add(Graphics(type, canvas, *speed))

    def move(self):

        for particle in self.particles:
            particle.move()
            if particle.left < 0 or particle.right > self.width:
                particle.speed_x = -particle.speed_x
            if particle.top < 0 or particle.bottom > self.height:
                particle.speed_y = -particle.speed_y

    def draw(self):

        for particle in self.particles:
            particle.draw(self.screen)
        pygame.display.flip()

    def play(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill(self.black)
            self.move()
            self.draw()
            time.sleep(0.005)


def demo():

    print('Every picture consumes ~1.8 kb on average,\n'
          'So if we weren\'t using Flyweight, a thousand particles would be consuming about 1.8 MB of memory.\n'
          'But instead we have that the difference between 1 and 1000 particles is at most 100 kb - 18 times cheaper!')
    game = Game(1000)
    game.load()
    game.play()


if __name__ == "__main__":
    demo()
