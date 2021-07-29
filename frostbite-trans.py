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

# First queue: events from StreamReader -> ApiClient
# and TranslationService -> ApiClient
apiclient_input_queue = Queue()
# Second queue: events from ApiClient -> TranslationService
apiclient_output_queue = Queue()

def main():
    streamReader = streamreader.StreamReader(apiclient_input_queue)
    apiClient = apiclient.ApiClient(apiclient_input_queue,apiclient_output_queue)
    translationService = transsvc.TranslationService(apiclient_output_queue, apiclient_input_queue)
    
    t1 = threading.Thread(target = streamReader.start)
    t2 = threading.Thread(target = apiClient.start)
    t1.start()
    t2.start()
    translationService.start()
    threading.current_thread().join()

if __name__ == "__main__":
    main()
