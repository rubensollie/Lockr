import threading
import time
import socket
import struct
import sys

class MulticastService(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run (self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        while(True):
            sock.sendto("lockerserver".encode(), ('255.255.255.255', 10000));
            time.sleep(1)

        
