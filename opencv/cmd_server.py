from cmd import Cmd
from boundingBox import updateFromCamera, calibrateFromCamera


class MyPrompt(Cmd):
    prompt = 'sticky_server> '
    intro = "Welcome to StickyAR! Type H to list commands"

    def do_h(self, inp):
        print("Click P to Enter the Game\n")
        print("Click U to Calibrate the Screen\n")
        print("Click S to Update Stickies")
        print("Click Q to Quit the Game\n")

    def do_p(self, inp):
        print("Entering the Game")  
        #Luke command to enter the game

    def do_u(self, inp):
        print("Calibrating screen...")
        # calibrate() # <--- Place calibration function here, Zach
        print("Screen Calibrated")
    
    def do_s(self, inp):
        print("Updating Sticky Note Locations...")
        # calibrate() # <--- Place calibration function here, Zach
        print("Stickies Updated")

    def do_q(self, inp):
        '''quit'''
        return True

MyPrompt().cmdloop()