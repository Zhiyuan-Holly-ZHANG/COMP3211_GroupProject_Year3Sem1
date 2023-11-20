import unittest
from unittest.mock import patch, mock_open
from model.Tasks import Task


class Test_Tasks(unittest.TestCase):
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
