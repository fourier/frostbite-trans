import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on %s port %s' % server_address)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
f = open("game-log.txt","r")
lines = f.readlines()

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        i = 0
        while True:
            time.sleep(0.1)
#            print("Sending line %s" % lines[i])
            connection.send(str.encode(lines[i]))
            i = i+1
            if i == len(lines): i = 0

    finally:
        # Clean up the connection
        connection.close()
