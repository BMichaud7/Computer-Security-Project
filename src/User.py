import os
import sys
import json
import hashlib
from cryptography.fernet import Fernet, InvalidToken

#used to encrypt_msg and decrypt_msg
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

#user class def
class User():
    def __init__(self, index, user, users_path, Fernet ,email ,public_key ,private__key):
        self.__index = index
        self.__user = user
        self.__path = users_path
        self.__Key = Fernet
        self.__email = email
        self.__public_key = public_key
        self.__private_key = private__key


#updates user.json file with new data if changed
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
#returns contact array
    def get_prop(self, prop):
        if(prop == 'contacts'):
            return list(map(lambda val: json.loads(decrypt_msg(val, self.__Key)), self.__user['contacts']))
        else:
            return decrypt_msg(self.__user[prop], self.__Key)
#called to add contact. Checks if contact exits with same eamil. if they do it raplect their name.
    def add_contact(self):
        email = input("Enter users Email: ")
        name = input("Enter users Name: ")
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
                            'public_key': public_key, 'ip': {}}),
                self.__Key
            )
            )

        self.update_file()
        # print("IN SAVE: ", self.get_prop('contacts'))
#saves networking info based on eami. this is used in list.
    def tempdef(self,pub_key, email, ip):
        # print("IN TEMPDEF")
        print(self.get_prop('contacts'))
        contacts = self.get_prop('contacts')
        contact = False
        foundindex = None
        for index in range(len(contacts)):
            if contacts[index]['email'] == email:
                foundindex = index
                contact = contacts[index]
        # print("AFTER LOOP: " , self.get_prop('contacts'))
        if not contact:
            print("Contact Not Found in saveNetworking")
        else:
            # print("CONTACT: ",contact)
            contact['public_key'] = pub_key
            contact['ip'] = ip
            self.__user['contacts'][foundindex] = encrypt_msg(
                json.dumps(contact), self.__Key)
            # print("B UPDATE FILE: " , self.get_prop('contacts'))
            self.update_file()
        # print("IN TEMPDEF END: " , self.get_prop('contacts'))
    #given an ip returns name of contact       
    def whoisthisip(self,ip):
        contacts = self.get_prop('contacts')
        print ("Contacts: ", contacts)
        name = None
        for Contact in contacts:
            if Contact['ip'] == ip:
                name = Contact['name']
        # print("DONE WITH LOOP")
        if name == None:
            return "Unknown"
        else:
            return name

#given a ip and public_key and hash returns name of conact. This is used in list
    def whoisthis(self, public_key, hash,ip):
        # print("public_key: ", public_key)
        contacts = self.get_prop('contacts')
        match = False
        email = None
        pub_key = None
        address = None
        # print("self.get_prop('contacts'): ", self.get_prop('contacts'))
        for Contact in contacts:
            hasher = hashlib.sha256()
            hasher.update(public_key.encode())
            hasher.update(Contact['email'].encode())
            # print("HASH: ", hash, " hasher.hexdigest(): " , hasher.hexdigest())
            # print(hasher.hexdigest() == hash)
            # print(Contact['email'])
            if hasher.hexdigest() == hash:
                # print("BEFORE")
                # self.tempdef(public_key,Contact['email'],ip)
                # # print("AFTER")  
                # # print("self.get_prop('contacts'): ", self.get_prop('contacts'))
                # return Contact['email'], True
                match = True
                pub_key = public_key
                email = Contact['email']
                address = ip
        if match:
            print("SAVING NAME: ", email )
            self.tempdef(pub_key,email,address)
                # print("AFTER")  
                # print("self.get_prop('contacts'): ", self.get_prop('contacts'))
            return email, True
        else:
            return "NONE", False
    #given wmail and public key makes hash of contact. This is used in list to varify identity of person send packets. 
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

    #this gets networing info based on the save. This is used in send.
    def getNetworking(self, email):
        contacts = self.get_prop('contacts')
        for Contact in contacts:
            if Contact['email'] == email:
                return Contact['public_key'], Contact['ip']
        return None,None
    #gets your email public key and private key. 
    def getCred(self):
        return self.__email, self.__public_key, self.__private_key


class Contact():
    def __init__(self, name, email):
        self.__email = email
        self.__name = name