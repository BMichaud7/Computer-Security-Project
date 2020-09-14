# CreateCred.py
# Creates a credential file.
import os.path
from cryptography.fernet import Fernet
import re
import ctypes
import time
import os
import sys
from pathlib import Path
import uuid
import hashlib
import json
class Contact():

    def __init__(self):
        self.__email = ""
        self.__name = ""

class Credentials():

    def __init__(self):
        self.__email = ""
        self.__name = ""
        self.__key = ""
        self.__password = ""
        self.__contacts = []

# ----------------------------------------
# Getter setter for attributes
# ----------------------------------------

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        while (name == ''):
            name = input('Enter a proper name, blank is not accepted:')
        self.__name = name

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email
        
    @property
    def password(self):
        return self.__password
        
    @password.setter
    def password(self, email):
        self.__password = __password
 

        
def new_Credential():
    # Creating an object for Credentials class
    creds = Credentials()
    # Accepting credentials
    creds.name = input("Enter Full Name: ")
    creds.email = input("Enter Email Address: ")
    password = input("Enter Password:")
    generate_key()
    key = load_key()
    encoded_password = password.encode()
    f = Fernet(key)
    creds.create_cred = f.encrypt(encoded_password)
    # Write Json file
def add_contact(contact):
#check if email exist with any other contacts if it does overide
# adds to __contacts list
def list_contact():
 #prints list of contacts
#https://medium.com/podiihq/networking-how-to-communicate-between-two-python-programs-abd58b97390a
def sendfile(file):
#https://www.thepythoncode.com/article/send-receive-files-using-sockets-python

def new_Credential_save(Credentials):
    s = json.dumps(Credentials.__dict__) 

def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
def load_key():
    return open("secret.key", "rb").read()
def main():
    if os.path.isfile('CredFile.json'):
        # Read JSON file in
        #compare  hashed_password to entered password

    else:
        print("No users are registered with this client.")
        choice = input("Do you want to register a new user (y/n)?")
        if choice == 'y' or 'Y':
            new_Credential()


if __name__ == "__main__":
    main()
