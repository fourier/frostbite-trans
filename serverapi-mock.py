import socket
import sys
import time

room_desc = "Plush seats lined up in rows face a hardwood stage raised four feet from the ground.  Red velvet curtains draped from the high vaulted ceiling cover the walls.  The acoustics create a warm echo which lends an air of nobility to the place.  A podium in the corner hints that the hall must be used for formal meetings as well as performances.\\0"
room_title = "[Bards' Guild, Performance Hall]\\0"

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10001)
print('starting up on %s port %s' % server_address)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        while True:
            data = connection.recv(4096)
            req = bytes.decode(data, 'UTF-8').rstrip()
            if req == "GET ROOM_DESC":
                print("Requested room description")
                connection.send(str.encode(room_desc))
            elif req == "GET ROOM_TITLE":
                print("Requested room title")
                connection.send(str.encode(room_title))
            else:
                connection.send(str.encode("\\0"))
    finally:
        # Clean up the connection
        connection.close()
