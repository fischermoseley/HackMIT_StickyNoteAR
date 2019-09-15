from cmd import Cmd
from interpreter import interpreter
import socket


UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6150

SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Create a datagram socket
SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class MyPrompt(Cmd):
    prompt = 'sticky_server> '
    intro = "Welcome to StickyAR! Type ? to list commands"

    
    SOCK.sendto(("connecting").encode(), (UDP_IP_ADDRESS, UDP_PORT_NO) )

    def do_u(self, inp):
        '''calibrate screen'''
        # calibrate() # <--- Place calibration function here, Zach
        print("Calibrating screen...")
    
    def do_p(self, inp):
        '''create new level'''
        print("Creating new level...")
        
        SOCK.sendto(("P180090234144").encode(),  (UDP_IP_ADDRESS, UDP_PORT_NO) )
        print("Board Reset!")

    def do_q(self, inp):
        '''quit'''
        return True


SOCK.sendto(("connecting").encode(),  (UDP_IP_ADDRESS, UDP_PORT_NO))
MyPrompt().cmdloop()