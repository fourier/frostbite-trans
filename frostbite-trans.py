#!/usr/bin/python

import sys
import queue
import time
import re
import streamreader

from threading import Thread
from queue import Queue

q = Queue()

def main():
    streamReader = streamreader.StreamReader(q)
    streamReader.start()

if __name__ == "__main__":
    main()
