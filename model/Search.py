import os
from datetime import datetime


class Searching:
    # init function set up the path and the types of the query (such as Events, Contacts, Tasks and QuickNotes)
    def __init__(self, types):
        self.path = os.path.join(os.path.dirname(__file__), '..', 'PIM_dbs')
        self.types = types

    # search by keywords
    def search_string(self, query):
        match = []
        for filename in os.listdir(self.path):
            if filename.startswith(self.types):
                file_path = os.path.join(self.path, filename)
                with open(file_path, 'r') as file:
                    contents = file.read()
                    if query in contents:
                        match.append(filename)
        return match

    # search with date and operation such as > 2023-11-11 11:11
    def search_date(self, query):
        match = []

        operator, time = query.split(' ', maxsplit=1)

        query_time = datetime.strptime(time, '%Y-%m-%d %H:%M')

        for filename in os.listdir(self.path):
            if filename.startswith(self.types):
                file_path = os.path.join(self.path, filename)
                with open(file_path, 'r') as file:
                    contents = file.read()
                    events = contents.split('------------------')
                    # check by matching with Start time or DDL
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

        return match
