#!/usr/bin/python
import socket
import sys
import queue
import time
import re
import urllib
import urllib.parse
# Local imports
import evnt

INTERRUPTED = False
API_SERVER_PORT = 3001

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
            # Create a translation window on a client
            print("Sending request to create window...")
            self.socket.send(str.encode("CLIENT WINDOW_ADD?trans&Translation\n"))
            data = self.socket.recv(ApiClient.buf_size)
            print("Reply: %s" % bytes.decode(data, 'UTF-8'))
            buffer = ''
            # Read from socket and accumulate
            while not INTERRUPTED:
                ev = self.read_queue.get()
                if type(ev) == evnt.GetRoomDesc:
                    print("Sending request to get room desc...")
                    self.socket.send(str.encode("GET ROOM_DESC\n"))
                    data = self.socket.recv(ApiClient.buf_size)
                    if data:
                        txt = bytes.decode(data, 'UTF-8')
                        print("Request room desc: %s" % txt)
                        self.write_queue.put(evnt.RequestTranslation(txt))
                    else:
                        # socket is closed
                        break
                elif type(ev) == evnt.SendTranslation:
                    print("Sending request to clear window...")
                    self.socket.send(str.encode("CLIENT WINDOW_CLEAR?trans\n"))
                    data = self.socket.recv(ApiClient.buf_size)
                    print("Reply: %s" % bytes.decode(data, 'UTF-8'))
                    txt = urllib.parse.quote(ev.translation)
                    print("Sending request to write to window...")
                    self.socket.send(str.encode("CLIENT WINDOW_WRITE?trans&" + txt + "\n"))
                    data = self.socket.recv(ApiClient.buf_size)
                    print("Reply: %s" % bytes.decode(data, 'UTF-8'))
                    
                    
        except BaseException as e:
            print(e)
#        print("Closing StreamReader socket")
        self.socket.close()
            
            
