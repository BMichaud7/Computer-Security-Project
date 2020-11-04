import os, sys, json
import hashlib
from cryptography.fernet import Fernet,InvalidToken
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

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

# def gen_key():
#     # Create and perm file if it doesn't exists or write if empty
#     exists = os.path.exists(key_path)
#     if not(os.path.exists(key_path)) or os.path.getsize(key_path) < 2:
#         set_json(key_path, 0o600, '[]')

#     key = Fernet.generate_key().decode()

#     try:
#         with open(key_path, 'w+') as key_file:
#             json.dump([key], key_file)
#     except IOError:
#         print("Error:", IOError, "\nFailed to write key to", key_path, "\nExiting...")
#         sys.exit()

#     return Fernet(key)

# def load_key():
#     if os.path.exists(key_path):
#         try:
#             with open(key_path, 'r') as key_file:
#                 key = json.load(key_file)[0]
#         except IOError:
#             print("Error:", IOError, "\nFailed to read key from", key_path, "\nExiting...")
#             sys.exit()

#         return Fernet(key)

#     else:
#         print("ERROR: Key File doesn't exist")
#         sys.exit()

def gen_key(password_input):
    password_provided = password_input
    password = password_provided.encode()  # Convert to type bytes
    salt = b'thisissecurepassword'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once
    return Fernet(key)



def encrypt_msg(msg, Fernet):
    return Fernet.encrypt(msg.encode()).decode()

def decrypt_msg(msg, Fernet):
    try:
        result = Fernet.decrypt(msg.encode()).decode()
        print("Valid Key - Successfully decrypted")
        return result
    except InvalidToken as e:
        print("Invalid Key - Unsuccessfully decrypted")
        sys.exit()

def new_user(file_path, users):
    name = input("Enter Full Name: ")
    email = input("Enter Email Address: ")

    # Loop until passwords match
    passwordsMatch = False
    while(not passwordsMatch):
        password = input("Enter Password: ")
        re_password = input("Re-enter Password: ")
        if password == re_password:
            passwordsMatch = True
        else:
            print("\nPasswords don't match, try again:")
    Fernet = gen_key(password)

    # Update struct
    users.append({
        'name': encrypt_msg(name,Fernet),
        'email': encrypt_msg(email,Fernet),
        'password': hashlib.sha256(hashlib.sha256(password.encode()).hexdigest().encode()).hexdigest(),
        'contacts': []
    })

    # Write out updated data
    with open(file_path, 'w') as users_file:
        json.dump(users, users_file)
        print("User Registered\n")

    #TODO: login automatically after registering

def login(users):
    email = input("Enter Email Address: ")
    password = input("Enter Password: ")
    Fernet = gen_key(password);
    for index, user in enumerate(users):
        if email == decrypt_msg(user['email'], Fernet):
            if user['password'] == hashlib.sha256(hashlib.sha256(password.encode()).hexdigest().encode()).hexdigest():
                return User(index, user, users_path, Fernet)
            else:
                print("Password or Email Do Not Match what is stored", "\nExiting Secure Drop")
                sys.exit()

    print("Password or Email Do Not Match what is stored", "\nExiting Secure Drop")
    sys.exit()