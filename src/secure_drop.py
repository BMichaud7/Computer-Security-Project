import os.path
import json
import hashlib
from cryptography.fernet import Fernet
import os, sys, stat 
import shutil
import subprocess 

def new_user(file_path):
    # FIXME: try catch block is poorly scoped
    # try:
            generate_key()
            key = load_key()
            fernet_instance = Fernet(key)
            name = encrypt_message(raw_input("Enter Full Name: "))
            email = encrypt_message(raw_input("Enter Email Address: "))
            passwordsMatch = False
            while(not passwordsMatch):
                password = raw_input("Enter Password: ")
                re_password = raw_input("Re-enter Password: ")
                if password == re_password:
                    user={}
                    user['main'] = []
                    #TODO: add contact array
                    user['main'].append({
                        'name': name,
                        'email': email,
                        'password': hashlib.sha256(password.encode()).hexdigest()
                    })
                    with open(file_path, 'w') as users_file:
                        json.dump(user, users_file)
                        print("User Registered.")
                        passwordsMatch = True

                else:
                    print("\nPasswords don't match, try again:")


    # except:
    #    print("ERROR: Unable to open ", file_path, " while creating a new user")

def e_user(file_path):
    with open(file_path) as users_file:
        user = json.load(users_file)
        key = load_key()
        attemptedEmail = raw_input("Enter Email Address: ")
        attempted = raw_input("Enter Password:")
        encoded_attemptedpassword = attempted.encode()
        f = Fernet(key)
        encrypt_attemptedpassword = hashlib.sha256(attempted.encode()).hexdigest()
        for p in user['main']:
            encrypt_password = p['password']
            encrypt_email = p['email']
            encrypt_name = p['name']
        # TODO load from JSON encrypt_password encrypt_email
        if encrypt_password==encrypt_attemptedpassword:
            print("Password or Email Do  Match what is stored")
            # TODO decode name and email
            print("encrypt_message(attemptedEmail): ", encrypt_message(attemptedEmail))
            print("encrypt_email: ", encrypt_email)
            if attemptedEmail == decrypt_message(encrypt_email): # TODO why is is retureing false? Why is the attemptedEmail dif then encrypt_email
                #is it some how a diffent key?
                email = decrypt_message(encrypt_email)
                name = decrypt_message(encrypt_name)
                print("Name: ", name)
                print("Email: ", email)
                help()
            else:
                print("Password or Email Do Not Match what is stored")
                print("Exiting SecureDrop.")
                sys.exit()
        else:
            print("Password or Email Do Not Match what is stored")
            print("Exiting SecureDrop.")
            sys.exit()

def existing_user(file_path):
    print ("Test")



def help():
    print("Welcome to SecureDrop.")
    help_menu=raw_input("Type \"help\" For Commands.\n#")
    if help_menu == "help":
        print("\"add\" -> Add a new contact")
        print("\"list\" -> List all online contacts")
        print("\"send\" -> Transfer file to contact")
        print("\"exit\" -> Exit SecureDrop")
        choice = raw_input()
        if choice == "add":
            add()
        elif choice == "list":
            lists()
        elif choice == "send":
            send()
        elif choice == "exit":
            print("Exiting SecureDrop.")
            sys.exit()
        else:
            print(choice, "is an invalid choice, use help for a list of commands")
        



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
            print("key in GEN: ",key)
def load_key():
    if os.path.exists("secret.key"):
        print ("Key: ",open("secret.key", "rb").read())
        return open("secret.key", "rb").read()
    else:
        print("Key File does not exist")
        sys.exit()
def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    print("F in load: ", f)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()


def encrypt_message(message):
    key = load_key()
    fernet_instance = Fernet(key)
    encrypted_message = fernet_instance.encrypt(message.encode('utf-8')).decode('utf-8')
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
def setfile(file_path):
    os.chown(file_path, 1000, 1000)
    subprocess.call(['chmod', '0700', file_path])
    # TODO check if right permisions