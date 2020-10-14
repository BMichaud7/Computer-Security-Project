import os, sys, json

# Program imports
from secure_drop import *

def main():
  # If file doesn't exists or doesn't have brackets create file and/or add []
  if not os.path.exists(users_path) or os.path.getsize(users_path) < 2:
    set_json(users_path, 0o640, '[]')

  # load users from JSON
  try:
    with open(users_path, 'r') as users_file:
      users = json.load(users_file)
  except IOError:
    print("Error:", IOError)
    print("Couldn't open", users_path, "\nExiting...")
    sys.exit()

  #if no users exists, ask user to create one
  if(not len(users)):
    choice = input("No users exists, Would you like to create a new user (Y/n)? ")
    if (choice == "y") or (choice == "Y"):
      new_user(users_path, users)
    else:
      print("At least one user must exists to use Secure Drop\n", "Exiting Secure Drop")
      sys.exit()
  else:
    # Login
    User = login(users)

    # Main Program Loop
    print("\nWelcome to SecureDrop")
    choice = input('Type "help" For list of commands and "exit" to quit \n#')
    while(True):
      if choice == "help":
        print('"add"  -> Add a new contact')
        print('"list" -> List all online contacts')
        print('"send" -> Transfer file to contact')
        print('"exit" -> Exit SecureDrop')
        print()
      elif choice == "add":
        # Enter some contact info
        User.add_contact("Hello2")
      elif choice == "list":
        contacts = User.get_prop('contacts')
        if(len(contacts)):
          print("Contacts:")
          for contact in contacts:
            print("  -", contact)
        else:
          print("No contacts exist")

      elif choice == "send":
        send(cred)
      elif choice == "exit":
        print("Exiting SecureDrop")
        sys.exit()
      else:
        print(choice, 'is an invalid option, type "help" for a list of commands')

      choice = input("\n# ")

if __name__ == "__main__":
    main()
