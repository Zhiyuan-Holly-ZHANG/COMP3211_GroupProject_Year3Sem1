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

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['First line', 'END', 'c', 'Second line', 'END', 'w'])
    @patch('builtins.open', new_callable=mock_open)
    def test_note_continue(self, mock_file, mock_input, mock_print):
        quick_note = QuickNote('testfile.pim')
        quick_note.makeNote()
        mock_print.assert_any_call("=====continue=======")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['First line', 'END', 'x', 'END', 'w'])
    @patch('builtins.open', new_callable=mock_open)
    def test_note_wrong_choice(self, mock_file, mock_input, mock_print):
        quick_note = QuickNote('testfile.pim')
        quick_note.makeNote()
        mock_print.assert_any_call("Wrong choice,try to enter 'END' again")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['First line', 'END', 'q'])
    @patch('builtins.open', new_callable=mock_open)
    def test_note_quit_choice(self, mock_file, mock_input, mock_print):
        quick_note = QuickNote('testfile.pim')
        quick_note.makeNote()
        mock_print.assert_any_call("Quit successfully")





