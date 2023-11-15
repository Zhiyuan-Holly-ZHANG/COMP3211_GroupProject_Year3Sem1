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











