# Program imports
import os
import sys
import json
import socket
import network
import pickle
from os import path
from secure_drop import *
from multiprocessing import Process
import time
import socket
import tqdm
users_path = "users.json"

# When someone logins in infiniteping starts beign called every 5 seconds in its own thread. 
def infiniteping(email,public_key):
    while(1):
        network.sendping(email, public_key)
        time.sleep(5)

def main():
    # check if user.json exist. If it does we try to login
    # If file doesn't exists or doesn't have brackets create file and/or add []
    if not os.path.exists(users_path) or os.path.getsize(users_path) < 2:
        set_json(users_path, 0o640, '[]')

    # load users from JSON
    try:
        with open(users_path, 'r') as users_file:
            users = json.load(users_file)
    except IOError:
        print("Error:", IOError)
        print("Couldn't open", users_path, "\nExiting...")
        sys.exit()

    # if no users exists, ask user to create one
    if(not len(users)):
        choice = input(
            "No users exists, Would you like to create a new user (Y/n)? ").lower()
        if (choice == "y") or (choice == "yes"):
            new_user(users_path, users)
            sys.exit()
        else:
            print("At least one user must exists to use Secure Drop\n",
                  "Exiting Secure Drop")
            sys.exit()
    else:
        # Login
        User = login(users)
        email, public_key, private_key = User.getCred()
        # WE are "online" now
        # Main Program Loop
        
        print("\nWelcome to SecureDrop")
        #send our key and hash out
        #check if anyone is send us a file
        network.init_ip()
        # we are loggedin now so we sart brocasting we are online with 2 threads.
        # p is for infiniteping and p1 is for receiving a file.
        p = Process(target=infiniteping, args=(email,public_key,) )
        p.start()
        p1 = Process(target=network.rec, args=(User,))
        p1.start()
        choice = input(
            'Type "help" For list of commands and "exit" to quit \n> ')
        while(True):
            if choice == "help":
                #
                print()
                print('"add"  -> Add a new contact')
                print('"list" -> List all online contacts')
                print('"send" -> Transfer file to contact')
                print('"exit" -> Exit SecureDrop')
            elif choice == "add": 
                
                # Enter some contact info
                # call add contact which handles adding contact to user.json file and saving new file
                User.add_contact()
            elif choice == "list":
                # lising online contacts that we know
                # print("BEFORE IN LIST : " , User.get_prop('contacts'))
                # network.weAreHere(email, "hi") 
                client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) #UDP

                client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

                #enable broadcasting
                client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
                client.settimeout(30.0)
                client.bind(("0.0.0.0", 37020))
                amTru = True
                online_contacts = []
                # add all online_contacts packets in array ang check if knwon and get ride of duplicates
                while amTru:
                    print("Searching for online contacts. This will take up to 30 seconds...\n")
                    try:
                        data, addr = client.recvfrom(1024)
                        recd = pickle.loads(data)
                        #print("%s"%recd)
                        the_hash = recd[2]
                        the_pub = recd[1]
                        ip = recd[3]
                        # print("IP REC", ip)
                        timeout = time.time() + 30
                        while ip == network.own_ip: 
                            # print("In Loop")
                            # print("INLOOP IN LIST : " , User.get_prop('contacts'))
                            if time.time() > timeout:
                                break
                            data, addr = client.recvfrom(1024)
                            recd = pickle.loads(data)
                            #print("%s"%recd)
                            the_hash = recd[2]
                            the_pub = recd[1]
                            ip = recd[3]
                            # save the ip public key, hash i.e. public key + email.
                        # print("BEFORE WHOISTHIS : " , User.get_prop('contacts'))
                        #check if person is known
                        name , known = User.whoisthis(the_pub,the_hash,ip)
                        # print("AFTER WHOISTHIS : " , User.get_prop('contacts'))
                        print(name,known)
                        # print("BEFORE KNOWN IN LIST : " , User.get_prop('contacts'))
                        if known:
                            online_contacts.append(name)
                        else:
                            online_contacts = list(dict.fromkeys(online_contacts))
                        # print("AFTER KNOWN IN LIST : " , User.get_prop('contacts'))         
                        # print(User.whoisthis(the_pub,the_hash))
                    except socket.timeout:
                        print("Online Contacts: 0\n")
                    amTru = False
               
                # print("online_contacts: ", online_contacts)
                print("Online Contacts: ", len(online_contacts))
                for names in range(len(online_contacts)):
                    print(online_contacts[names])
                #print names of known people online.
                contacts = User.get_prop('contacts')
                num_contacts = len(contacts)
                if num_contacts:
                    if(num_contacts > 1):
                        print(num_contacts, "Contact:")
                    else:
                        print(num_contacts, "Contacts:")

                    for contact in contacts:
                        print("  -", contact['email'])
                        # printing online offline and if no contacts

                else:
                    print("No contacts exist")
            # send file
            #what file you want to send checks if file and contact exist
            elif choice == "send":
                name = input("Who would you like to send to?\n")
                filetosend = input("What file would you like to send\n")
                if path.exists(filetosend):
                    public_key, ip = User.getNetworking(name)
                    while ip == None:
                        print("Contact not Found")
                        name = input("Who would you like to send to?\n")
                        filetosend = input("What file would you like to send\n")
                        public_key, ip = User.getNetworking(name)
                        #get saved networking info from listing
                    #send the selsct file to the selected person.
                    network.send(public_key,ip,filetosend)
                else:
                    print("File does not exist")
            elif choice == "exit":
                print("Exiting SecureDrop")
                #stop all threads
                p.terminate()
                p1.terminate()
                sys.exit()
            else:
                print(choice, 'is an invalid option, type "help" for a list of commands')
            
            
            choice = input("\n> ")




if __name__ == "__main__":
    main()
