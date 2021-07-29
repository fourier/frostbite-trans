#!/usr/bin/python
import socket
import sys
import queue
import time
import re
import evnt

INTERRUPTED = False
STREAM_PORT = 10000

class StreamReader(object):
    """Reader of the stream events from Frostbite."""    
    server_address = ('localhost', STREAM_PORT)
    buf_size = 4096
    room_title_matcher = re.compile("^\[.+\]\n")
    
    def __init__(self,q):
        self.socket = None
        self.queue = q
        
    def start(self):
        while not INTERRUPTED:
            self.connect_and_read()
#            print("Sleeping 1 sec...")
            time.sleep(1)
            
        print("Exiting")
        
    def connect_and_read(self):
        try:
            # Recreate and connect closed socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
            self.socket.connect(StreamReader.server_address)
            buffer = ''
            # Read from socket and accumulate
            while not INTERRUPTED:
                data = self.socket.recv(StreamReader.buf_size)
#                print("Recv returned %d bytes" % len(data))
                if data:
                    buffer += bytes.decode(data, 'UTF-8')
                    if len(data) < StreamReader.buf_size:
                        # Finally process the received data
                        self.process_data(buffer)
                        buffer = ''
                else:
                    # socket is closed
                    break
        except BaseException as e:
            None
#        print("Closing StreamReader socket")
        self.socket.close()

    def process_data(self, buffer):
        m = StreamReader.room_title_matcher.match(buffer)
        if m:
            print(m.group())
            self.queue.put(evnt.GetRoomDesc(m.group()))
            
            
