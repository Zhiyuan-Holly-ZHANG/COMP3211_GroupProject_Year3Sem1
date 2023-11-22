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

    # Test the __init__.class of the created file
    @patch('os.path.dirname')
    @patch("builtins.open", mock_open())
    def test_init(self, mock_dirname):
        # Mock os.path.dirname to return a specific path
        mock_dirname.return_value = 'fake'

        # The file does not have a branch
        item = Item('Contacts', 0)
        current_date = datetime.now().strftime('%Y-%m-%d')
        expected_filename = os.path.join('fake', '..', 'PIM_dbs', 'Contacts_' + current_date + '.pim')

        self.assertEqual(item.filename, expected_filename)
        self.assertEqual(item.list, [])

        # File exists in a branch
        item = Item('test_pir', 'Contacts_test.pim')
        expected_filename = os.path.join('fake', '..', 'PIM_dbs', 'Contacts_test.pim')

        self.assertEqual(item.filename, expected_filename)
        self.assertEqual(item.list, [])

    # save test
    @patch('os.path.dirname')
    @patch('os.path.join')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_to_file(self, mock_file_open, mock_path_join, mock_dirname):
        # set up file creation
        mock_dirname.return_value = 'fake'
        mock_path_join.return_value = 'fake/PIM_dbs/fake.pim'
        item = Item('Contacts', 0)

        # store data
        item_data = {'Name': 'test_case', 'Phone': '110'}

        # call save function 
        item.save_to_file(item_data)

        mock_file_open.assert_called_with('fake/PIM_dbs/fake.pim', 'a')

        # test file write operation
        expected_calls = [
            unittest.mock.call.write('Name: test_case\n'),
            unittest.mock.call.write('Phone: 110\n'),
            unittest.mock.call.write('------------------\n')
        ]

        mock_file_open().write.assert_has_calls(expected_calls, any_order=False)

    # View test

    @patch('os.path.dirname')
    @patch('os.path.join')
    @patch('builtins.open', new_callable=mock_open, read_data="Name: test_case\nPhone: 110\n------------------\n")
    def test_view(self, mock_file_open, mock_path_join, mock_dirname):
        # set up
        mock_dirname.return_value = 'fake'
        mock_path_join.return_value = 'fake/PIM_dbs/fake.pim'
        item = Item('Contacts', 0)

        with patch('builtins.print') as mock_print:
            item.view()

            # test print function
            expected_print = [
                unittest.mock.call('Name: test_case\n'),
                unittest.mock.call('Phone: 110\n'),
                unittest.mock.call('------------------\n')
            ]

            mock_print.assert_has_calls(expected_print, any_order=False)

        # test open function
        mock_file_open.assert_called_with('fake/PIM_dbs/fake.pim', 'r')

    # delete test
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

            # test open function 2 call(for reading and writing)
            #  Why are there three file reading operations here?
            self.assertEqual(mock_file_open.call_count, 3)
            mock_file_open.assert_any_call('fake_dir/PIM_dbs/fake_file.pim', 'r')
            mock_file_open.assert_any_call('fake_dir/PIM_dbs/fake_file.pim', 'w')

            # test write function
            expected_write_calls = [
                unittest.mock.call("Name: John Doe\nPhone: 1234567890\n"),
                unittest.mock.call("------------------\n")
            ]
            mock_file().write.assert_has_calls(expected_write_calls, any_order=False)

    # update test
    @patch('os.path.dirname')
    @patch('os.path.join')
    @patch.object(Item, 'create_item', side_effect=lambda item_data: item_data)
    def test_update(self, mock_create_item, mock_path_join, mock_dirname):
        # set up
        mock_dirname.return_value = 'fake_dir'
        mock_path_join.return_value = 'fake_dir/PIM_dbs/fake_file.pim'

        # read file mock
        mock_file_data = "Name: John Doe\nPhone: 1234567890\n------------------\n" + \
                         "Title: Mr\nIdentifier: 123\n------------------\n"

        with patch('builtins.open', new_callable=mock_open, read_data=mock_file_data):
            item = Item('Contacts', 0)

            # update function
            item.update()
            expected_items = [
                {'Name': 'John Doe', 'Phone': '1234567890'},
                {'Title': 'Mr', 'Identifier': '123'}
            ]
            self.assertEqual(item.list, expected_items)

    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_view_file_not_found(self, mock_print, mock_open):
        item = Item("TestItem", 0)
        mock_open.side_effect = FileNotFoundError

        item.view()
        mock_print.assert_called_with(FileNotFoundError)

    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_delete_item_file_not_found(self, mock_print, mock_open):
        item = Item("TestItem", "nonexistentfile.pim")
        # Execute
        item.delete_item("Title", "Identifier")
        mock_open.side_effect = FileNotFoundError
        mock_print.assert_called_with("Item not found.")
