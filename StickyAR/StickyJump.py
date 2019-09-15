import pygame as pg
import random
from settings import *
from sprites import *

DEFAULT_CV = [(150,200,50,50,"blue"), (275,200,50,50,"orange"), (375,200,50,50,"green"), (450,200,50,50,"pink")]
class StickyJump:
    def __init__(self, cv_data):
        if cv_data is None:
            self.cv_data = DEFAULT_CV
        else:
            self.cv_ddata = cv_data
            
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.platform_list = []
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def read_cv_data(self):
        print(self.cv_data)
        for sticky in self.cv_data:
            plat = sticky[:-1]
            print("PLAT")
            print(*plat)

            sticky_color = sticky[-1]
            if sticky_color == "green":
                p = WinSticky(*plat)
            elif sticky_color == "blue":
                p = WalkSticky(*plat)
            elif sticky_color == "pink":
                p = DieSticky(*plat)
            elif sticky_color == "orange":
                p = SpawnSticky(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p) 

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.read_cv_data()
        # for plat in PLATFORM_LIST:
        #     p = Platform(*plat)
        #     self.all_sprites.add(p)
        #     self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

