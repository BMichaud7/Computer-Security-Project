import os, sys, json
import hashlib
from cryptography.fernet import Fernet

# Program imports
from User import *

users_path = "users.json"
key_path = 'secret.json'

def set_json(file_path, perm, tag):
    # Create and perm file if it doesn't exists and write empty JSON tag
    try:
        with open(file_path, 'w+') as curr_file:
            curr_file.write(tag)
        if not(os.path.exists(file_path)):
            chmod(file_path, perm)
    except IOError:
        print("Error:", IOError, "\nFailed to open", file_path, "\nExiting...")
        sys.exit()

def gen_key():
    # Create and perm file if it doesn't exists or write if empty
    exists = os.path.exists(key_path)
    if not(os.path.exists(key_path)) or os.path.getsize(key_path) < 2:
        set_json(key_path, 0o600, '[]')

    key = Fernet.generate_key().decode()

    try:
        with open(key_path, 'w+') as key_file:
            json.dump([key], key_file)
    except IOError:
        print("Error:", IOError, "\nFailed to write key to", key_path, "\nExiting...")
        sys.exit()

    return Fernet(key)

def load_key():
    if os.path.exists(key_path):
        try:
            with open(key_path, 'r') as key_file:
                key = json.load(key_file)[0]
        except IOError:
            print("Error:", IOError, "\nFailed to read key from", key_path, "\nExiting...")
            sys.exit()

        return Fernet(key)

    else:
        print("ERROR: Key File doesn't exist")
        sys.exit()

def encrypt_msg(msg, Fernet):
    return Fernet.encrypt(msg.encode()).decode()

def decrypt_msg(msg, Fernet):
    return Fernet.decrypt(msg.encode()).decode()

def new_user(file_path, users):
    Fernet = gen_key()
    name = encrypt_msg(input("Enter Full Name: "), Fernet)
    email = encrypt_msg(input("Enter Email Address: "), Fernet)

    # Loop until passwords match
    passwordsMatch = False
    while(not passwordsMatch):
        password = input("Enter Password: ")
        re_password = input("Re-enter Password: ")
        if password == re_password:
            passwordsMatch = True
        else:
            print("\nPasswords don't match, try again:")

    # Update struct
    users.append({
        'name': name,
        'email': email,
        'password': hashlib.sha256(password.encode()).hexdigest(),
        'contacts': []
    })

    # Write out updated data
    with open(file_path, 'w') as users_file:
        json.dump(users, users_file)
        print("User Registered\n")

    #TODO: login automatically after registering

def login(users):
    Fernet = load_key();

    email = input("Enter Email Address: ")
    password = input("Enter Password: ")

    for index, user in enumerate(users):
        if email == decrypt_msg(user['email'], Fernet):
            if user['password'] == hashlib.sha256(password.encode()).hexdigest():
                return User(index, user, users_path, Fernet)
            else:
                break

    print("Password or Email Do Not Match what is stored", "\nExiting Secure Drop")
    sys.exit()