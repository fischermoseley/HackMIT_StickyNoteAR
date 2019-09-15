import socket

localIP     = "127.0.0.1"
localPort   = 6150
bufferSize  = 1024

def run_server():
    # Create a datagram socket
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind to address and ip
    SOCK.bind((localIP, localPort))

    SOCK.sendto(("connecting").encode(), (localIP, localPort))

    # Listen for incoming datagrams
    try:
        while True:
            bytesAddressPair = SOCK.recvfrom(bufferSize)

            message = bytesAddressPair[0]
            print(message)
            translate = "{}".format(message)
            
            if(translate=='hello'):
                SOCK.sendto(("Connected").encode())

            elif(translate=='calibrate'):
                SOCK.sendto(("I'm calibrating").encode())

            elif(translate=='sticky'):
                #write the call function to fischers code
                #bytesToSend = ""
                # Sending a reply to client
                SOCK.sendto(("P180090234144").encode())
    except KeyboardInterrupt:
        print("terminating server")


if __name__ == "__main__":
    run_server()

    
    
    