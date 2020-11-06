import os
import sys
import json

# Program imports
from secure_drop import *
users_path = "users.json"

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
        # WE are "online" now
        # Main Program Loop
        
        print("\nWelcome to SecureDrop")
        #send our key and hash out
        #check if anyone is send us a file
        choice = input(
            'Type "help" For list of commands and "exit" to quit \n> ')
        while(True):
            if choice == "help":
                print()
                print('"add"  -> Add a new contact')
                print('"list" -> List all online contacts')
                print('"send" -> Transfer file to contact')
                print('"exit" -> Exit SecureDrop')
            elif choice == "add":
                # Enter some contact info
                User.add_contact()
            elif choice == "list":
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
                pass
                #send(cred)
                # name = input("Who would you like to send to?")
                # path = input("What file would you like to send")
                #User = send(users,name,path)

                pass
            elif choice == "exit":
                print("Exiting SecureDrop")
                sys.exit()
            else:
                print(choice, 'is an invalid option, type "help" for a list of commands')

            choice = input("\n> ")


if __name__ == "__main__":
    main()
