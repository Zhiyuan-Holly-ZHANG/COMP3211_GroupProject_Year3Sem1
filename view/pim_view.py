class Printer:
    def __init__(self):
        pass

    def main_page(self):
        print("Personal Information Manager (PIM)")
        print("1. Contacts")
        print("2. Events")
        print("3. Take Quick Notes")
        print("4. Tasks")
        print("5. Load File")
        print("9. Exit")

    def contact_page(self):
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Delete Contact")
        print("4. Back to Main Menu")

    def event_page(self):
        print("1. Add Event")
        print("2. View Events")
        print("3. Delete Event")
        print("4. Back to Main Menu")

    def task_page(self):
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Delete Task")
        print("4. Back to Main Menu")

    def note_page(self):
        print("======Take Quick Notes========")
        print("=====Enter ""END"" to END=====")

    def load_page(self):
        print("load your file, makesure it end with .pim")

