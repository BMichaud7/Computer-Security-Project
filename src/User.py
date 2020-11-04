import os, sys, json

def encrypt_msg(msg, Fernet):
    return Fernet.encrypt(msg.encode()).decode()

def decrypt_msg(msg, Fernet):
    return Fernet.decrypt(msg.encode()).decode()

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
            print("Error:", IOError, "\nFailed to read from", self.__path, "\nExiting...")

        try:
            with open(self.__path, 'w') as curr_file:
                users[self.__index] = self.__user
                json.dump(users, curr_file)
        except IOError:
            print("Error:", IOError, "\nFailed to write to", self.__path, "\nExiting...")

    def get_prop(self, prop):
        if(prop == 'contacts'):
            return list(map(lambda val:json.loads(decrypt_msg(val, self.__Key)), self.__user['contacts']))
        else:
            return decrypt_msg(self.__user[prop], self.__Key)

    def add_contact(self):
        email = input("Enter users Email: ")
        name = input("Enter users Username: ")
        contacts = self.get_prop('contacts')
        found = False
        for Contact in contacts:
           if Contact['email'] == email:
               print("We already have a Contact under that email. We are going to replace their name.")
               Contact['name'] = name
               found = True
        if  not found:
            self.__user['contacts'].append(encrypt_msg(
                    json.dumps({ 'name': name, 'email': email }),
                    self.__Key
                )
            )

        self.update_file()


class Contact():
   def __init__(self,name,email):
        self.__email = email
        self.__name = name

