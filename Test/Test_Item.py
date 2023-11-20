import unittest
from datetime import datetime
from unittest.mock import patch, mock_open

from model.Item import Item
from model.Search import Searching
from model.Notes import QuickNote
from model.Contacts import Contact
from model.Events import Event
from model.Tasks import Task
from datetime import datetime

import os


class TestItem(unittest.TestCase):

    # 测试创建文件的__init__.class
    @patch('os.path.dirname')
    @patch("builtins.open", mock_open())
    def test_init(self, mock_dirname):
        # 模拟 os.path.dirname 返回特定路径
        mock_dirname.return_value = 'fake'

        # 文件不存在分支
        item = Item('Contacts', 0)
        current_date = datetime.now().strftime('%Y-%m-%d')
        expected_filename = os.path.join('fake', '..', 'PIM_dbs', 'Contacts_' + current_date + '.pim')

        self.assertEqual(item.filename, expected_filename)
        self.assertEqual(item.list, [])

        # 文件存在分支
        item = Item('test_pir', 'Contacts_test.pim')
        expected_filename = os.path.join('fake', '..', 'PIM_dbs', 'Contacts_test.pim')

        self.assertEqual(item.filename, expected_filename)
        self.assertEqual(item.list, [])

    # save测试
    @patch('os.path.dirname')
    @patch('os.path.join')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_to_file(self, mock_file_open, mock_path_join, mock_dirname):
        # 前置操作文件创建
        mock_dirname.return_value = 'fake'
        mock_path_join.return_value = 'fake/PIM_dbs/fake.pim'
        item = Item('Contacts', 0)

        # 储存数据
        item_data = {'Name': 'test_case', 'Phone': '110'}

        # 调用save函数
        item.save_to_file(item_data)

        mock_file_open.assert_called_with('fake/PIM_dbs/fake.pim', 'a')

        # 检查文件写入操作
        expected_calls = [
            unittest.mock.call.write('Name: test_case\n'),
            unittest.mock.call.write('Phone: 110\n'),
            unittest.mock.call.write('------------------\n')
        ]

        mock_file_open().write.assert_has_calls(expected_calls, any_order=False)

    # View 测试

    @patch('os.path.dirname')
    @patch('os.path.join')
    @patch('builtins.open', new_callable=mock_open, read_data="Name: test_case\nPhone: 110\n------------------\n")
    def test_view(self, mock_file_open, mock_path_join, mock_dirname):
        # 前置操作文件创建
        mock_dirname.return_value = 'fake'
        mock_path_join.return_value = 'fake/PIM_dbs/fake.pim'
        item = Item('Contacts', 0)

        with patch('builtins.print') as mock_print:
            item.view()

            # 检查 print 功能
            expected_print = [
                unittest.mock.call('Name: test_case\n'),
                unittest.mock.call('Phone: 110\n'),
                unittest.mock.call('------------------\n')
            ]

            mock_print.assert_has_calls(expected_print, any_order=False)

        # 检查文件open功能
        mock_file_open.assert_called_with('fake/PIM_dbs/fake.pim', 'r')

    # delete 测试
    @patch('os.path.dirname')
    @patch('os.path.join')
    def test_delete_item(self, mock_path_join, mock_dirname):
        mock_dirname.return_value = 'fake_dir'
        mock_path_join.return_value = 'fake_dir/PIM_dbs/fake_file.pim'

        mock_file_data = "Name: John Doe\nPhone: 1234567890\n------------------\n" + \
                         "Title: Mr\nIdentifier: 123\n------------------\n"

        mock_file = mock_open(read_data=mock_file_data)
        with patch('builtins.open', mock_file) as mock_file_open:
            item = Item('Contacts', 0)
            item.delete_item('Title', 'Mr')

            # 检查 open function 2次call(for reading and writing)
            #  这边为什么会出现三次文件读取操作？
            self.assertEqual(mock_file_open.call_count, 3)
            mock_file_open.assert_any_call('fake_dir/PIM_dbs/fake_file.pim', 'r')
            mock_file_open.assert_any_call('fake_dir/PIM_dbs/fake_file.pim', 'w')

            # 检擦写入功能
            expected_write_calls = [
                unittest.mock.call("Name: John Doe\nPhone: 1234567890\n"),
                unittest.mock.call("------------------\n")
            ]
            mock_file().write.assert_has_calls(expected_write_calls, any_order=False)

    # update 测试
    @patch('os.path.dirname')
    @patch('os.path.join')
    @patch.object(Item, 'create_item', side_effect=lambda item_data: item_data)
    def test_update(self, mock_create_item, mock_path_join, mock_dirname):
        # 前置操作
        mock_dirname.return_value = 'fake_dir'
        mock_path_join.return_value = 'fake_dir/PIM_dbs/fake_file.pim'

        # 文件读取操作的mock
        mock_file_data = "Name: John Doe\nPhone: 1234567890\n------------------\n" + \
                         "Title: Mr\nIdentifier: 123\n------------------\n"

        with patch('builtins.open', new_callable=mock_open, read_data=mock_file_data):
            item = Item('Contacts', 0)

            # update 功能
            item.update()
            expected_items = [
                {'Name': 'John Doe', 'Phone': '1234567890'},
                {'Title': 'Mr', 'Identifier': '123'}
            ]
            self.assertEqual(item.list, expected_items)








 # Tests for Searching
    @patch('os.path.join')
    @patch('os.listdir')
    def test_search_string(self, mock_listdir, mock_path_join):
        # Set up mock data
        mock_file_data = "This is a test file containing the word test."
        mock_listdir.return_value = ['test_file_1.txt', 'test_file_2.txt']
        mock_path_join.side_effect = lambda *args: '/'.join(args)

        # Create a mock open function
        with patch('builtins.open', new_callable=mock_open, read_data=mock_file_data) as mock_file:
            # Create an instance of the Searching class
            searching = Searching('test_file')

            # Execute the search method
            result = searching.search_string("test")

            # Verify the search result
            self.assertIn('test_file_1.txt', result)
            self.assertIn('test_file_2.txt', result)

    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    def test_search_date(self, mock_file, mock_listdir):
        # Setup
        mock_listdir.return_value = ['eventfile1.pim', 'eventfile2.pim']

        file_data = {
            'eventfile1.pim': "Start Time: 2021-01-01 10:00:00\n------------------\n",
            'eventfile2.pim': "Start Time: 2020-12-30 10:00:00\n------------------\n"
        }

        # Define side effect for mock_open
        def mock_file_read(file_name, mode):
            return mock_open(read_data=file_data[os.path.basename(file_name)])()

        mock_file.side_effect = mock_file_read

        searcher = Searching('eventfile')

        # Execute
        results = searcher.search_date('> 2020-12-31 23:59')

        # Verify
        mock_listdir.assert_called_once()
        self.assertIn('eventfile1.pim', results)
        self.assertNotIn('eventfile2.pim', results)

    #Note_test

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['First line', 'Second line', 'END', 's'])
    @patch('builtins.open', new_callable=mock_open)
    def test_note(self, mock_file, mock_input, mock_print):
        # Setup
        quick_note = QuickNote('testfile.pim')

        # Execute
        quick_note.makeNote()

        # Verify file operations
        # mock_file.assert_called_once_with(quick_note.filename, 'w')
        mock_file.assert_any_call(quick_note.filename, 'w')
        handle = mock_file()
        expected_write_calls = [
            unittest.mock.call('First line\nSecond line'),
            # unittest.mock.call('Second line\n'),
        ]
        handle.write.assert_has_calls(expected_write_calls, any_order=False)


        # Verify print output
        expected_print_calls = [unittest.mock.call("Note saved successfully")]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)





    # Contact_test
    def test_create_item(self):
        # Setup
        item_data = {
            "Name": "John Doe",
            "Phone": "1234567890",
            "Email": "john@example.com",
            "Address": "123 Main St"
        }
        contact = Contact("John", "1234567890", "john@example.com", "123 Main St", 0)

        # Execute
        created_contact = contact.create_item(item_data)

        # Verify
        self.assertEqual(created_contact.name, "John Doe")
        self.assertEqual(created_contact.phone, "1234567890")
        self.assertEqual(created_contact.email, "john@example.com")
        self.assertEqual(created_contact.address, "123 Main St")

    @patch('builtins.open', new_callable=mock_open)
    def test_add_contact(self, mock_file):
        # Setup
        contact = Contact("John", "1234567890", "john@example.com", "123 Main St", 0)
        name = "Jane Doe"
        phone = "0987654321"
        email = "jane@example.com"
        address = "321 Other St"

        # Execute
        contact.add_contact(name, phone, email, address)

        # Verify that the open function was called for append and read
        expected_calls = [
            unittest.mock.call(contact.filename, 'a'),
            unittest.mock.call(contact.filename, 'r')
        ]
        mock_file.assert_has_calls(expected_calls, any_order=True)

        # Verify file write operations
        handle = mock_file()

        expected_write_calls = [
            unittest.mock.call.write("Name: Jane Doe\n"),
            unittest.mock.call.write("Phone: 0987654321\n"),
            unittest.mock.call.write("Email: jane@example.com\n"),
            unittest.mock.call.write("Address: 321 Other St\n"),
            unittest.mock.call.write("------------------\n")
        ]
        handle.write.assert_has_calls(expected_write_calls, any_order=False)




    #Event_test
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







    #tast_test

    def test_create_item(self):
        # Setup
        item_data = {
            "Description": "Finish report",
            "DDL": "2021-02-20"
        }
        task = Task("Finish report", "2021-02-20", 0)

        # Execute
        created_task = task.create_item(item_data)

        # Verify
        self.assertEqual(created_task.description, "Finish report")
        self.assertEqual(created_task.ddl, "2021-02-20")

    @patch('builtins.open', new_callable=mock_open)
    def test_add_task(self, mock_file):
        # Setup
        task = Task("Finish report", "2021-02-20", 0)
        description = "Prepare presentation"
        ddl = "2021-03-15"

        # Execute
        task.add_task(description, ddl)

        # Verify file write operations
        handle = mock_file()
        expected_calls = [
            unittest.mock.call.write("Description: Prepare presentation\n"),
            unittest.mock.call.write("DDL: 2021-03-15\n"),
            unittest.mock.call.write("------------------\n")
        ]
        handle.write.assert_has_calls(expected_calls, any_order=False)


if __name__ == '__main__':
    unittest.main()
