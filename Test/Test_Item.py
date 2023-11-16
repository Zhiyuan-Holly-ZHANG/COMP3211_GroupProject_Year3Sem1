import unittest
from datetime import datetime
from unittest.mock import patch, mock_open
from model.pim_model import Item
from datetime import datetime
import os


class TestItem(unittest.TestCase):
    @patch('os.path.dirname')
    @patch("builtins.open", mock_open())

    #只写了一个，后面靠你了，郑桑
    def test_init(self, mock_dirname):
        # 模拟 os.path.dirname 返回特定路径
        mock_dirname.return_value = 'fake'

        item = Item('Contacts', 0)
        current_date = datetime.now().strftime('%Y-%m-%d')
        expected_filename = os.path.join('fake', '..', 'PIM_dbs','Contacts_'+current_date+'.pim')
        self.assertEqual(item.filename, expected_filename)
        self.assertEqual(item.list, [])

        item = Item('test_pir', 'Contacts_test.pim')
        expected_filename = os.path.join('fake', '..', 'PIM_dbs', 'Contacts_test.pim')
        self.assertEqual(item.filename, expected_filename)
        self.assertEqual(item.list, [])


