import socket

localIP     = "127.0.0.1"
localPort   = 6150
bufferSize  = 1024

connection = False

# Create a datagram socket
SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and ip
SOCK.bind((localIP, localPort))

SOCK.sendto(("connecting").encode())

# Listen for incoming datagrams
while True:
    bytesAddressPair = SOCK.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    translate = "{}".format(message)

    if(translate=='hello'):
        SOCK.sendto(("Connected").encode())
        connection = True

    elif(translate=='calibrate' and connection):
        SOCK.sendto(("I'm calibrating").encode())

    elif(translate=='sticky' and connection):
        #write the call function to fischers code
        #bytesToSend = ""
        # Sending a reply to client
        SOCK.sendto(("P180090234144").encode())

    
    
    