import unittest
import os
from unittest.mock import patch, mock_open
from model.Search import Searching

class Test_Search(unittest.TestCase):
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
    def test_search_date_event(self, mock_file, mock_listdir):
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

    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    def test_search_date(self, mock_file, mock_listdir):
        # Setup
        mock_listdir.return_value = ['tasks_file1.pim', 'tasks_file2.pim']

        file_data = {
            'tasks_file1.pim': "DDL: 2021-01-01 10:00\n------------------\n",
            'tasks_file2.pim': "DDL: 2020-12-30 10:00\n------------------\n"
        }

        # Define side effect for mock_open
        def mock_file_read(file_name, mode):
            return mock_open(read_data=file_data[os.path.basename(file_name)])()

        mock_file.side_effect = mock_file_read

        searcher = Searching('tasks_file')

        # Execute
        results = searcher.search_date('> 2020-12-31 23:59')

        # Verify
        mock_listdir.assert_called_once()
        self.assertIn('tasks_file1.pim', results)
        self.assertNotIn('tasks_file2.pim', results)

