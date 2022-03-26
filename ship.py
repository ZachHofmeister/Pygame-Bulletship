import pygame as pg
from vector import Vector
from timer import Timer
from pygame.sprite import Sprite, Group
from laser import Laser, Lasers
from copy import copy


class Ship(Sprite):
    exploding_images = [pg.transform.scale(pg.image.load(f'images/explode{n}.png'), (48, 48)) for n in range(8)]
    images = [pg.transform.scale(pg.image.load(f'images/ship.png'), (48, 48)) for n in range(1)]

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.alien_fleet = None
        self.lasers = None
        self.stats = game.stats
        self.sound = game.sound

        self.exploding_timer = Timer(image_list=Ship.exploding_images, delay=200, is_loop=False)
        self.normal_timer = Timer(image_list=Ship.images, delay=1000, is_loop=True)
        self.timer = self.normal_timer
        self.dying = False

        self.image = self.timer.image()

        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.center_bottom()
        self.v = Vector()

        self.burst_count = 3
        self.burst_remain = 0
        self.burst_frame_delay = 8
        self.burst_frame_counter = 0

    def set_alien_fleet(self, alien_fleet):
        self.alien_fleet = alien_fleet

    def set_lasers(self, lasers):
        self.lasers = lasers

    def center_bottom(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = Vector(self.rect.centerx, self.rect.centery)

    def reset_timer(self):
        self.exploding_timer.reset()
        self.normal_timer.reset()
        self.timer = self.normal_timer

    def hit(self):
        self.sound.play_ship_explosion()
        self.timer = self.exploding_timer
        self.dying = True

    def is_dying(self):
        return self.dying

    def die(self):
        self.stats.ship_hit()
        if self.stats.ships_left == 0:
            self.game.finished = True
        self.dying = False
        self.game.restart()

    def moving(self, vector):
        self.v = vector

    def inc_add(self, other):
        self.v += other

    def clamp(self):
        rw, rh = self.rect.width, self.rect.height
        srw, srb = self.screen_rect.width, self.screen_rect.bottom
        x, y = self.center.x, self.center.y

        self.center.x = min(max(x, rw / 2), srw - rw / 2)
        self.center.y = min(max(y, rh / 2), srb - rh / 2)

    def update(self):
        if self.dying and self.timer.is_expired():
            self.die()
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
        image = self.timer.image()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
        # self.screen.blit(self.image, self.rect)
        # pg.draw.rect(self.screen, Game.RED, self.rect, 1)

    def fire(self):
        laser = Laser(self.game, copy(self.center), direct=Vector(0, -1), color=self.settings.ship_laser_color)
        self.game.ship_lasers.add(laser)
