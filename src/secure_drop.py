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

# gen kets based on password for user
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
    #deleted password from memory
    gc.collect()
    return Fernet(key)

#encrypts message. 
def encrypt_msg(msg, Fernet):
    return Fernet.encrypt(msg.encode()).decode()

#Decrypts message using keys
def decrypt_msg(msg, Fernet):
    try:
        result = Fernet.decrypt(msg.encode()).decode()
        # print("Valid Key - Successfully decrypted")
        Fernet = None
        del Fernet
        return result
    except InvalidToken as e:
        print("Invalid Key - Unsuccessfully decrypted")
        sys.exit()

#Gets called when new user is detected i.e. no user.json file. Creates keys based on apsswrd and store all users info in user.json
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
    public_key = private_key.public_key().public_bytes(serialization.Encoding.OpenSSH, \
    serialization.PublicFormat.OpenSSH)
    pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption())
    # Update struct
    users.append({
        'name': encrypt_msg(name, Fernet),
        'email': encrypt_msg(email, Fernet),
        'password': hashlib.sha256(hashlib.sha256(password.encode()).hexdigest().encode()).hexdigest(),
        'contacts': [],
        'public_key' : encrypt_msg(public_key.decode('utf-8'), Fernet),
        'private_key' :  encrypt_msg(pem.decode('utf-8'), Fernet)
        
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

#If not a new user i.e. user.json exits than login. Check if email and password are correct.
def login(users):
    email = input("Enter Email Address: ")
    password = input("Enter Password: ")
    Fernet = gen_key(password)
    for index, user in enumerate(users):
        if email == decrypt_msg(user['email'], Fernet):
            if user['password'] == hashlib.sha256(hashlib.sha256(password.encode()).hexdigest().encode()).hexdigest():
               public_key =  decrypt_msg(user['public_key'],Fernet)
               private_key = decrypt_msg(user['private_key'],Fernet)
               return User(index, user, users_path, Fernet, email,public_key, private_key)
            else:
                print("Password or Email Do Not Match what is stored",
                      "\nExiting Secure Drop")
                sys.exit()

    print("Password or Email Do Not Match what is stored", "\nExiting Secure Drop")
    sys.exit()

#Create hash based on public key and email of current user, you used  for list
def keyemail(public_key, email):
    hasher = hashlib.sha256()
    hasher.update(public_key.encode())
    hasher.update(email.encode())
    return hasher.hexdigest()

#checks if given email and public key equal given hash for list
def hashcheck(hash, email, public_key):
    if keyemail(public_key, email) == hash:
        return True
    else:
        return False
