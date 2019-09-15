import pygame as pg 
import thorpy
from StickyJump import *
from launch_game import *
from settings import *

pg.init()
pg.key.set_repeat(300, 30)
screen = pg.display.set_mode((WIDTH,HEIGHT))
screen.fill((255,255,255))

rect = pg.Rect((0, 0, 50, 50))
rect.center = screen.get_rect().center
clock = pg.time.Clock()

pg.draw.rect(screen, (255,0,0), rect)
pg.display.flip()

#THORPY ELEMENTS
quit_button = thorpy.make_button("Quit", func=thorpy.functions.quit_func)
sticky_jump_button = thorpy.make_button("StickyJump", func=launch_game) # < -- eventually abstract more
calibrate_button = thorpy.make_button("Calibrate", func=print("calibrating")) # <-- zach add calibration here

box = thorpy.Box(elements=[sticky_jump_button,calibrate_button,quit_button])

#we regroup all elements on a menu, even if we do not launch the menu
menu = thorpy.Menu(box)
#important : set the screen as surface for all elements
for element in menu.get_population():
    element.surface = screen

#use the elements normally...
box.set_topleft((WIDTH // 2, HEIGHT // 2))
box.blit()
box.update()

playing_game = True
while playing_game:
    clock.tick(1)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing_game = False
            break
        menu.react(event) #the menu automatically integrate your elements

pg.quit()