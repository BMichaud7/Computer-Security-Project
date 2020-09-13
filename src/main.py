import os.path
import json
from secure_drop import *

file_path = 'users.json'

def main():
  # FIXME: not handled if no file exists
  # FIXME: Handle if empty JSON
  with open(file_path, 'r') as users_file:
    users = json.load(users_file)

    if(not len(users)):
      print("No users are registered with this client.")

      choice = input("Do you want to register a new user (y/n)? ")
      if (choice == 'y') or (choice == 'Y'):
        pass
        new_user(users, file_path)
      else:
        print("No users exists") # and file is empty
        # TODO: stub


    else:
      running = True
      while(running):
        # TODO: switch statement that waits for commands
        print("listener")






if __name__ == "__main__":
    main()
