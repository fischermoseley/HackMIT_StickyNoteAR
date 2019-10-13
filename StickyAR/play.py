from cmd import Cmd
from stickys import updateSticky, clearSticky, calibrate, uncalibrate
from launch_game import launch_game


class MyPrompt(Cmd):
    prompt = 'sticky_server> '
    intro = "Welcome to StickyAR! Type H to list commands"

    def do_h(self, inp):
        print("Click P to Enter the Game")
        print("Click U to Calibrate the Screen")
        print("Click S to Update Stickies")
        print("Click Q to Quit the Game")

    def do_p(self, inp):
        print("Entering the Game")
        currentState = updateSticky()
        print("attempt at retrieving currentState")
        print(currentState)
        launch_game(currentState)

    def do_u(self, inp):
        print("Calibrating screen...")
        calibrate()
        print("Screen Calibrated")
    
    def do_s(self, inp):
        print("Updating Sticky Note Locations...")
        updateSticky()
        print("Stickies Updated")

    def do_q(self, inp):
        """Quit Game"""
        return True

MyPrompt().cmdloop()