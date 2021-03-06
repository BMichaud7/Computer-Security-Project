import sys
import ssl
import socket
import time
import User
import os
from secure_drop import *
from main import *
import re

own_ip = None

#get own ip 
def init_ip():
    global own_ip
    stream = os.popen('hostname -I')
    output = stream.read()
    own_ip = output.strip()
    # print(own_ip)

#calcs ping packet i.e. publickey and email. sends using pickel combines them.
def sendping(email, public_key):
    server = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)
    hash1 = keyemail(public_key, email)
    # print("SENDING THIS IP", own_ip)
    # print("SENDING THIS IP TO CONTACT: ", own_ip)
    d = {1: public_key, 2: hash1, 3: own_ip}

    msg = pickle.dumps(d)
    # print("Going out:", msg)

    amTru = True
    while amTru:
        server.sendto(msg, ('<broadcast>', 37020))
        amTru = False

#checks if new file is tring to be send from contact.
def rec(User):
    # device's IP address
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 5001
    # receive 4096 bytes each time
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    # create the server socket
    # TCP socket
    s = socket.socket()
    # bind the socket to our local address
    s.bind((SERVER_HOST, SERVER_PORT))
    # enabling our server to accept connections
    # 5 here is the number of unaccepted connections that
    # the system will allow before refusing new connections
    s.listen(5)
    # print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    # accept connection if there is any
    client_socket, address = s.accept()
    # if below code is executed, that means the sender is connected
    ipPattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    # findIP = find(ipPattern,address)
    # print("findIP: ",findIP)
    name = User.whoisthisip(address[0])
    print(f"{name} is sending a file, with an IP of: {address} is sending a file.\n>")

    # receive the file infos
    # receive using client socket, not server socket
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.basename(filename)
     # convert to integer
    filesize = int(filesize)
      # start receiving the file from the socket
      # and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for _ in progress:
                # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                    # nothing is received
                    # file transmitting is done
                break
                # write to the file the bytes we just received
            f.write(bytes_read)
                # update the progress bar
            progress.update(len(bytes_read))

        # close the client socket
    client_socket.close()
        # close the server socket
    s.close()
    print(">")


def send(pub_key, ip, file):
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096  # send 4096 bytes each time step
    # the ip address or hostname of the server, the receiver
    host = ip
    # the port, let's use 5001
    port = 5001
    # the name of file we want to send, make sure it exists
    filename = file
    # get the file size
    filesize = os.path.getsize(filename)
    # create the client socket
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    # send the filename and filesize
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())
    # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        for _ in progress:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    # close the socket
    s.close()
