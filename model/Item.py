from datetime import datetime
import os


# This is the super class Item, its subclasses are Contacts, Events, Notes and Tasks

# if user want to name the file, init function set filename to be input filename
# if they don't want, init function set filename to be the current date
class Item:
    def __init__(self, pir, load):
        self.load = load
        if load == 0:
            filename = f"{pir}_{datetime.now().strftime('%Y-%m-%d')}.pim"
            self.filename = os.path.join(os.path.dirname(__file__), '..', 'PIM_dbs', filename)
            with open(self.filename, "a") as f:
                pass
        else:
            self.filename = os.path.join(os.path.dirname(__file__), '..', 'PIM_dbs', load)
            with open(self.filename, "a") as f:
                pass

        self.list = []

    # save file
    def save_to_file(self, item_data):
        with open(self.filename, "a") as f:
            for key, value in item_data.items():
                f.write(f"{key}: {value}\n")
            f.write("------------------\n")
        print(f"{type(self).__name__} added successfully.")

    # view function, print out the information of a certain pir file
    def view(self):
        try:
            file1 = open(self.filename, 'r')
            Lines = file1.readlines()
            for line in Lines:
                print(line)
        except FileNotFoundError:
            print(FileNotFoundError)

    # delete a certain ocation by a title(description, name, etc.)
    def delete_item(self, title, identifier):
        with open(self.filename, 'r') as file:
            items_data = file.read()

        # split different blocks
        items_blocks = items_data.split("------------------\n")
        items_to_delete = f"{title}: {identifier}\n"
        items_to_keep = []

        for item in items_blocks:
            if not item.startswith(items_to_delete):
                items_to_keep.append(item)

        # if the deleted file remain same as before indicates that no deletion
        if len(items_to_keep) == len(items_blocks):
            print(f"{type(self).__name__} not found.")
            return

        # update new
        with open(self.filename, 'w') as file:
            for item in items_to_keep:
                if item.strip() != "":
                    file.write(item)
                    file.write("------------------\n")

        print(f"{type(self).__name__} deleted successfully.")
        file.close()

    # this function is essential to the system, it read the information from the DBS(PIM_dbs) and update the information
    def update(self):
        self.list = []  # Clear the current items list to avoid duplicates
        try:
            with open(self.filename, 'r') as file:
                item_data = {}
                for line in file:
                    if '------------------' in line:  # '------------------' make a clear boundary between every pir
                        if item_data:
                            self.list.append(self.create_item(item_data))
                            item_data = {}
                    else:
                        key, value = line.strip().split(': ')
                        item_data[key] = value
        except FileNotFoundError:
            print(f"The file {self.filename} was not found.")

    # an abstract method that need to be overriden by subclass
    def create_item(self, item_data):
        raise NotImplementedError("must be overriden")
