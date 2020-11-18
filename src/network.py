import sys
import ssl
import socket
import time
import User
from secure_drop import *
from main import *



def weAreHere(email, public_key):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    server.settimeout(0.2)
    hash1 = keyemail(public_key, email)
    d = {1:public_key , 2: hash1}

    msg = pickle.dumps(d)
    #print("Going out:", msg)

    amTru = True
    while amTru:
        server.sendto(msg, ('<broadcast>', 37020))
        amTru = False
