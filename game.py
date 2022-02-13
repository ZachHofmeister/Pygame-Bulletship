import pygame as pg
import sys
import game_functions as gf
from vector import Vector
from pygame.sprite import Sprite, Group
from copy import copy
import random


class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (150, 150, 150)

        self.ship_speed_factor = 3

        self.laser_speed_factor = 1
        self.laser_width = 3
        self.laser_height = 15
        self.laser_color = 255, 0, 0


class Alien:
    def __init__(self): pass
    def update(self): pass
    def draw(self): pass


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


class Ship:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.image = pg.image.load('images/ship.bmp')

        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = Vector(self.rect.centerx, self.rect.centery)

        self.v = Vector()

        self.burst_count = 3
        self.burst_remain = 0
        self.burst_frame_delay = 20
        self.burst_frame_counter = 0
        self.aimcone = 0.1

    def moving(self, vector): self.v = vector
    def inc_add(self, other): self.v += other

    def clamp(self):
        rw, rh = self.rect.width, self.rect.height
        srw, srb = self.screen_rect.width, self.screen_rect.bottom
        x, y = self.center.x, self.center.y

        self.center.x = min(max(x, rw/2), srw - rw/2)
        self.center.y = min(max(y, rh/2), srb - rh/2)

    def update(self):
        self.center += self.v * self.settings.ship_speed_factor
        self.clamp()
        self.rect.centerx, self.rect.centery = self.center.x, self.center.y

        if self.burst_remain > 0:
            if self.burst_frame_counter == 0:
                self.fire()
                self.burst_remain -= 1
            # increment the burst frame count
            self.burst_frame_counter += 1
            self.burst_frame_counter %= self.burst_frame_delay

    def draw(self):
        self.screen.blit(self.image, self.rect)
        pg.draw.rect(self.screen, Game.RED, self.rect, 1)

    def fire(self):
        laser = Laser(self.game, random.uniform(-self.aimcone, self.aimcone))
        self.game.lasers.add(laser)

class Game:
    RED = (255, 0, 0)

    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))
        self.bg_color = self.settings.bg_color
        pg.display.set_caption("Alien Invasion")
        self.ship = Ship(game=self)
        self.lasers = Group()

    def update(self):
        self.ship.update()
        self.lasers.update()
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0: self.lasers.remove(laser)
        print(len(self.lasers))

    def draw(self):
        self.screen.fill(self.bg_color)
        self.ship.draw()
        for laser in self.lasers.sprites():
            laser.draw()
        pg.display.flip()

    def play(self):
        finished = False
        while not finished:
            self.update()
            self.draw()
            gf.check_events(game=self)   # exits game if QUIT pressed


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
