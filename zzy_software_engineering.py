from datetime import datetime, timedelta


class Item:
    def __init__(self, filename):
        self.filename = f"{filename}_{datetime.now().strftime('%Y-%m-%d')}.pim"
        self.list = []

    def save_to_file(self, item_data):
        with open(self.filename, "a") as f:
            for key, value in item_data.items():
                f.write(f"{key}: {value}\n")
            f.write("------------------\n")
        print(f"{type(self).__name__} added successfully.")
        f.close()

    def view(self):
        try:
            file1 = open(self.filename, 'r')
            Lines = file1.readlines()
            for line in Lines:
                print(line)
        except FileNotFoundError:
            print(FileNotFoundError)

    def delete_item(self, title, identifier):
        # 读取当前文件中所有的条目
        try:
            with open(self.filename, 'r') as file:
                items_data = file.read()
        except FileNotFoundError:
            print("File not found.")
            return

        # 分割每个条目块，并确定要删除的条目块
        items_blocks = items_data.split("------------------\n")
        items_to_delete = f"{title}: {identifier}\n"
        items_to_keep = []

        for item in items_blocks:
            if not item.startswith(items_to_delete):
                items_to_keep.append(item)

        # 如果更新后的列表长度等于原来的长度，说明没有条目被删除
        if len(items_to_keep) == len(items_blocks):
            print(f"{type(self).__name__} not found.")
            return

        # 写入更新后的条目列表到文件
        with open(self.filename, 'w') as file:
            for item in items_to_keep:
                if item.strip() != "":
                    file.write(item)
                    file.write("------------------\n")

        print(f"{type(self).__name__} deleted successfully.")
        file.close()

    def update(self):
        self.list = []  # Clear the current items list to avoid duplicates
        try:
            with open(self.filename, 'r') as file:
                item_data = {}
                for line in file:
                    if '------------------' in line:
                        if item_data:
                            self.list.append(self.create_item(item_data))
                            item_data = {}
                    else:
                        key, value = line.strip().split(': ')
                        item_data[key] = value
        except FileNotFoundError:
            print(f"The file {self.filename} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # an abstract method that need to be overriden by subclass
    def create_item(self, item_data):
        raise NotImplementedError("must be overriden")


class Contact(Item):
    def __init__(self, name, phone, email, address):
        super().__init__("Contacts")
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def __str__(self):
        return f"Name: {self.name}\nPhone: {self.phone}\nEmail: {self.email}\n"

    def create_item(self, item_data):
        return Contact(item_data['Name'], item_data['Phone'], item_data['Email'], item_data['Address'])

    def add_contact(self, name, phone, email, address):
        event_data = {
            "Name": name,
            "Phone": phone,
            "Email": email,
            "Address": address
        }
        self.save_to_file(event_data)
        self.update()

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
                self.view()
            elif choice == "3":
                name = input("Enter name of contact to delete: ")
                self.delete_item("Name", name)
            elif choice == "4":
                return
            else:
                print("Invalid choice. Please try again.")


class Event(Item):
    def __init__(self, description, start_time, alarm):
        super().__init__("Events")
        self.description = description
        self.start_time = start_time
        self.alarm = alarm

    def __str__(self):
        return f"Description: {self.description}\nStart Time: {self.start_time}\nAlarm: {self.alarm}\n"

    def create_item(self, item_data):
        return Event(item_data['Description'], item_data['Start Time'], item_data['Alarm'])

    def add_event(self, description, start_time, alarm):
        event_data = {
            "Description": description,
            "Start Time": start_time,
            "Alarm": alarm
        }
        self.save_to_file(event_data)
        self.update()

    def choices(self):
        while True:
            self.update()
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
                    self.add_event(description, start_time, alarm)
                except ValueError:
                    print("Invalid date/time format. Event not added.")
            elif choice == "2":
                self.view()
            elif choice == "3":
                description = input("Enter event description to delete: ")
                self.delete_item("Description", description)
            elif choice == "4":
                return
            else:
                print("Invalid choice. Please try again.")


class Task(Item):
    def __init__(self, description, ddl):
        super().__init__("Tasks")
        self.description = description
        self.ddl = ddl

    def add_task(self, description, ddl):
        event_data = {
            "Description": description,
            "DDL": ddl
        }
        self.save_to_file(event_data)
        self.update()

    def create_item(self, item_data):
        return Task(item_data['Description'], item_data['DDL'])

    def choices(self):
        while True:
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
                    self.add_task(description, ddl)
                except ValueError:
                    print("Invalid date/time format. Event not added.")
            elif choice == "2":
                self.view()
            elif choice == "3":
                description = input("Enter task description to delete: ")
                self.delete_item("Description", description)
            elif choice == "4":
                return
            else:
                print("Invalid choice. Please try again.")


class QuickNote(Item):
    def __init__(self):
        super().__init__("QuickNotes")
        QNote = input("======Take Quick Notes======\n")
        try:
            file1 = open(self.filename, 'w')
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
