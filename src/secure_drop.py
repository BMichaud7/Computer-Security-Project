import json
from cryptography.fernet import Fernet

def new_user(users, file_path):
    # FIXME: try catch block is poorly scoped
    # try:
        with open(file_path, 'w') as users_file:
            name = input("Select a username: ")
            email = input("Enter Email Address: ")

            key = Fernet.generate_key()
            fernet_instance = Fernet(key)
            password = fernet_instance.encrypt(input("Create Password: ").encode('utf-8')).decode('utf-8')

            users.append({ 'name': name, 'email': email, 'password': password })

            json.dump(users, users_file)

            # TODO: create a key file or whatever we want to do with the key

    # except:
    #    print("ERROR: Unable to open ", file_path, " while creating a new user")


