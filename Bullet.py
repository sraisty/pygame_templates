import pygame as pg


class Bullet:
    def __init__(self, position, heading):
        self.position = pg.Vector2(position)
        self.direction = pg.Vector2(1, 0).rotate(-heading)
        self.speed = 700

    def update(self, dt):
        self.position += self.direction() * self.speed * dt
