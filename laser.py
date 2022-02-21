import pygame as pg
from vector import Vector
from pygame.sprite import Sprite, Group
from copy import copy

class Lasers:
    def __init__(self, game):
        self.game = game
        self.alien_fleet = game.alien_fleet
        self.lasers = Group()

    def add(self, laser): self.lasers.add(laser)
    def empty(self): self.lasers.empty()
    def update(self):
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0: self.lasers.remove(laser)

        collisions = pg.sprite.groupcollide(self.lasers,
                                            self.alien_fleet.fleet,
                                            True, True)
        if self.alien_fleet.length() == 0:  pass    # TODO

        for laser in self.lasers:
            laser.update()

    def draw(self):
        for laser in self.lasers:
            laser.draw()

class Laser(Sprite):
    def __init__(self, game, aimcone=0):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.w, self.h = self.settings.laser_width, self.settings.laser_height
        self.ship = game.ship

        self.rect = pg.Rect(0, 0, self.w, self.h)
        self.center = copy(self.ship.center)
        print(f'center is at {self.center}')
        self.color = self.settings.laser_color
        self.v = Vector(aimcone, -1) * self.settings.laser_speed_factor

    def update(self):
        self.center += self.v
        self.rect.x, self.rect.y = self.center.x, self.center.y

    def draw(self): pg.draw.rect(self.screen, self.color, self.rect)