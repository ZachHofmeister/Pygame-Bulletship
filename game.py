import pygame as pg
import game_functions as gf
from ship import Ship
from settings import Settings
from stats import Stats
from alien import AlienFleet
from laser import Lasers
from sys import exit
from time import sleep
from scoreboard import Scoreboard
from sound import Sound


class Game:
    RED = (255, 0, 0)

    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.stats = Stats(game=self)
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))
        self.sound = Sound()
        self.bg_color = self.settings.bg_color
        pg.display.set_caption("Star Invaders")

        self.sb = Scoreboard(game=self)
        self.ship = Ship(game=self)
        self.alien_fleet = AlienFleet(game=self)
        self.ship_lasers = Lasers(game=self)
        self.alien_lasers = Lasers(game=self)
        self.ship.set_alien_fleet(self.alien_fleet)
        self.ship.set_lasers(self.ship_lasers)
        self.finished = False

    def restart(self):
        if self.stats.ships_left == 0:
            self.game_over()
        print("restarting game")
        self.ship_lasers.empty()
        self.alien_lasers.empty()
        self.alien_fleet.empty()
        self.alien_fleet.create_fleet()
        self.ship.center_bottom()
        self.ship.reset_timer()
        self.update()
        self.draw()
        sleep(0.5)

    def update(self):
        self.ship.update()
        self.alien_fleet.update()
        self.ship_lasers.update()
        self.alien_lasers.update()
        self.sb.update()

    def draw(self):
        self.screen.fill(self.bg_color)
        self.ship.draw()
        self.alien_fleet.draw()
        self.ship_lasers.draw()
        self.alien_lasers.draw()
        self.sb.draw()
        pg.display.flip()

    def play(self):
        self.finished = False
        self.sound.play_bg()
        while not self.finished:
            self.update()
            self.draw()
            gf.check_events(game=self)   # exits game if QUIT pressed
        self.game_over()

    def game_over(self):
        self.sound.play_game_over()
        print('\nGAME OVER!\n\n')
        exit()    # can ask to replay here instead of exiting the game
