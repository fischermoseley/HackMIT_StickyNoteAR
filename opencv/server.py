import socket

localIP     = "127.0.0.1"
localPort   = 6150
bufferSize  = 1024

# Create a datagram socket
SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and ip
SOCK.bind((localIP, localPort))

# Listen for incoming datagrams
while True: 
    bytesAddressPair = SOCK.recvfrom(bufferSize)
    message = bytesAddressPair[0]

    translate = "{}".format(message)

    if(translate=='calibrate'):
        #write the call function to fischers code
        #bytesToSend = ""

        # Sending a reply to client
        SOCK.sendto(("I'm calibrating").encode())

    elif(translate=='sticky'):
        #write the call function to fischers code
        #bytesToSend = ""

        # Sending a reply to client
        SOCK.sendto(("I'm wet").encode())

    
    
    