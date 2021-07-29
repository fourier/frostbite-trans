#!/usr/bin/python

import sys
import queue
import time
import re
import threading
# local imports
import streamreader
import apiclient
import transsvc

from threading import Thread
from queue import Queue

q1 = Queue()
q2 = Queue()

def main():
    streamReader = streamreader.StreamReader(q1)
    apiClient = apiclient.ApiClient(q1,q2)
    
    t1 = threading.Thread(target = streamReader.start)
    t2 = threading.Thread(target = apiClient.start)
    t1.start()
    t2.start()
    transsvc.trans(q1,q2)
    threading.current_thread().join()

if __name__ == "__main__":
    main()
