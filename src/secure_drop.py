import os.path
import json
import hashlib
from cryptography.fernet import Fernet

def new_user(users, file_path):
    # FIXME: try catch block is poorly scoped
    # try:
        with open(file_path, 'w') as users_file:
            name = input("Enter Full Name: ")
            email = input("Enter Email Address: ")

            passwordsMatch = False
            while(not passwordsMatch):
                password = input("Enter Password: ")
                re_password = input("Re-enter Password: ")
                if password == re_password:
                    #TODO: add contact array
                    users.append({
                        'name': encrypt_message(name),
                        'email': encrypt_message(email),
                        'password': hashlib.sha256(password.encode()).hexdigest()
                    })

                    json.dump(users, users_file)
                    print("User Registered.")
                    passwordsMatch = True
                else:
                    print("\nPasswords don't match, try again:")


    # except:
    #    print("ERROR: Unable to open ", file_path, " while creating a new user")


"""
def existing_user(users, file_path):
     with open(file_path, 'r') as users_file:
        key = load_key()
        email = input("Enter Email Address: ")
        attempted = input("Enter Password:")
        encoded_attemptedpassword = attempted.encode()
        f = Fernet(key)
        encrypt_attemptedpassword = hashlib.sha256(attempted.encode())
        # TODO load from JSON encrypt_password encrypt_email
        if encrypt_password == encrypt_attemptedpassword:
            # TODO decode name and email
            if encrypt_message(attemptedEmail) == encrypt_email: #check if email match
                # TODO decrypt all
                help()
            else:
                print("Password or Email Do Not Match what is stored")
                print("Exiting SecureDrop.")
                sys.exit()
        else:
            print("Password or Email Do Not Match what is stored")
            print("Exiting SecureDrop.")
            sys.exit()
"""

"""
def help():
    print("Welcome to SecureDrop.")
    help_menu=input("Type \"help\" For Commands.")
    if help_menu == "help":
        print("\"add\" -> Add a new contact")
        print("\"list\" -> List all online contacts")
        print("\"send\" -> Transfer file to contact")
        print("\"exit\" -> Exit SecureDrop")
        choice = input()
        switch (choice)
        {
            case "add":
                add()
                break;
            case "list":
                lists()
                break;
            case "send";
                send()
                break;
            case "exit":
                print("Exiting SecureDrop.")
                sys.exit()
                break;
            default:
                print(choice, "is an invalid choice, use help for a list of commands")
                pass
                break;
        }
"""


def add():
    print("# The \"add\" command adds a new contact for the user. If a contact exists, it overwrites \n# the existing details. Note that the email address is used as the user identifier.")
    name = input("Enter Full Name: ")
    email = input("Enter Email Address: ")
     # TODO
    #deencrypt_contact()
    #Checks if users exist
    #If it does Replace
    #If it doesnt make new Contact in array
    #encrypt_contact()

def lists():
    print("# The \"list\" command should show only those contacts that satisfy the following conditions -\n# 1. The contact information has been added to this user's contacts.\n# 2. The contact has also added this user's information to their contacts.\n# 3. The contact is online on the user's local network.")
     # TODO
    #decrypt_contact()
    #check contact if
    # 1. The contact information has been added to this user's contacts
    # 2. The contact has also added this user's information to their contacts.
    # 3. The contact is online on the user's local network.

def send():
    print("# The \"send\" command transfers a file to the contact. Note that the contact must receive the\n# following alert and they must approve the transfer. You can save the file to a directory\n# of your choice with the same file name as the transmitted file.\n# Contact",name," ","<",email,">" ,"is sending a file. Accept (y/n)?")


def generate_key():
    if os.path.exists("secret.key"):
        print("Key File already exists")
    else:
        # TODO change permissions  of  secret.key
        with open("secret.key", "wb") as key_file:
            key = Fernet.generate_key()
            key_file.write(key)
def load_key():
    if os.path.exists("secret.key"):
        return open("secret.key", "rb").read()
    else:
        print("Key File does not exist")
        return
def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message


def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message

def encrypt_contact(Contacts):
    pass
    # TODO
    #go threw array
    #encrypt_contact[i] = encrypt_message(dencrypt_Contact[i])
    #save encrypt_contact to JSON
def decrypt_contact(Contacts):
    pass
     # TODO
    #go threw array
    #decrypt_contact[i] = decrypt_message(encrypt_Contact[i])
    #return decrypt_contact
def encrypt_JSON(userfile,user):
    pass
    # TODO
    # encrypt_contact(Contacts)
    # encrypt_user from user object
    #save JSON from file

def dencrypt_JSON(userfile):
    pass
    # TODO
    # get data from JSON contact and user
    # user.contact =  dencrypt_contact(Contacts)
    # encrypt_user
    #save JSON from file
    #return user