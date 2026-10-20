import json
import os

#    ------------- APP FUNCTIONS --------------
class media_tracker:

  def __init__(self):
    self.file_name = "media_data.json" # Creating a JSON file to store all the items, which will preserve data even after program ends 
    self.media_list = [] # Creating an empty python list to store data
    self.load_data()

    
# Loading the data from the JSON file into the media_list attribute of the class. If the file doesn't exist, it will create a new one and start with an empty list.
  def load_data(self): 
    if os.path.exists(self.file_name): # Checking if the file exists or not
      with open(self.file_name, "r") as file: # Opening the file in read mode
        try:
          self.media_list = json.load(file) # Loading the data from the JSON file -> Python List with json.load() method
        except json.decoder.JSONDecodeError:
          # If the file exists but is blank or corrupted, catch the error and reset!
          print("<<< Warning: JSON file was corrupted or empty. Resetting data. >>>")
          self.media_list = []
    else:
      print("<<< No existing saved file found. Starting fresh >>>")
  

  def save_data(self):
    with open(self.file_name,"w") as file: # truncating the file and opening it in write mode
      json.dump(self.media_list, file, indent=4) # Saving the data from Python List -> JSON file with json
  

  def add_title(self, title, status="watched"):
    new_item = {"title": title, "status": status} # Creating a new dictionary item with the title and status which will be added to the media_list
    self.media_list.append(new_item)
    self.save_data()
    print(f"<<< Successfully added '{title}' >>>")
  

  def view_titles(self):
    if len(self.media_list) == 0: # Checking if the list is empty or not
      print("<<< No title found ! Please add new titles first >>>") # Printing a message if the list is empty
      return # Returning from the function if the list is empty, so that the rest of the code doesn't execute
    
    print("\nSaved titles: ")
    for index, item in enumerate(self.media_list, start=1): # Enumerating through the list and printing the index, title and status of each item
      print(f"{index}. {item['title']} - [{item['status']}]")
    

  def remove_title(self, index_to_remove):
    try:
      removed_item = self.media_list.pop(index_to_remove - 1) # Removing the item from the list based on the index provided by the user. Subtracting 1 because list indices start from 0
      self.save_data()
      print(f"Successfully removed '{removed_item['title']}'")

    except Exception: # Handling any other unexpected errors that may occur during the removal process
      print("<<< Error occurred while removing the title. Please try again. >>>")

  
  def search_by_title(self,title):
    for index, item in enumerate(self.media_list, start=1):
      if item["title"].casefold() == title:
        print(f"<<< Found '{item['title']}' at index no.{index} >>>")
        break
    else:
      print(f"<<< No title with name '{title}' found >>>")

  def search_by_status(self,status): 
    category = [item["title"] for item in self.media_list if item["status"] == status]
    if len(category) == 0:
      print(f"<<< No title with status '{status}' found >>>")
    else:
      print(f"\nTitles with status '{status}': ")
      for item in category:
        print(item)

  def clear_all(self):
    self.media_list = []
    self.save_data()
    print("<<< All data cleared successfully >>>")


# It will be added in the new update
  def update_title(self, index, new_title):
    old_title = self.media_list[index - 1]["title"] # Storing the old title before updating it
    self.media_list[index - 1]["title"] = new_title # Updating the title of the item at the specified index
    self.save_data()
    print(f"<<< Successfully updated title from '{old_title}' to '{new_title}' >>>")
    
# It will be added in the new update
  def update_status(self, index, new_status):
    old_status = self.media_list[index - 1]["status"] # Storing the old status before updating it
    self.media_list[index - 1]["status"] = new_status # Updating the status of the item at the specified index
    self.save_data()
    print(f"<<< Successfully updated status from '{old_status}' to '{new_status}' >>>")


# -------------------- MAIN APP EXECUTION ---------------------------- 


print("Welcome to CLI Media Tracker App ")
tracker = media_tracker() # Creating an instance of the media_tracker class to access its methods and attributes
is_running = True

while (is_running):
  print("\n --- Choose any Option --- \n")
  print("1. Add new title \n2. Remove a title \n3. View all titles \n4. Search for a title \n5. Search by status \n6. Clear all data \n7. Exit")
  print("Choose from the above options #enter index no. of the option")
  choice = input("I choose: ").strip()

  if choice == "1":
    
    new_title = input("Enter the title to add: ").strip()
    status = input("Enter the status index(1. watched/2. unwatched/3. watching): ").strip()

    # Map the user's choice to the actual status
    if status == "1":
      status = "watched"
    elif status == "2":
      status = "unwatched"
    elif status == "3":
      status = "watching"
    else:
      print("<<< Invalid status index entered. Please enter a valid option from 1->(watched), 2->(unwatched), 3->(watching). >>>")
      continue # Skipping the rest of the loop and going back to the start of the while loop to ask for a new choice from the user

    tracker.add_title(new_title, status)

  elif choice == "2":
    tracker.view_titles()
    
    if len(tracker.media_list) > 0: # Checking if the list is not empty before asking for index to remove, if empty then no need to ask for index to remove i.e below code will only execute if the list is not empty

      try:
        rem_index = int(input("\nEnter the index of the title to remove: "))  
        if rem_index < 1 or rem_index > len(tracker.media_list): # Checking if the index entered by the user is valid or not
          print(f"<<< Title with index no. {rem_index} doesn't exist. >>>")
        else:
          tracker.remove_title(rem_index)
      except ValueError: # Handling the case where the user enters a non-integer value for the index to remove
        print("<<< Invalid input passed ! Please enter a valid index number i.e only integers >>>")
      except Exception: # Handling any other unexpected errors that may occur during the removal process
        print("<<< Error occurred while removing the title. Please try again. >>>")

  elif choice == "3":
    tracker.view_titles()

  elif choice == "4":
    search_title  = input("Enter the title/name: ")
    tracker.search_by_title(search_title.casefold().strip())
  
  elif choice == "5":
    status = input("Enter the status index(1. watched/2. unwatched/3. watching): ").strip()

    # Map the user's choice to the actual status
    if status == "1":
      status = "watched"
    elif status == "2":
      status = "unwatched"
    elif status == "3":
      status = "watching"
    else:
      print("<<< Invalid status index entered. Please enter a valid option from 1->(watched), 2->(unwatched), 3->(watching). >>>")
      continue
    
    tracker.search_by_status(status)
  
  elif choice == "6":
    tracker.clear_all()

  elif choice == "7":
    is_running = False # Setting the is_running variable to False to exit the while loop and terminate the program
    print("<<< Closing App... Goodbye ! >>>")

  else:
    print("<<< Invalid option entered. Please Try Again ! >>>")