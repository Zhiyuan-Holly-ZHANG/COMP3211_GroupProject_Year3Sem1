import unittest
from unittest.mock import patch, mock_open
from model.Notes import QuickNote


class Test_Notes(unittest.TestCase):
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['First line', 'Second line', 'END', 'w'])
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

