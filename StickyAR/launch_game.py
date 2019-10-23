from StickyJump import *
from settings import *
from sprites import *

def launch_game(cv_data=None, debug_mode=False):
    print("launching game")
    g = StickyJump(cv_data, debug_mode)
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_go_screen()

if __name__ == "__main__":
    launch_game()