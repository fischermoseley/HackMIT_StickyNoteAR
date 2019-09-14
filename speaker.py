import socket

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6150

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


sock.sendto( ("JUMP!").encode(), (UDP_IP, UDP_PORT) )
print("Jump Action Triggered!")



