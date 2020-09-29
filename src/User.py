from Contact import *
class Credentials():

    def __init__(self,name,email,contact):
        self.__email = email
        self.__name = name
        self.__contacts = contact #list of Contacts
            # getter method 
    def get_email(self): 
        return self.__email 
      
    # setter method 
    def set_email(self, email): 
        self.__email = email 
            # getter method 
    def get_name(self): 
        return self.__name 
      
    # setter method 
    def set_name(self, name): 
        self.__name = name 
            # getter method 
    def get_contact(self): 
        return self.__contacts 
      
    # setter method 
    def set_contact(self, contacts): 
        self.__contacts = contacts 
        
        

class Contact():
   def __init__(self,name,email):
        self.__email = email
        self.__name = name

