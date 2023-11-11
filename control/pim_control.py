from model.pim_model import Contact
from model.pim_model import Event
from model.pim_model import Task
from model.pim_model import QuickNote
from datetime import datetime, timedelta
from view.pim_view import Printer
import os


class Controller:
    def __init__(self):
        self.printer = Printer()
        self.contact_model = None
        self.event_model = None
        self.task_model = None
        self.note_model = None
        self.load = 0
        self.load_mode = False

    def contact_control(self):
        if not self.load_mode:
            while True:
                choice = input("would you like to name the contact ? (y/n) > ")
                if choice == 'y':
                    name = input("Enter filename start with 'Contacts' > ")
                    if name.startswith('Contacts'):
                        self.load = name + ".pim"
                        break
                    else:
                        print("!!!!!!Not start with 'Contacts' try again!!!!!!")
                elif choice == 'n':
                    break
                else:
                    print("wrong command try again")

        self.contact_model = Contact("Me", "12345678", "me@gmail.com", "home", self.load)
        while True:
            self.contact_model.update()
            self.printer.contact_page()
            choice = input("Enter your choice (1-4): ")
            if choice == "1":
                name = input("Enter name: ")
                phone = input("Enter phone number: ")
                email = input("Enter email address: ")
                address = input("Enter address: ")
                self.contact_model.add_contact(name, phone, email, address)
            elif choice == "2":
                self.contact_model.view()
            elif choice == "3":
                name = input("Enter name of contact to delete: ")
                self.contact_model.delete_item("Name", name)
            elif choice == "4":
                return
            else:
                print("Invalid choice. Please try again.")

    def event_control(self):
        if not self.load_mode:
            while True:
                choice = input("would you like to name the event ? (y/n) > ")
                if choice == 'y':
                    name = input("Enter filename start with 'Events' > ")
                    if name.startswith('Events'):
                        self.load = name + ".pim"
                        break
                    else:
                        print("!!!!!!Not start with 'Events' try again!!!!!!")
                elif choice == 'n':
                    break
                else:
                    print("wrong command try again")

        self.event_model = Event("Group Meeting", "2023-10-24 20:00", "19:50", self.load)
        while True:
            self.event_model.update()
            self.printer.event_page()
            choice = input("Enter your choice (1-4): ")
            if choice == "1":
                description = input("Enter event description: ")
                start_time_str = input("Enter event start time (YYYY-MM-DD HH:MM): ")
                alarm_str = input("Enter event alarm (minutes before start time): ")
                try:
                    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
                    alarm = timedelta(minutes=int(alarm_str))
                    self.event_model.add_event(description, start_time, alarm)
                except ValueError:
                    print("Invalid date/time format. Event not added.")
            elif choice == "2":
                self.event_model.view()
            elif choice == "3":
                description = input("Enter event description to delete: ")
                self.event_model.delete_item("Description", description)
            elif choice == "4":
                return
            else:
                print("Invalid choice. Please try again.")

    def task_control(self):
        if not self.load_mode:
            while True:
                choice = input("would you like to name the task ? (y/n) > ")
                if choice == 'y':
                    name = input("Enter filename start with 'Tasks' > ")
                    if name.startswith('Tasks'):
                        self.load = name + ".pim"
                        break
                    else:
                        print("!!!!!!Not start with 'Tasks' try again!!!!!!")
                elif choice == 'n':
                    break
                else:
                    print("wrong command try again")

        self.task_model = Task("Group Meeting", "2023-10-24 20:00", self.load)
        while True:
            self.task_model.update()
            self.printer.task_page()
            choice = input("Enter your choice (1-4): ")
            if choice == "1":
                description = input("Enter task description: ")
                ddl = input("Enter event deadline (YYYY-MM-DD HH:MM): ")
                try:
                    start_time = datetime.strptime(ddl, "%Y-%m-%d %H:%M")
                    # alarm = timedelta(minutes=int(alarm_str))
                    self.task_model.add_task(description, ddl)
                except ValueError:
                    print("Invalid date/time format. Event not added.")
            elif choice == "2":
                self.task_model.view()
            elif choice == "3":
                description = input("Enter task description to delete: ")
                self.task_model.delete_item("Description", description)
            elif choice == "4":
                return
            else:
                print("Invalid choice. Please try again.")

    def note_control(self):
        if not self.load_mode:
            while True:
                choice = input("would you like to name the note ? (y/n) > ")
                if choice == 'y':
                    name = input("Enter filename start with 'QuickNotes' > ")
                    if name.startswith('QuickNotes'):
                        self.load = name + ".pim"
                        break
                    else:
                        print("!!!!!!Not start with 'QuickNotes' try again!!!!!!")
                elif choice == 'n':
                    break
                else:
                    print("wrong command try again")

        self.printer.note_page()
        self.note_model = QuickNote(self.load)
        self.note_model.makeNote()

    def load_control(self):
        self.load_mode = True
        while True:
            filename = input("enter the file name or 'q' to exit > ")
            if filename == 'q':
                return
            flag = True
            if not filename.endswith('.pim'):
                print("format error : not end with pim")
                flag = False
            file_path = os.path.join(os.path.dirname(__file__), '..', 'PIM_dbs', filename)
            if not os.path.exists(file_path):
                print(f" {filename} not exit in PIM_dbs ")
                flag = False
            if flag:
                break
        self.load = filename
        if filename.startswith("Contacts"):
            print("========load successfully=========")
            self.contact_control()
        elif filename.startswith("Events"):
            print("========load successfully=========")
            self.event_control()
        elif filename.startswith("QuickNotes"):
            print("========load successfully=========")
            self.note_control()
        elif filename.startswith("Tasks"):
            print("========load successfully=========")
            self.task_control()
        else:
            raise SystemError("unknown error occurs")
        self.load_mode = False
