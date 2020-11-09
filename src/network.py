import sys
import ssl
import socket
import time
import User




#server data

def weAreHere():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    server.settimeout(0.2)
    message = b"I'm online"

    amTru = True
    while amTru:
        server.sendto(User.getNetworking, ('<broadcast>', 37020))
        amTru = False
