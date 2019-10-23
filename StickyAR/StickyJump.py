"""
Flagship file for the StickyJump platformer game
Proprietary content of StickyAR, 2019
Brought to you by Luke Igel, Fischer Moseley, Tim Gutterman, and Zach Rolfness
"""
import pygame as pg
import time
import random
from settings import *
from stickys import updateSticky, clearSticky, calibrate, uncalibrate

from sprites import *
from time import sleep

# Default data seeds a guaranteed game world in absence of CV data
DEFAULT_CV = [(150,200,50,50,"blue"), (275,200,50,50,"orange"), (375,200,50,50,"green"), (450,200,50,50,"pink")]

class StickyJump:
    def __init__(self, cv_data, debug_mode):
        self.debug_mode = debug_mode
        # Check if CV data pipeline is operational, and use default data if not
        if cv_data is None:
            self.cv_data = DEFAULT_CV
        else:
            self.cv_data = cv_data
        # Add the invisible killing floor to bottom of game window
        self.cv_data.append((0, 768, 2048, 5,"pink"))
        
        # Initialize game window
        pg.init()
        pg.mixer.init()
        if debug_mode:
            self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        else:
            self.screen = pg.display.set_mode((WIDTH, HEIGHT),flags=pg.FULLSCREEN)
        pg.display.set_caption(TITLE)
        
        #Basic procedural game settings
        self.clock = pg.time.Clock()
        self.running = True
        self.xspawn = 0
        self.yspawn = 0
        self.win_state = False

    def read_cv_data(self):
        """Reads incoming CV data from the projected visual field and adds colored platforms as game sprites"""
        print(self.cv_data)
        
        for sticky in self.cv_data:
            # Get the sticky note's (x, y) position, width, and height, respectively
            plat = sticky[:-1]
            print("PLAT")
            print(*plat)

            sticky_color = sticky[-1]
            # Different types of platforms correspond to different sticky note colors
            if sticky_color == "green":
                p = WinSticky(debug_mode=self.debug_mode,*plat)
                self.safeplatforms.add(p)
                self.winplatform.add(p)
                
            elif sticky_color == "blue":
                p = WalkSticky(debug_mode=self.debug_mode,*plat)
                self.safeplatforms.add(p)
            
            # Orange sticky is the spawn platform; only expect one of these
            elif sticky_color == "orange":
                p = SpawnSticky(debug_mode=self.debug_mode,*plat)
                self.safeplatforms.add(p)
                self.spawnplatform.add(p)
                # Add spawn coords to overall StickyJump game settings
                self.xspawn = p.rect.x
                self.yspawn = p.rect.y
                
            elif sticky_color == "pink":
                # If it's a death sticky, it belongs to a group of platforms reserved for death stickies
                p = DieSticky(debug_mode=self.debug_mode,*plat)
                self.deathplatforms.add(p)
                
            self.all_sprites.add(p)
            
    def spawnplayer(self):
        """Spawn in Player at spawn sticky"""
        self.player = Player(self, self.xspawn, self.yspawn)
        self.all_sprites.add(self.player)
        
        # Player begins stationary in x direction
        self.player.vel = vec(0, 0)
        self.player.acc = vec(0, 0)
        
    def win_condition(self):
        #Displays win screen and then starts new game
        self.message_display('You Win!')
        time.sleep(1.25)
        self.new()
            
    def new(self, resticky=False):
        """Start a new game"""
        if resticky:
            print("attempting to resticky")
            self.cv_data = updateSticky()
            print(self.cv_data)
            
        # Define groups and subgroups of platforms
        self.all_sprites = pg.sprite.Group()
        self.safeplatforms = pg.sprite.Group()
        self.spawnplatform = pg.sprite.GroupSingle()
        self.winplatform = pg.sprite.GroupSingle()
        self.deathplatforms = pg.sprite.Group()
        
        #Fill out groups of platforms using CV data
        self.read_cv_data()
        
        #Spawn player and enter master game loop
        self.spawnplayer()
        self.win_state = False
        self.run()

    def run(self):
        """Master Game Loop"""
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            # Update player's position and handle collisions with platforms
            self.update()
            # Checks for keystrokes that alter player or game state
            self.events() 
            # Redraws game in window accordingly
            self.draw() 
        
        if not self.playing:
            pg.QUIT()

    def update(self):
        """Game Loop - Update"""
        # Updates Player sprite directly, allowing for movement along x-axis and falling along y-axis
        self.all_sprites.update()

        if self.win_state:
            self.win_condition()
        
        # Handles when player falls and collides with different types of platforms
        if self.player.vel.y > 0:
            
            # Falling collision with safe (orange, blue, green) platform
            hits = pg.sprite.spritecollide(self.player, self.safeplatforms, False)
            if hits:
                # Kill player's velocity at point of collision
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                
            # Handles win sequence if player falls onto win (green) platform
            wins = pg.sprite.spritecollide(self.player, self.winplatform, False)
            if wins:
                self.win_state = True
                
            # If collision with death (pink) platform, kill player and then respawn
            dead = pg.sprite.spritecollide(self.player, self.deathplatforms, False) #Checks for collision with death platform
            if dead:
                self.player.kill()
                self.player.remove()
                sleep(0.5)
                self.spawnplayer()

    def events(self):
        """Game Loop - Keystroke Events"""
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                
                # Escape key exits game
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False
                    
                # Spacebar mapped to jump
                if event.key == pg.K_SPACE:
                    self.player.jump()
                    
                # 'U' key means resticky and start new game
                if event.key == pg.K_u:
                    print("restickying")
                    self.resticky()
                    
    def draw(self):
        """Game Loop - Draw"""
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()
                    
    def resticky(self):
            """ **WORK IN PROGRESS**
                 Handles changes to sticky note layout and builds new game accordingly
            """
            print("restickying!")
            self.new(True)
    
            # Extraneous for now
            delay = 250 # 500ms = 0.5s
    
            current_time = pg.time.get_ticks()
            change_time = current_time + delay
            show = True
                    
    def text_objects(self, text, font):
        """Helper function for message_display"""
        textSurface = font.render(text, True, WHITE)
        return textSurface, textSurface.get_rect()
    
    def message_display(self, text):
        """Displays message in center of game window"""
        largeText = pg.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = ((WIDTH/2),(HEIGHT/2))
        self.screen.blit(TextSurf, TextRect)
        pg.display.update()

    def show_start_screen(self):
        """game splash/start screen"""
        pass

    def show_go_screen(self):
        """game over/continue"""
        pass

