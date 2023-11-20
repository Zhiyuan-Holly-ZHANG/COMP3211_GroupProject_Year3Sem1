from model.Item import Item


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
