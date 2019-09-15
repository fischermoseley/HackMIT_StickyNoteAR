import pygame as pg
import time
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
        
        self.cv_data.append((0, 768, 2048, 5,"pink"))
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT),flags=pg.FULLSCREEN)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.xspawn = 0
        self.yspawn = 0
        self.win_state = False

    def read_cv_data(self):
        """Reads Fischer's beautiful data"""
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
#                print("Spawnplatform:" + SpawnSticky(*plat).rect.x)
                spawn_location.append(SpawnSticky(*plat).rect.x)
                spawn_location.append(SpawnSticky(*plat).rect.y)
            elif sticky_color == "pink":
                #If it's a death sticky, it belongs to a group reserved for death stickies.
                p = DieSticky(*plat)
                self.deathplatforms.add(p)
                
            self.all_sprites.add(p)
            
    def new(self):
        """Start a new game"""
        #Define groups and subgroups of platforms
        self.all_sprites = pg.sprite.Group()
        self.safeplatforms = pg.sprite.Group()
        self.spawnplatform = pg.sprite.GroupSingle()
        self.winplatform = pg.sprite.GroupSingle()
        self.deathplatforms = pg.sprite.Group()
        self.win_state = False
        self.read_cv_data()
        self.spawnplayer()
        self.run()

    def run(self):
        """Game Loop"""
        
        won = False
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            won = self.update()
            if won: #Checks for win condition
                self.events(True)
            self.events()
            self.draw()
        if not self.playing:
            pg.QUIT()

    def win_condition(self):
        self.message_display('You Win!')
        time.sleep(1.25)
        self.new()

    def update(self):
        """Game Loop - Update"""
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.win_state:
            self.message_display('You Win!')
            self.win_condition()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.safeplatforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
            if pg.sprite.spritecollide(self.player, self.winplatform, False):
                self.win_state = True
            dead = pg.sprite.spritecollide(self.player, self.deathplatforms, False) #Checks for collision with death platform
            if dead:
                self.player.kill()
                self.player.remove()
                sleep(0.5)
                self.spawnplayer()
        return False
        
    def spawnplayer(self):
        """Spawn in Player at spawn sticky"""
        self.player = Player(self, spawn_location[0], spawn_location[1])
        self.all_sprites.add(self.player)
        self.player.vel = vec(0, 0)
        self.player.acc = vec(0, 0)

    def resticky(self):
        print("restickying!")
        self.new()

        #extraneous for now
        delay = 250 # 500ms = 0.5s

        current_time = pg.time.get_ticks()
        change_time = current_time + delay
        show = True


    def events(self, won=False):
        """Game Loop - events"""
        for event in pg.event.get():
            # check for closing window
            if won:
                print("won!")
                while not pg.K_BACKSPACE:
                    pass
                
                self.new()
#            if event.type == pg.QUIT:
#                if self.playing:
#                    self.playing = False
#                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.key == pg.K_SPACE:
                    self.player.jump()
                if event.key == pg.K_u:
                    self.resticky()

                    
    def text_objects(self, text, font):
        textSurface = font.render(text, True, WHITE)
        return textSurface, textSurface.get_rect()
    
    def message_display(self, text):
        largeText = pg.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = ((WIDTH/2),(HEIGHT/2))
        self.screen.blit(TextSurf, TextRect)
        pg.display.update()
        self.events(True)

    def draw(self):
        """Game Loop - draw"""
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        """game splash/start screen"""
        pass

    def show_go_screen(self):
        """game over/continue"""
        pass

