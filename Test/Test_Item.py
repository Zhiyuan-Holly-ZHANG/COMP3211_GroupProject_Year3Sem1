import unittest
from datetime import datetime
from unittest.mock import patch, mock_open
from model.pim_model import Item
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


if __name__ == '__main__':
    unittest.main()
