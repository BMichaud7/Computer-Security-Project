import os
import sys
import json
import hashlib
from cryptography.fernet import Fernet, InvalidToken


def encrypt_msg(msg, Fernet):
    return Fernet.encrypt(msg.encode()).decode()


def decrypt_msg(msg, Fernet):
    try:
        result = Fernet.decrypt(msg.encode()).decode()
        Fernet = None
        del Fernet
        return result
    except InvalidToken as e:
        print("Invalid Key - Unsuccessfully decrypted")
        sys.exit()


class User():
    def __init__(self, index, user, users_path, Fernet):
        self.__index = index
        self.__user = user
        self.__path = users_path
        self.__Key = Fernet

    def update_file(self):
        try:
            with open(self.__path, 'r') as curr_file:
                users = json.load(curr_file)
        except IOError:
            print("Error:", IOError, "\nFailed to read from",
                  self.__path, "\nExiting...")

        try:
            with open(self.__path, 'w') as curr_file:
                users[self.__index] = self.__user
                json.dump(users, curr_file)
        except IOError:
            print("Error:", IOError, "\nFailed to write to",
                  self.__path, "\nExiting...")

    def get_prop(self, prop):
        if(prop == 'contacts'):
            return list(map(lambda val: json.loads(decrypt_msg(val, self.__Key)), self.__user['contacts']))
        else:
            return decrypt_msg(self.__user[prop], self.__Key)

    def add_contact(self):
        email = input("Enter users Email: ")
        name = input("Enter users Username: ")
        contacts = self.get_prop('contacts')
        public_key = ""
        found = False
        for Contact in contacts:
            if Contact['email'] == email:
                print(
                    "We already have a Contact under that email. We are going to replace their name.")
                Contact['name'] = name
                found = True
        if not found:
            self.__user['contacts'].append(encrypt_msg(
                json.dumps({'name': name, 'email': email,
                            'public_key': public_key}),
                self.__Key
            )
            )

        self.update_file()

    def whoisthis(self, public_key, hash):
        contacts = self.get_prop('contacts')
        for Contact in contacts:
            hasher = hashlib.sha256()
            hasher.update(public_key.encode())
            hasher.update(Contact['email'].encode())
            if hasher.hexdigest() == hash:
                return Contact['email'], True
        return "NONE", False

    def hashthiscontact(self, email, public_key):
        found = False
        contacts = self.get_prop('contacts')
        for Contact in contacts:
            if Contact['email'] == email:
                hasher = hashlib.sha256()
                hasher.update(public_key.encode())
                hasher.update(Contact['email'].encode())
                found = True
                return hasher.hexdigest()
        if not found:
            print("Not found hashthiscontact")
        self.update_file()

    def saveNetworking(self, pub_key, email):
        contacts = self.get_prop('contacts')
        contact = False
        for index in range(len(contacts)):
            if contacts[index]['email'] == email:
                contact = contacts[index]

        if not contact:
            print("Contact Not Found in saveNetworking")
        else:
            contact['public_key'] = pub_key
            self.__user['contacts'][index] = encrypt_msg(
                json.dumps(contact), self.__Key)
            self.update_file()

    def getNetworking(self, email):
        contacts = self.get_prop('contacts')
        for Contact in contacts:
            if Contact['email'] == email:
                return Contact['public_key']


class Contact():
    def __init__(self, name, email):
        self.__email = email
        self.__name = name
