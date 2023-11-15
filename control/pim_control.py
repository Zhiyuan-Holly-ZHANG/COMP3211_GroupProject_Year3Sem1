from model.Contacts import Contact
from model.Events import Event
from model.Tasks import Task
from model.Notes import QuickNote
from datetime import datetime, timedelta
from view.pim_view import Printer
from model.Search import Searching
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
        self.search_model = None

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

    def logic_search(self, cmd, types):
        self.search_model = Searching(types)
        # 获取全集
        all_files = set(self.search_model.search_string(''))
        # 初始化操作数和操作符栈
        operands = []
        operators = []
        tokens = cmd.split()
        print("tokens:")
        print(tokens)
        for token in tokens:
            if token == '!':
                operators.append(token)
            elif token == '&&' or token == '||':
                # 当前操作符比栈顶操作符优先级低或相等时，处理栈顶操作符
                while operators and operators[-1] == '&&':
                    self.apply_operator(operands, operators, all_files)
                operators.append(token)
            else:
                # 当前 token 是一个查询字符串
                if operators and operators[-1] == '!':
                    # 如果栈顶是逻辑非，立即处理
                    files = set(self.search_model.search_string(token))
                    operands.append(all_files - files)
                    operators.pop()
                else:
                    files = set(self.search_model.search_string(token))
                    operands.append(files)

        # 应用剩余的操作符
        while operators:
            self.apply_operator(operands, operators, all_files)

        return list(operands[-1])

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
            # 注意: ! 操作符在逻辑搜索中应该是后缀，但这里我们预先处理它
            subset = operands.pop()
            operands.append(all_files - subset)

    def logic_date(self, expression, types):
        self.search_model = Searching(types)
        # 获取全集
        all_files = set(self.search_model.search_string(''))
        # 初始化操作数和操作符栈
        operands = []
        operators = []
        logic_operators = ['&&', '||', '!']
        tokens = []
        buffer = ''
        i = 0

        # 遍历表达式字符
        while i < len(expression):
            # 检测多字符逻辑运算符
            if expression[i:i + 2] in logic_operators:
                if buffer: tokens.append(buffer)
                tokens.append(expression[i:i + 2])
                buffer = ''
                i += 2
            # 检测单字符逻辑运算符
            elif expression[i] in logic_operators:
                if buffer: tokens.append(buffer)
                tokens.append(expression[i])
                buffer = ''
                i += 1
            else:
                buffer += expression[i]
                i += 1

        # 添加最后的缓冲区内容，如果存在
        if buffer:
            tokens.append(buffer)

        # 去除可能的空白符
        tokens = [token.strip() for token in tokens]
        print("tokens:")
        print(tokens)
        for token in tokens:
            if token == '!':
                operators.append(token)
            elif token == '&&' or token == '||':
                # 当前操作符比栈顶操作符优先级低或相等时，处理栈顶操作符
                while operators and operators[-1] == '&&':
                    self.apply_operator(operands, operators, all_files)
                operators.append(token)
            else:
                # 当前 token 是一个查询字符串
                if operators and operators[-1] == '!':
                    # 如果栈顶是逻辑非，立即处理
                    files = set(self.search_model.search_date(token))
                    operands.append(all_files - files)
                    operators.pop()
                else:
                    files = set(self.search_model.search_date(token))
                    operands.append(files)

        # 应用剩余的操作符
        while operators:
            self.apply_operator(operands, operators, all_files)

        return list(operands[-1])

    def select(self, choice):
        cmd = input("input keywords (support !, ||, &&): ")
        find = self.logic_search(cmd, choice)
        if len(find) == 0:
            print("file not found")
        else:
            print("file find as follows: ")
            print(find)

    def select_time(self, choice):
        cmd = input("enter time constraint with <, >, = (YYYY-MM-DD HH:MM)(support || &&): ")
        find = self.logic_date(cmd, choice)
        if len(find) == 0:
            print("file not found")
        else:
            print("file find as follows: ")
            print(find)

    def search_control(self):
        while True:
            choice1 = input("input type of pir you want to search quit(q): ")
            if choice1 == 'Contacts':
                self.select(choice1)


            elif choice1 == 'Events':
                choice2 = input("1)search by keywords 2)search by start time : ")
                if choice2 == '1':
                    self.select(choice1)
                elif choice2 == '2':
                    self.select_time(choice1)


            elif choice1 == 'Tasks':
                choice2 = input("1)search by keywords  2)search by DDL : ")
                if choice2 == '1':
                    self.select(choice1)
                elif choice2 == '2':
                    self.select_time(choice1)

            elif choice1 == 'QuickNotes':
                self.select(choice1)

            elif choice1 == 'q':
                return
