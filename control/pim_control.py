from model.pim_model import Contact
from model.pim_model import Event
from model.pim_model import Task
from model.pim_model import QuickNote
from datetime import datetime, timedelta
from view.pim_view import Printer


class Controller:
    def __init__(self):
        self.printer = Printer()
        self.contact_model = None
        self.event_model = None
        self.task_model = None
        self.note_model = None

    def contact_control(self):
        self.contact_model = Contact("Me", "12345678", "me@gmail.com", "home")
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
        self.event_model = Event("Group Meeting", "2023-10-24 20:00", "19:50")
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
        self.task_model = Task("Group Meeting", "2023-10-24 20:00")
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
        self.printer.note_page()
        self.note_model = QuickNote()
        self.note_model.makeNote()
