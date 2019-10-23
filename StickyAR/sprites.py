"""
Sprite classes for StickyJump platformer game
Proprietary content of StickyAR, 2019
Brought to you by Luke Igel, Fischer Moseley, Tim Gutterman, and Zach Rolfness
"""
import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, spawnx, spawny):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        
        # Place player sprite above the spawn platform with initial velocity (0, 0)
        self.rect.center = (spawnx + 25, spawny - 100)
        self.pos = vec(spawnx + 25, spawny - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        """Jump method called by 'Events' phase of master game loop when spacebar pressed"""
        # Jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.safeplatforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20

    def update(self):
        """Handles player movement in x- and y-directions"""
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # Apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        
        # Equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        # Wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos
                
class Platform(pg.sprite.Sprite):
    """Superclass for all game platform sprites"""
    def __init__(self, x, y, w, h, debug_mode=False):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""Different flavors of sticky note platforms"""
class WalkSticky(Platform):
    def __init__(self, x, y, w, h,debug_mode=False):
        Platform.__init__(self, x, y, w, h)
        if debug_mode:
            self.image.fill(BLUE)

class SpawnSticky(Platform):
    def __init__(self, x, y, w, h,debug_mode=False):
        Platform.__init__(self, x, y, w, h)
        if debug_mode:
            self.image.fill(ORANGE)

class DieSticky(Platform):
    def __init__(self, x, y, w, h, debug_mode=False):
        Platform.__init__(self, x, y, w, h)
        if debug_mode:
            self.image.fill(PINK)
        
class WinSticky(Platform):
    def __init__(self, x, y, w, h, debug_mode=False):
        Platform.__init__(self, x, y, w, h)
        if debug_mode:
            self.image.fill(GREEN)