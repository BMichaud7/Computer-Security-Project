def encrypt_msg(msg, Fernet):
    return Fernet.encrypt(msg.encode()).decode()

def decrypt_msg(msg, Fernet):
    return Fernet.decrypt(msg.encode()).decode()

class User():
    def __init__(self, user, Fernet):
        self.__user = user
        self.__Key = Fernet

    def get_prop(self, prop):
        if(prop == 'contacts'):
            return list(map(lambda val:decrypt_msg(val, self.__Key), self.__user['contacts']))
        else:
            return decrypt_msg(self.__user[prop], self.__Key)

    def add_contact(self, contact):
        self.__user['contacts'].append(encrypt_msg(contact, self.__Key))
        print(self.__user['contacts'])


class Contact():
   def __init__(self,name,email):
        self.__email = email
        self.__name = name

