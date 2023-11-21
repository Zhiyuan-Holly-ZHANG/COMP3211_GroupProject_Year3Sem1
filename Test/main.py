from Test_Contacts import Test_Contacts
from Test_Search import Test_Search
from Test_Notes import Test_Notes
from Test_Events import Test_Events
from Test_Item import TestItem
from Test_Tasks import Test_Tasks
from Test_Alarm import Test_Alarm
import unittest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_Tasks))
    suite.addTest(unittest.makeSuite(Test_Contacts))
    suite.addTest(unittest.makeSuite(TestItem))
    suite.addTest(unittest.makeSuite(Test_Notes))
    suite.addTest(unittest.makeSuite(Test_Events))
    suite.addTest(unittest.makeSuite(Test_Search))
    suite.addTest(unittest.makeSuite(Test_Alarm))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
