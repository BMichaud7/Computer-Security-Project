import os
import sys
import json
import socket
import network
import pickle
# Program imports
from secure_drop import *
from multiprocessing import Process
import time
import socket
import tqdm
import os
users_path = "users.json"


def infiniteping(email,public_key):
    while(1):
        network.sendping(email, public_key)
        time.sleep(5)

def main():
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
        p = Process(target=infiniteping, args=(email,public_key,) )
        p.start()
        p1 = Process(target=network.rec,)
        p1.start()
        choice = input(
            'Type "help" For list of commands and "exit" to quit \n> ')
        while(True):
            if choice == "help":
                # network.weAreHere(email, "hi")
                print()
                print('"add"  -> Add a new contact')
                print('"list" -> List all online contacts')
                print('"send" -> Transfer file to contact')
                print('"exit" -> Exit SecureDrop')
            elif choice == "add": 
                # network.weAreHere(email, "hi")  
                # Enter some contact info
                User.add_contact()
            elif choice == "list":
                # network.weAreHere(email, "hi") 
                client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) #UDP

                client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

                #enable broadcasting
                client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
                client.settimeout(30.0)
                client.bind(("", 37020))
                amTru = True
                online_contacts = []
                while amTru:
                    print("Searching for online contacts. This will take up to 30 seconds...\n")
                    try:
                        data, addr = client.recvfrom(1024)
                        recd = pickle.loads(data)
                        #print("%s"%recd)
                        the_hash = recd[2]
                        the_pub = recd[1]
                        ip = recd[3]
                        name , known = User.whoisthis(the_pub,the_hash,ip)
                        if known:
                           online_contacts.append(name)
                        else:
                            pass
                        online_contacts = list(dict.fromkeys(online_contacts))
                                               
                        # print(User.whoisthis(the_pub,the_hash))
                    except socket.timeout:
                        print("Online Contacts: 0\n")
                    amTru = False
                print("Online Contacts: ", len(online_contacts))
                for names in range(len(online_contacts)):
                    print(online_contacts[names])
                    
                #we are the socket server now
                #clients are sending us their publickey and hash
                # for all the uniq hash we do
                # name, known = User.whoisthis()
                # check if we have a contact with the email threw network
                # if known == True we know them
                # we should also save their public key for sending
                # User.saveNetworking(public_key,email)
                # if we do list them
                # User.saveNetworking("PUBKEY","Test")
                # print(User.getNetworking("Test"))
                # print(User.hashthiscontact("b", "TEST"))
                # name, found = User.whoisthis(
                #     "TEST", User.hashthiscontact("b", "TEST"))
                # print(name)
                contacts = User.get_prop('contacts')
                # network.weAreHere(email, "hi") 
                num_contacts = len(contacts)
                if num_contacts:
                    if(num_contacts > 1):
                        print(num_contacts, "Contact:")
                    else:
                        print(num_contacts, "Contacts:")

                    for contact in contacts:
                        print("  -", contact['email'])

                else:
                    print("No contacts exist")

            elif choice == "send":
                name = input("Who would you like to send to?")
                path = input("What file would you like to send")
                public_key, ip = User.getNetworking(name)
                network.send(pub_key,ip,path)
                # name = input("Who would you like to send to?")
                # path = input("What file would you like to send")
                s.close()
            elif choice == "exit":
                print("Exiting SecureDrop")
                p.terminate()
                p1.terminate()
                sys.exit()
            else:
                print(choice, 'is an invalid option, type "help" for a list of commands')
            
            
            choice = input("\n> ")




if __name__ == "__main__":
    main()
