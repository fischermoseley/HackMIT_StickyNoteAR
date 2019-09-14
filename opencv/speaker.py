import socket
from pynput.keyboard import Key, Controller, Listener


UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6150

SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def sendjump(sock):
    sock.sendto( ("JUMP!").encode(), (UDP_IP_ADDRESS, UDP_PORT_NO) )
    print("Jump Action Triggered!")


def on_press(key):
    if key == Key.up:
        sendjump
    print('{0} pressed'.format(
        key))

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()