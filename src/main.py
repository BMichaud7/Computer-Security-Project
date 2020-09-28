import os.path
import sys
import json
from secure_drop import *
import string
import os, sys, stat
import subprocess 
import shutil

file_path = 'users.json'

def main():
  # FIXME: not handled if no file exists  Solution: if no file exists new_user
  # FIXME: Handle if empty JSON Solution: if  file is empty  new_user
  #users

  # If file doesn't exists or doesn't have brackets create file and/or add []
  if not os.path.exists(file_path) or os.path.getsize(file_path) < 2:
    try:
      with open(file_path, 'w+') as users_file:
        users_file.write("[]")
    except IOError:
      print("Error:", IOError)
      print("Couldn't create/format", file_path, "\nExiting...")
      sys.exit()

  # load users from JSON
  try:
    with open(file_path, 'r') as users_file:
      users = json.load(users_file)  #loading twice, here & in new_user()/existing_user()
  except IOError:
    print("Error:", IOError)
    print("Couldn't open/create", file_path, "\nExiting...")
    sys.exit()

  #if no users exists, ask user to create one
  if(not len(users)):
    print("No users exists")
    choice = raw_input("Would you like to create a new user (y/n)? ")
    if (choice == "y") or (choice == "Y"):
      new_user(users, file_path)
      setfile(file_path)
      #print("Yes")
    else:
      print("At least one user must exists to use Secure Drop")
      print("Exiting Secure Drop")
      sys.exit()
  else:
    #TODO: login loop here
    existing_usersusers, file_path)
    running = True
    #while(running):
      # TODO: switch statement that waits for commands
      # Input now handeled in new_user()/existing_user()
      # email = input("Enter Email Address: ")
      # password = input("Enter Password: ")

      # Read user from JSON
     






if __name__ == "__main__":
    main()
