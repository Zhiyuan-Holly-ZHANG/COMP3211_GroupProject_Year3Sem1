from model.Contacts import Contact
from model.Events import Event
from model.Tasks import Task
from model.Notes import QuickNote
from datetime import datetime, timedelta
from view.pim_view import Printer
from model.Search import Searching
import os
import re


# the Controller class is responsible to respond to user's input and take corresponding actions by
# creating the associate  control class to call the operation in Model section to handle with the database
# in the init function, it initiates all the control model that will be used by the system
class Controller:
    def __init__(self):
        self.printer = Printer()
        self.contact_model = None
        self.event_model = None
        self.task_model = None
        self.note_model = None
        self.load = 0
        self.load_mode = False  # to identify the current mode, if it is load from dbs, or it is firs time being created
        self.search_model = None

    # create control to handle contacts request
    def contact_control(self):
        if not self.load_mode:
            while True:
                choice = input("Would you like to self define the contact filename? (y/n) > ")
                if choice.lower() == 'y':
                    name = input("Enter filename start with 'Contacts' > ")
                    if name.startswith('Contacts'):
                        self.load = name + ".pim"
                        break
                    else:
                        print("!!!!!!Not start with 'Contacts' try again!!!!!!")
                elif choice.lower() == 'n':
                    break
                else:
                    print("wrong command try again")

        # while the input valid initiates the Contacts class
        self.contact_model = Contact("Me", "12345678", "me@gmail.com", "home", self.load)
        while True:
            # reload information every time an operation is done
            self.contact_model.update()
            # print out information of the choice
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

    # create control to handle contacts request
    def event_control(self):
        if not self.load_mode:
            while True:
                choice = input("would you like to name the event ? (y/n) > ")
                if choice.lower() == 'y':
                    name = input("Enter filename start with 'Events' > ")
                    if name.startswith('Events'):
                        self.load = name + ".pim"
                        break
                    else:
                        print("!!!!!!Not start with 'Events' try again!!!!!!")
                elif choice.lower() == 'n':
                    break
                else:
                    print("wrong command try again")
        # while the input valid initiates the Events class
        self.event_model = Event("Group Meeting", "2023-10-24 20:00", "19:50", self.load)
        while True:
            self.event_model.update()
            # print out information of the choice
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

    # create control to handle tasks request
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
            # print out information of the choice
            self.printer.task_page()
            choice = input("Enter your choice (1-4): ")
            if choice == "1":
                description = input("Enter task description: ")
                ddl = input("Enter event deadline (YYYY-MM-DD HH:MM): ")
                try:
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

    # create control to handle QuickNotes request
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
        # notify the start of the note
        self.printer.note_page()
        self.note_model = QuickNote(self.load)
        self.note_model.makeNote()

    # different from the above functions, load_control is another load mode, it calls the the method in Controller class
    # not in Model section
    # the input is the filename
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

    # this function handle with keywords search, it identify the operators(!,||,&&)
    # identify also keywords
    # return the matching file list
    def logic_search(self, cmd, types):
        self.search_model = Searching(types)

        all_files = set(self.search_model.search_string(''))

        operands = []
        operators = []
        tokens = cmd.split()
        for token in tokens:
            if token == '!':
                operators.append(token)
            elif token == '&&' or token == '||':

                while operators and operators[-1] == '&&':
                    self.apply_operator(operands, operators, all_files)
                operators.append(token)
            else:

                if operators and operators[-1] == '!':

                    files = set(self.search_model.search_string(token))
                    operands.append(all_files - files)
                    operators.pop()
                else:
                    files = set(self.search_model.search_string(token))
                    operands.append(files)

        while operators:
            self.apply_operator(operands, operators, all_files)

        return list(operands[-1])

    # this the inside logic of handle operators with a stack
    def apply_operator(self, operands, operators, all_files):
        operator = operators.pop()
        if operator == '&&':
            right = operands.pop()
            left = operands.pop()
            operands.append(left & right)
        elif operator == '||':
            right = operands.pop()
            left = operands.pop()
            operands.append(left | right)
        elif operator == '!':

            subset = operands.pop()
            operands.append(all_files - subset)

    # this function handle with keywords search, it identify the operators(!,||,&&)
    # identify also keywords (>,=,< with date YYYY-MM-DD HH:MM)
    # return the matching file list
    def logic_date(self, expression, types):
        flag = True  # indicate if there is a mistake in query
        self.search_model = Searching(types)
        # get all file
        all_files = set(self.search_model.search_string(''))

        operands = []
        operators = []
        logic_operators = ['&&', '||', '!']
        tokens = []
        buffer = ''
        i = 0

        # traverse all logic expression
        while i < len(expression):

            if expression[i:i + 2] in logic_operators:
                if buffer: tokens.append(buffer)
                tokens.append(expression[i:i + 2])
                buffer = ''
                i += 2

            elif expression[i] in logic_operators:
                if buffer: tokens.append(buffer)
                tokens.append(expression[i])
                buffer = ''
                i += 1
            else:
                buffer += expression[i]
                i += 1

        if buffer:
            tokens.append(buffer)

        tokens = [token.strip() for token in tokens]
        for token in tokens:
            if token == '!':
                operators.append(token)
            elif token == '&&' or token == '||':

                while operators and operators[-1] == '&&':
                    self.apply_operator(operands, operators, all_files)
                operators.append(token)
            else:
                # check for keywords
                # check if meet with the format: >,=,< with date YYYY-MM-DD HH:MM
                pattern = r'[><=]\s\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}'
                match = re.match(pattern, token)
                if match is None:
                    print("Invalid query,check again")
                    flag = False
                    return None, flag

                if operators and operators[-1] == '!':

                    files = set(self.search_model.search_date(token))
                    operands.append(all_files - files)
                    operators.pop()
                else:
                    files = set(self.search_model.search_date(token))
                    operands.append(files)

        while operators:
            self.apply_operator(operands, operators, all_files)

        return list(operands[-1]), flag

    # handle with user input and call search to search keywords
    def select(self, choice):
        cmd = input("input keywords (support !, ||, &&): ")
        find = self.logic_search(cmd, choice)
        if len(find) == 0:
            print("file not found")
        else:
            print("file find as follows: ")
            print(find)

    # handle with user input and call search to search time
    def select_time(self, choice):
        while True:
            cmd = input("enter time constraint with <, >, = (YYYY-MM-DD HH:MM)(support || &&): ")
            find, flag = self.logic_date(cmd, choice)
            if flag:
                if len(find) == 0:
                    print("file not found")
                else:
                    print("file find as follows: ")
                    print(find)
                break

    # create a search control first ask user input what kind of pir to search
    # than respond following operation with respect to the kinds
    def search_control(self):
        while True:
            choice1 = input("input type of pir you want to search quit(q): ")
            if choice1.lower() in ['contacts', 'quicknotes']:
                self.select(choice1)
            elif choice1.lower() in ['tasks', 'events']:
                while True:
                    if choice1.lower() == 'events':
                        print("1)search by keywords 2)search by start time : ")
                    else:
                        print("1)search by keywords  2)search by DDL : ")
                    choice2 = input()
                    if choice2 == '1':
                        self.select(choice1)
                        break
                    elif choice2 == '2':
                        self.select_time(choice1)
                        break
                    else:
                        print("wrong command, try again")
            elif choice1.lower() == 'q':
                return
            else:
                print("wrong command, try again")
