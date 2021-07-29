#!/usr/bin/python
import socket
import sys
import queue
import time
import re
import evnt

INTERRUPTED = False
API_SERVER_PORT = 10001

class ApiClient(object):
    """Reader of the stream events from Frostbite."""    
    server_address = ('localhost', API_SERVER_PORT)
    buf_size = 4096
    
    def __init__(self,input_queue, output_queue):
        self.socket = None
        self.read_queue = input_queue
        self.write_queue = output_queue
        
    def start(self):
        while not INTERRUPTED:
            self.connect()
#            print("Sleeping 1 sec...")
            time.sleep(1)
            
        print("Exiting")
        
    def connect(self):
        try:
            # Recreate and connect closed socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
            self.socket.connect(ApiClient.server_address)
            buffer = ''
            # Read from socket and accumulate
            while not INTERRUPTED:
                ev = self.read_queue.get()
                if type(ev) == evnt.GetRoomDesc:
                    self.socket.send(str.encode("GET ROOM_DESC"))
                    data = self.socket.recv(ApiClient.buf_size)
                    if data:
                        txt = bytes.decode(data, 'UTF-8')
                        print("Request room desc: %s" % txt)
                        self.write_queue.put(evnt.RequestTranslation(txt))
                    else:
                        # socket is closed
                        break
                elif type(ev) == evnt.SendTranslation:
                    print(ev.translation)
                    
        except BaseException as e:
            None
#        print("Closing StreamReader socket")
        self.socket.close()
            
            
