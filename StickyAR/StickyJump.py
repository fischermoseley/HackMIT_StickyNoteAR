import pygame as pg
import random
from settings import *
# from stickys import updateSticky, clearSticky, calibrate, uncalibrate

from sprites import *
from time import sleep

spawn_location = []

DEFAULT_CV = [(150,200,50,50,"blue"), (275,200,50,50,"orange"), (375,200,50,50,"green"), (450,200,50,50,"pink")]
class StickyJump:
    def __init__(self, cv_data):
        if cv_data is None:
            self.cv_data = DEFAULT_CV
        else:
            self.cv_data = cv_data
            
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), flags=pg.FULLSCREEN)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.xspawn = 0
        self.yspawn = 0

    def read_cv_data(self):
        print(self.cv_data)
        for sticky in self.cv_data:
            plat = sticky[:-1]
            print("PLAT")
            print(*plat)

            sticky_color = sticky[-1]
            if sticky_color == "green":
                p = WinSticky(*plat)
                self.safeplatforms.add(p)
                self.winplatform.add(p)
            elif sticky_color == "blue":
                p = WalkSticky(*plat)
                self.safeplatforms.add(p)
            elif sticky_color == "orange":
                p = SpawnSticky(*plat)
                self.safeplatforms.add(p)
                self.spawnplatform.add(p)
                spawn_location.append(p.rect.x)
                spawn_location.append(p.rect.y)
            elif sticky_color == "pink":
                p = DieSticky(*plat)
                self.deathplatforms.add(p)

            self.all_sprites.add(p)

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.safeplatforms = pg.sprite.Group()
        self.spawnplatform = pg.sprite.GroupSingle()
        self.winplatform = pg.sprite.GroupSingle()
        self.deathplatforms = pg.sprite.Group()

        self.read_cv_data()
        self.spawnplayer()
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        if not self.playing:
            pg.QUIT()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.safeplatforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
            dead = pg.sprite.spritecollide(self.player, self.deathplatforms, False)
            if dead:
                self.player.kill()
                self.player.remove()
                sleep(0.5)
                self.spawnplayer()
    
    def spawnplayer(self):
        # Spawn in player at spawn sticky
        self.player = Player(self, spawn_location[0], spawn_location[1])
        self.all_sprites.add(self.player)

    def resticky(self):
        print("restickying!")
        self.new()

        #extraneous for now
        delay = 250 # 500ms = 0.5s

        current_time = pg.time.get_ticks()
        change_time = current_time + delay
        show = True


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
                if event.key == pg.K_u:
                    self.resticky()



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

