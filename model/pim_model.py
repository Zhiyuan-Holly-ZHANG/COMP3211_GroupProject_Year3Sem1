from datetime import datetime
import os


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

    def save_to_file(self, item_data):
        with open(self.filename, "a") as f:
            for key, value in item_data.items():
                f.write(f"{key}: {value}\n")
            f.write("------------------\n")
        print(f"{type(self).__name__} added successfully.")

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
    def __init__(self, name, phone, email, address, load):
        super().__init__("Contacts", load)
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def __str__(self):
        return f"Name: {self.name}\nPhone: {self.phone}\nEmail: {self.email}\n"

    def create_item(self, item_data):
        return Contact(item_data['Name'], item_data['Phone'], item_data['Email'], item_data['Address'], self.load)

    def add_contact(self, name, phone, email, address):
        event_data = {
            "Name": name,
            "Phone": phone,
            "Email": email,
            "Address": address
        }
        self.save_to_file(event_data)
        self.update()


class Event(Item):
    def __init__(self, description, start_time, alarm, load):
        super().__init__("Events", load)
        self.description = description
        self.start_time = start_time
        self.alarm = alarm

    def __str__(self):
        return f"Description: {self.description}\nStart Time: {self.start_time}\nAlarm: {self.alarm}\n"

    def create_item(self, item_data):
        return Event(item_data['Description'], item_data['Start Time'], item_data['Alarm'], self.load)

    def add_event(self, description, start_time, alarm):
        event_data = {
            "Description": description,
            "Start Time": start_time,
            "Alarm": alarm
        }
        self.save_to_file(event_data)
        self.update()


class Task(Item):
    def __init__(self, description, ddl, load):
        super().__init__("Tasks", load)
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
        return Task(item_data['Description'], item_data['DDL'], self.load)


class QuickNote(Item):
    def __init__(self, load):
        super().__init__("QuickNotes", load)

    def makeNote(self):
        QNote = []
        flag = True
        while True:
            line = input()
            if line.strip() == 'END':
                confirm = input("Save(s) | Continue(c) | Quit without save(q)")
                if confirm.lower() == 's':
                    break
                elif confirm.lower() == 'q':
                    flag = False
                    break
                else:
                    print("=====continue=======")

            else:
                QNote.append(line)


        if flag:
            note_text = '\n'.join(QNote)
            try:
                with open(self.filename, 'w') as file:
                    file.write(note_text)
                print("Note saved successfully")
            except FileNotFoundError:
                print("File save fail")


class Searching:
    def __init__(self, types):
        self.path = os.path.join(os.path.dirname(__file__), '..', 'PIM_dbs')
        self.types = types

    def search_string(self,query):
        match = []
        for filename in os.listdir(self.path):
            if filename.startswith(self.types):
                file_path = os.path.join(self.path, filename)
                with open(file_path, 'r') as file:
                    contents = file.read()
                    if query in contents:
                        match.append(filename)
        return match

    def search_date(self, query):
        print("date use")
        match = []


        operator, time = query.split(' ', maxsplit=1)

        query_time = datetime.strptime(time, '%Y-%m-%d %H:%M')


        for filename in os.listdir(self.path):
            if filename.startswith(self.types):
                file_path = os.path.join(self.path, filename)
                with open(file_path, 'r') as file:
                    contents = file.read()
                    events = contents.split('------------------')
                    for event in events:
                        if 'Start Time:' in event:
                            start_time_str = event.split('Start Time: ')[1].split('\n')[0].strip()

                            start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
                            # Check if the start time matches the query
                            if ((operator == '<' and start_time < query_time) or
                                    (operator == '>' and start_time > query_time) or
                                    (operator == '=' and start_time == query_time)):
                                match.append(filename)
                        elif 'DDL:' in event:
                            start_time_str = event.split('DDL: ')[1].split('\n')[0].strip()
                            start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
                            # Check if the start time matches the query
                            if ((operator == '<' and start_time < query_time) or
                                    (operator == '>' and start_time > query_time) or
                                    (operator == '=' and start_time == query_time)):
                                match.append(filename)
        print(match)
        return match