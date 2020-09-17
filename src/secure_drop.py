import json
from cryptography.fernet import Fernet

def new_user(users, file_path):
    # FIXME: try catch block is poorly scoped
    # try:
        with open(file_path, 'w') as users_file:
            name = input("Enter Full Name: ")
            email = input("Enter Email Address: ")
            password = input("Enter Password:")
            re_password = input("Re-enter Password:")
            if password == re_password:
                users.append({ 'name': encrypt_message(name), 'email': encrypt_message(email), 'password': encrypt_message(password) }) #add contact array
                json.dump(users, users_file)
                print"User Registered.")
                print("Exiting SecureDrop.")
                sys.exit()
            else:
                print("Passwords Do Not Match")
                print("Exiting SecureDrop.")
                sys.exit()
            # TODO: create a key file or whatever we want to do with the key

    # except:
    #    print("ERROR: Unable to open ", file_path, " while creating a new user")



def existing_user(users, file_path):
     with open(file_path, 'r') as users_file:
        key = load_key()
        email = input("Enter Email Address: ")
        attempted = input("Enter Password:")
        encoded_attemptedpassword = attempted.encode()
        f = Fernet(key)
        encrypt_attemptedpassword = f.encrypt(encoded_attemptedpassword)
        #load from JSON encrypt_password encrypt_email
        if encrypt_password == encrypt_message(attempted):
            #decode name and email
            if encrypt_message(attemptedEmail) == encrypt_email: #check if email match
                #decrypt all 
                help()
            else:
            print("Password or Email Do Not Match what is stored")
            print("Exiting SecureDrop.")
            sys.exit()
        else:
            print("Password or Email Do Not Match what is stored")
            print("Exiting SecureDrop.")
            sys.exit()
            
            

def help():
    print("Welcome to SecureDrop.")
            help_menu =input("Type \"help\" For Commands.")
            if help_menu == "help":
                print("\"add\" -> Add a new contact")
                print("\"list\" -> List all online contacts")
                print("\"send\" -> Transfer file to contact")
                print("\"exit\" -> Exit SecureDrop")
                choice = input()
                switch (choice) {
                    case 1:  choice = "add";
                            add()
                            break;
                    case 2:  choice = "list";
                            lists()
                            break;
                    case 3:  choice = "send";
                            send()
                            break;
                    case 4:  choice = "exit";
                            print("Exiting SecureDrop.")
                            sys.exit()
                            break;
                    default: choice = "Invalid option";
                            print("Exiting SecureDrop.")
                            sys.exit()
                            break;
        }


def add():
    print("# The \"add\" command adds a new contact for the user. If a contact exists, it overwrites \n# the existing details. Note that the email address is used as the user identifier.")
def lists():
    print("# The \"list\" command should show only those contacts that satisfy the following conditions -\n# 1. The contact information has been added to this user's contacts.\n# 2. The contact has also added this user's information to their contacts.\n# 3. The contact is online on the user's local network.")
def send():
    print("# The \"send\" command transfers a file to the contact. Note that the contact must receive the\n# following alert and they must approve the transfer. You can save the file to a directory\n# of your choice with the same file name as the transmitted file.\n# Contact",name," ","<",email,">" ,"is sending a file. Accept (y/n)?")


def generate_keys():
    if path.exists("secret.key")
        print("Key File already exists")
    else:
        with open("secret.key", "wb") as key_file:
            key = Fernet.generate_key() 
            key_file.write(key)
def load_key():
    if path.exists("secret.key")
        return open("secret.key", "rb").read()
    else:
        print("Key File does not exist")
        return
def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message


def encrypt_message(message):
    """
    Encrypts a message
    """
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message