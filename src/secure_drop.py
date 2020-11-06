import os
import sys
import json
import gc
import hashlib
from cryptography.fernet import Fernet, InvalidToken
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

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
            os.chmod(file_path, perm)
    except IOError:
        print("Error:", IOError, "\nFailed to open", file_path, "\nExiting...")
        sys.exit()


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
    key = base64.urlsafe_b64encode(
        kdf.derive(password))  # Can only use kdf once
    password_provided = None
    password = None
    password_input = None
    del password_provided
    del password
    del password_input
    gc.collect()
    return Fernet(key)


def encrypt_msg(msg, Fernet):
    return Fernet.encrypt(msg.encode()).decode()


def decrypt_msg(msg, Fernet):
    try:
        result = Fernet.decrypt(msg.encode()).decode()
        print("Valid Key - Successfully decrypted")
        Fernet = None
        del Fernet
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
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend())
    public_key = private_key.public_key()
    # Update struct
    users.append({
        'name': encrypt_msg(name, Fernet),
        'email': encrypt_msg(email, Fernet),
        'password': hashlib.sha256(hashlib.sha256(password.encode()).hexdigest().encode()).hexdigest(),
        'contacts': []

    })
    Fernet = None
    password = None
    re_password = None
    del password
    del re_password
    del Fernet
    gc.collect()
    # Write out updated data
    with open(file_path, 'w') as users_file:
        json.dump(users, users_file)
        print("User Registered\n")


def login(users):
    email = input("Enter Email Address: ")
    password = input("Enter Password: ")
    Fernet = gen_key(password)
    for index, user in enumerate(users):
        if email == decrypt_msg(user['email'], Fernet):
            if user['password'] == hashlib.sha256(hashlib.sha256(password.encode()).hexdigest().encode()).hexdigest():
                return User(index, user, users_path, Fernet)
            else:
                print("Password or Email Do Not Match what is stored",
                      "\nExiting Secure Drop")
                sys.exit()

    print("Password or Email Do Not Match what is stored", "\nExiting Secure Drop")
    sys.exit()


def keyemail(public_key, email):
    hasher = hashlib.sha256()
    hasher.update(public_key)
    hasher.update(email)
    return hasher.hexdigest()


def hashcheck(hash, email, public_key):
    if keyemail(public_key, email) == hash:
        return True
    else:
        return False
