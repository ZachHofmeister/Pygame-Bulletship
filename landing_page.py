import pygame as pg
import sys
from alien import AlienFleet, Alien
from vector import Vector
from settings import Settings
from button import Button

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (130, 130, 130)
YELLOW = (250, 250, 0)


class LandingPage:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.landing_page_finished = False

        heading_font = pg.font.SysFont(None, 192)
        subheading_font = pg.font.SysFont(None, 122)
        font = pg.font.SysFont(None, 48)

        strings = [('STAR', YELLOW, heading_font), ('INVADERS', YELLOW, subheading_font),
                ('= 10 PTS', GREY, font), ('= 20 PTS', GREY, font),
                            ('= 40 PTS', GREY, font), ('= ???', GREY, font),
                ('', YELLOW, font), ('', GREY, font)]

        self.texts = [self.get_text(msg=s[0], color=s[1], font=s[2]) for s in strings]

        self.posns = [150, 230]
        alien = [60 * x + 400 for x in range(4)]
        play_high = [x for x in range(650, 760, 80)]
        self.posns.extend(alien)
        self.posns.extend(play_high)
        self.aliens = [
            Alien(self.game, AlienFleet.alien1_images, ul=(450, alien[0] - 24), v=Vector(0, 0)),
            Alien(self.game, AlienFleet.alien2_images, ul=(450, alien[1] - 24), v=Vector(0, 0)),
            Alien(self.game, AlienFleet.alien3_images, ul=(450, alien[2] - 24), v=Vector(0, 0)),
            Alien(self.game, AlienFleet.alien4_images, ul=(450, alien[3] - 24), v=Vector(0, 0))
        ]

        centerx = self.screen.get_rect().centerx
        n = len(self.texts)
        self.rects = [self.get_text_rect(text=self.texts[i], centerx=centerx, centery=self.posns[i]) for i in range(n)]
        self.buttons = [Button(self.screen, self.rects[-2], message='Play Game', action=self.play),
                        Button(self.screen, self.rects[-1], message='High Scores', action=self.show_high_scores)]

    def get_text(self, font, msg, color): return font.render(msg, True, color, BLACK)

    def get_text_rect(self, text, centerx, centery):
        rect = text.get_rect()
        rect.centerx = centerx
        rect.centery = centery
        return rect

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()
            elif e.type == pg.KEYUP and e.key == pg.K_p:   # pretend PLAY BUTTON pressed
                self.landing_page_finished = True        # TODO change to actual PLAY button
                                                         # SEE ch. 14 of Crash Course for button
            elif e.type == pg.MOUSEBUTTONDOWN:  # Mouse pressed
                for button in self.buttons:
                    if button.is_hovering():
                        button.action()

    def update(self):       # TODO make aliens move
        for alien in self.aliens:
            alien.update()
        for button in self.buttons:
            button.update()

    def show(self):
        while not self.landing_page_finished:
            self.update()
            self.draw()
            self.check_events()   # exits game if QUIT pressed

    def draw_text(self):
        n = len(self.texts)
        for i in range(n):
            self.screen.blit(self.texts[i], self.rects[i])

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_text()
        for alien in self.aliens:
            alien.draw()
        for button in self.buttons:
            button.draw()
        # self.alien_fleet.draw()   # TODO draw my aliens
        # self.lasers.draw()        # TODO dray my button and handle mouse events
        pg.display.flip()

    def play(self):
        self.landing_page_finished = True

    def show_high_scores(self):
        pass
