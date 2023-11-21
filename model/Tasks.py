from model.Item import Item


class Task(Item):
    #  Override init function by specifying more information
    def __init__(self, description, ddl, load):
        super().__init__("Tasks", load)
        self.description = description
        self.ddl = ddl

    # override creat_item function by specifying more information
    def add_task(self, description, ddl):
        event_data = {
            "Description": description,
            "DDL": ddl
        }
        self.save_to_file(event_data)
        self.update()

    # add new task pir to the task file
    def create_item(self, item_data):
        return Task(item_data['Description'], item_data['DDL'], self.load)
