from control.Mail import Mail
import os
from datetime import datetime, timedelta


class Alarm:
    # default path as PIM_dbs
    def __init__(self):
        self.folder_path = os.path.join(os.path.dirname(__file__), '..', 'PIM_dbs')

    # split events with (---------------), get DDL and alarm information of every event
    def parse_event(self, file_path):
        with open(file_path, 'r') as file:
            event_sections = file.read().split('------------------\n')

        events = []
        for section in event_sections:
            lines = section.strip().split('\n')
            if len(lines) < 3 or 'Alerted: True' in section:
                continue

            description = lines[0].split(': ')[1].strip()
            start_time_str = lines[1].split(': ')[1].strip()
            alarm_str = lines[2].split(': ')[1].strip()

            start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
            alarm_duration = timedelta(hours=int(alarm_str.split(':')[0]),
                                       minutes=int(alarm_str.split(':')[1]),
                                       seconds=int(alarm_str.split(':')[2]))
            events.append((description, start_time, alarm_duration))

        return events

    # mark the event already send notification
    def mark_event_as_alerted(self, file_path, event_description):
        with open(file_path, 'r') as file:
            content = file.read()

        updated_content = content.replace(event_description, event_description + '\nAlerted: True')

        with open(file_path, 'w') as file:
            file.write(updated_content)

    # check if the event DDL is close with alarm time
    def check_events(self):
        current_time = datetime.now()
        for file in os.listdir(self.folder_path):
            if file.startswith('Events'):
                file_path = os.path.join(self.folder_path, file)
                events = self.parse_event(file_path)
                for description, start_time, alarm_duration in events:
                    if start_time - alarm_duration <= current_time <= start_time:
                        self.mark_event_as_alerted(file_path, description)
                        return description

    # send Mail to Event need to be notified
    def alarm(self):
        result = self.check_events()
        if result:
            mail = Mail('oliverlorentino@gmail.com', '21099573d@connect.polyu.hk')
            mail.send("Events: " + result + " will start soon")
