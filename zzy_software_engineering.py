from datetime import datetime, timedelta


class Contact:
    def __init__(self, name, phone, email, address):
        self.contacts = []
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.filename = f"Contacts_{self.current_date}.pim"
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def update(self):
        self.contacts = []  # Clear the current contacts list to avoid duplicates

        try:
            with open(self.filename, 'r') as file:
                contact_info = {}
                for line in file:
                    # Check if the line is a separator line
                    if '------------------' in line:
                        if contact_info:  # If contact_info is not empty
                            new_contact = Contact(contact_info['Name'], contact_info['Phone'], contact_info['Email'],
                                                  contact_info['Address'])
                            self.contacts.append(new_contact)
                            contact_info = {}  # Reset the dictionary for the next contact
                    else:
                        # Split the line by ': ' to get the key-value pair
                        key, value = line.strip().split(': ')
                        contact_info[key] = value  # Update the dictionary with contact details
        except FileNotFoundError:
            print(f"The file {self.filename} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def __str__(self):
        return f"Name: {self.name}\nPhone: {self.phone}\nEmail: {self.email}\n"

    def add_contact(self, name, phone, email, address):
        contact = Contact(name, phone, email, address)
        self.contacts.append(contact)
        with open(self.filename, "a") as f:
            f.write(f"Name: {contact.name}\n")
            f.write(f"Phone: {contact.phone}\n")
            f.write(f"Email: {contact.email}\n")
            f.write(f"Address: {contact.address}\n")
            f.write("------------------\n")
        print("Contact added successfully.")
        f.close()
        self.update()

    def view_contacts(self):
        try:
            file1 = open(self.filename, 'r')
            Lines = file1.readlines()

            for line in Lines:
                print(line)
        except FileNotFoundError:
            print(FileNotFoundError)

    def delete_contact(self, name_to_delete):
        # 先读取当前文件中所有的联系人
        try:
            with open(self.filename, 'r') as file:
                contacts_data = file.read()
        except FileNotFoundError:
            print("File not found.")
            return

        # 分割每个联系人块，并确定要删除的联系人块
        contacts_blocks = contacts_data.split("------------------\n")
        contact_to_delete = f"Name: {name_to_delete}\n"
        updated_contacts = []

        for contact in contacts_blocks:
            if not contact.startswith(contact_to_delete):
                updated_contacts.append(contact)

        # means noting deleted then error
        if len(updated_contacts) == len(contacts_blocks):
            print("Contact not found.")
            return

        # 写入更新后的联系人列表到文件
        with open(self.filename, 'w') as file:
            for contact in updated_contacts:
                if contact.strip() != "":
                    file.write(contact)
                    file.write("------------------\n")

        print("Contact deleted successfully.")

    def choices(self):
        while True:
            self.update()
            print("1. Add Contact")
            print("2. View Contacts")
            print("3. Delete Contact")
            print("4. Back to Main Menu")
            choice = input("Enter your choice (1-4): ")
            if choice == "1":
                name = input("Enter name: ")
                phone = input("Enter phone number: ")
                email = input("Enter email address: ")
                address = input("Enter address: ")
                self.add_contact(name, phone, email, address)
            elif choice == "2":
                self.view_contacts()
            elif choice == "3":
                name = input("Enter name of contact to delete: ")
                self.delete_contact(name)
            elif choice == "4":
                return
            else:
                print("Invalid choice. Please try again.")


class Event:
    def __init__(self, description, start_time, alarm):
        self.events = []
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.filename = f"Events_{self.current_date}.pim"
        self.description = description
        self.start_time = start_time
        self.alarm = alarm

    def __str__(self):
        return f"Description: {self.description}\nStart Time: {self.start_time}\nAlarm: {self.alarm}\n"

    def add_event(self, description, start_time, alarm):
        event = Event(description, start_time, alarm)
        self.events.append(event)
        with open(self.filename, "a") as f:
            f.write(f"Description: {event.description}\n")
            f.write(f"Start Time: {event.start_time}\n")
            f.write(f"Alarm: {event.alarm}\n")
            f.write("------------------\n")
        print("Event added successfully.")
        f.close()

    def view_events(self):
        try:
            file1 = open(self.filename, 'r')
            Lines = file1.readlines()
            for line in Lines:
                print(line)
        except FileNotFoundError:
            print(FileNotFoundError)

    def delete_event(self, description):
        found_events = [event for event in self.events if event.description.lower() == description.lower()]
        if len(found_events) > 0:
            self.events.remove(found_events[0])
            print("Event deleted successfully.")
        else:
            print("Event not found.")

    @staticmethod
    def choices():
        e = Event("Group Meeting", "20:00", "19:50")
        print("1. Add Event")
        print("2. View Events")
        print("3. Delete Event")
        print("4. Back to Main Menu")
        choice = input("Enter your choice (1-4): ")
        if choice == "1":
            description = input("Enter event description: ")
            start_time_str = input("Enter event start time (YYYY-MM-DD HH:MM): ")
            alarm_str = input("Enter event alarm (minutes before start time): ")
            try:
                start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
                alarm = timedelta(minutes=int(alarm_str))
                e.add_event(description, start_time, alarm)
            except ValueError:
                print("Invalid date/time format. Event not added.")
        elif choice == "2":
            e.view_events()
        elif choice == "3":
            description = input("Enter event description to delete: ")
            e.delete_event(description)
        elif choice == "4":
            return
        else:
            print("Invalid choice. Please try again.")


class Task:
    def __init__(self, description, ddl):
        self.tasks = []
        self.description = description
        self.ddl = ddl
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.filename = f"Tasks_{self.current_date}.pim"

    def add_task(self, description, ddl):
        task = Task(description, ddl)
        self.tasks.append(task)
        with open(self.filename, "a") as f:
            f.write(f"Description: {task.description}\n")
            f.write(f"Deadline: {task.ddl}\n")
            f.write("------------------\n")
        print("Task added successfully.")
        f.close()

    def view_task(self):
        try:
            file1 = open(self.filename, 'r')
            Lines = file1.readlines()
            for line in Lines:
                print(line)
        except FileNotFoundError:
            print(FileNotFoundError)

    def delete_task(self, description):
        found_tasks = [task for task in self.tasks if task.description.lower() == description.lower()]
        if len(found_tasks) > 0:
            self.tasks.remove(found_tasks[0])
            print("Event deleted successfully.")
        else:
            print("Event not found.")

    @staticmethod
    def choices():
        e = Task("Group Meeting", "2023-10-24 20:00")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Delete Task")
        print("4. Back to Main Menu")
        choice = input("Enter your choice (1-4): ")
        if choice == "1":
            description = input("Enter task description: ")
            ddl = input("Enter event deadline (YYYY-MM-DD HH:MM): ")
            try:
                start_time = datetime.strptime(ddl, "%Y-%m-%d %H:%M")
                # alarm = timedelta(minutes=int(alarm_str))
                e.add_task(description, ddl)
            except ValueError:
                print("Invalid date/time format. Event not added.")
        elif choice == "2":
            e.view_task()
        elif choice == "3":
            description = input("Enter task description to delete: ")
            e.delete_task(description)
        elif choice == "4":
            return
        else:
            print("Invalid choice. Please try again.")


class QuickNote:
    def __init__(self):
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"QuickNotes_{self.current_date}.pim"
        QNote = input("======Take Quick Notes======\n")
        try:
            file1 = open(filename, 'w')
            file1.write(QNote)
        except FileNotFoundError:
            print(FileNotFoundError)


def main():
    c = Contact("Me", "12345678", "me@gmail.com", "home")
    e = Event("Group Meeting", "2023-10-24 20:00", "19:50")
    t = Task("Group Meeting", "2023-10-24 20:00")
    while True:
        print("Personal Information Manager (PIM)")
        print("1. Contacts")
        print("2. Events")
        print("3. Take Quick Notes")
        print("4. Tasks")
        print("9. Exit")
        choice0 = input("Enter your choice (1-4, 9): ")
        if choice0 == "1":
            c.choices()
        elif choice0 == "2":
            e.choices()
        elif choice0 == "3":
            QuickNote()
        elif choice0 == "4":
            t.choices()
        elif choice0 == "9":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
