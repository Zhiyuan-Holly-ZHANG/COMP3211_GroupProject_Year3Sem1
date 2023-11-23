import unittest
from model.Alarm import Alarm
from datetime import datetime
from unittest.mock import patch, mock_open, MagicMock


class Test_Alarm(unittest.TestCase):
    
    # Test the 'parse_event' method of the Alarm class
    @patch('os.listdir')
    @patch('model.Alarm.open', new_callable=mock_open,
           read_data="Description: Meeting\nStart Time: 2023-11-20 10:00:00\nAlarm: 1:0:0\n------------------\n")
    def test_parse_event(self, mock_open, mock_listdir):
        alarm = Alarm()
        mock_listdir.return_value = ['Events_2023-11-20.pim']
        events = alarm.parse_event('fake/path/Events_2023-11-20.pim')
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0][0], 'Meeting')

    # Patch the 'model.Alarm.open' method with a mock object, using a fake file content
    # Test the 'mark_event_as_alerted' method of the Alarm class
    @patch('model.Alarm.open', new_callable=mock_open,
           read_data="Description: Meeting\nStart Time: 2023-11-20 10:00:00\nAlarm: 1:0:0\n------------------\n")
    def test_mark_event_as_alerted(self, mock_open):
        alarm = Alarm()
        alarm.mark_event_as_alerted('fake/path/Events_2023-11-20.pim', 'Meeting')
        mock_open().write.assert_called_with(
            "Description: Meeting\nAlerted: True\nStart Time: 2023-11-20 10:00:00\nAlarm: 1:0:0\n------------------\n")

    @patch('model.Alarm.datetime')
    @patch('os.listdir')
    @patch('model.Alarm.open', new_callable=mock_open,
           read_data="Description: Meeting\nStart Time: 2023-11-20 10:00:00\nAlarm: 1:0:0\n------------------\n")
    def test_check_events(self, mock_open, mock_listdir, mock_datetime):
        alarm = Alarm()
        mock_listdir.return_value = ['Events_2023-11-20.pim']
        mock_datetime.now.return_value = datetime(2023, 11, 20, 9, 0)
        mock_datetime.strptime = datetime.strptime
        description = alarm.check_events()
        self.assertEqual(description, 'Meeting')

    @patch('model.Alarm.Mail')
    @patch('model.Alarm.Alarm.check_events')
    def test_alarm(self, mock_check_events, mock_mail_class):
        # Set up the mock to return "Meeting" when check_events is called
        mock_check_events.return_value = "Meeting"

        # Set up the mock for the Mail class
        mock_mail_instance = MagicMock()
        mock_mail_class.return_value = mock_mail_instance

        # Instantiate the Alarm and call the alarm method
        alarm = Alarm()
        alarm.alarm()

        # Assert that the Mail's send method was called with the expected argument
        mock_mail_instance.send.assert_called_with("Events: Meeting will start soon")
