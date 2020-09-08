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


class Credentials():

    def __init__(self):
        self.__email = ""
        self.__name = ""
        self.__key = ""
        self.__password = ""
        self.__key_file = 'key.key'
        self.__time_of_exp = -1

# ----------------------------------------
# Getter setter for attributes
# ----------------------------------------

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        while (name == ''):
            name = input('Enter a proper User name, blank is not accepted:')
        self.__name = name

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email - email

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__key = Fernet.generate_key()
        f = Fernet(self.__key)
        self.__password = f.encrypt(password.encode()).decode()
        del f


    def create_cred(self,cred):
        """ 
        This function is responsible for encrypting the password and create key file for 
        storing the key and create a credential file with user name and password 
        """

        cred_filename = 'CredFile.ini'
		key = Fernet.generate_key()
		Fernetkey = Fernet(key)
		Fernetkey.encrypt(cred.password)

        


def new_Credential():
    # Creating an object for Credentials class
    creds = Credentials()

    # Accepting credentials
    creds.name = input("Enter Full Name: ")
    creds.email = input("Enter Email Address: ")
    creds.password = input("Enter Password:")
    print(
        "Enter the epiry time for key file in minutes, [default:Will never expire]")
    creds.expiry_time = int(input("Enter time:") or '-1')

    # calling the Credit
    creds.create_cred()
    print("**"*20)
    print("Cred file created successfully at {}"
          .format(time.ctime()))

    if not(creds.expiry_time == -1):
        os.startfile('expire.py')

    print("**"*20)
    return


def main():
    if os.path.isfile('CredFile.ini'):
        print("TEST")
    else:
        print("No users are registered with this client.")
        choice = input("Do you want to register a new user (y/n)?")
        if choice == 'y' or 'Y':
            new_Credential()


if __name__ == "__main__":
    main()
