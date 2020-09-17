import os.path
import json
from secure_drop import *

file_path = 'users.json'

def main():
  # FIXME: not handled if no file exists  Solution: if no file exists new_user
  # FIXME: Handle if empty JSON Solution: if  file is empty  new_user
  with open(file_path, 'r') as users_file:
    users = json.load(users_file)  #loading twice. Once here and Once in new_user()/existing_user()

    if(not len(users)): #check if user exists. Should it check if file exist first?
      print("No users are registered with this client.")

      choice = input("Do you want to register a new user (y/n)? ")
      if (choice == 'y') or (choice == 'Y'):
        new_user(users, file_path)
      else:
        print("Goodbye") # and file is empty
        sys.exit()

        # TODO: stub


    else:
      running = True
      while(running):
        # TODO: switch statement that waits for commands
        # Input now handeled in new_user()/existing_user()
        # email = input("Enter Email Address: ")
        # password = input("Enter Password: ")
      
        # Read user from JSON
        print("listener")






if __name__ == "__main__":
    main()
