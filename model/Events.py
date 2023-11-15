from model.pim_model import Item


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
