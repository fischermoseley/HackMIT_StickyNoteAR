import socket
import keyboard #make sure to pip install keyboard

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6150

def send_jump_eventI(sock):
    sock.sendto( ("JUMP!").encode(), (UDP_IP_ADDRESS, UDP_PORT_NO) )
    print("Jump Action Triggered!")

if __name__ == "__main__": 

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


