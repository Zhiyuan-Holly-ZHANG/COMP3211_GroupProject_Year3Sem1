import unittest
from unittest.mock import patch, mock_open
from model.Events import Event

class Test_Events(unittest.TestCase):
    def test_create_item(self):
        # Setup
        item_data = {
            "Description": "Meeting with team",
            "Start Time": "2021-01-01 10:00",
            "Alarm": "2020-12-31 09:00"
        }
        event = Event("Meeting", "2021-01-01 10:00", "2020-12-31 09:00", 0)

        # Execute
        created_event = event.create_item(item_data)

        # Verify
        self.assertEqual(created_event.description, "Meeting with team")
        self.assertEqual(created_event.start_time, "2021-01-01 10:00")
        self.assertEqual(created_event.alarm, "2020-12-31 09:00")

    @patch('builtins.open', new_callable=mock_open)
    def test_add_event(self, mock_file):
        # Setup
        event = Event("Meeting", "2021-01-01 10:00", "2020-12-31 09:00", 0)
        description = "Project Review"
        start_time = "2021-02-01 14:00"
        alarm = "2021-02-01 13:00"

        # Execute
        event.add_event(description, start_time, alarm)

        # Verify file write operations

        handle = mock_file()
        expected_calls = [
            unittest.mock.call.write("Description: Project Review\n"),
            unittest.mock.call.write("Start Time: 2021-02-01 14:00\n"),
            unittest.mock.call.write("Alarm: 2021-02-01 13:00\n"),
            unittest.mock.call.write("------------------\n")
        ]
        handle.write.assert_has_calls(expected_calls, any_order=False)
