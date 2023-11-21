import unittest
from unittest.mock import patch, mock_open
from model.Contacts import Contact

class Test_Contacts(unittest.TestCase):
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


