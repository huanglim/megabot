import unittest
import sys, os, time
sys.path.append(os.path.dirname(__file__))
#sys.path.append(os.path.dirname(os.getcwd()))

from requestsloader import RequestsLoader

class TestRquestsLoader(unittest.TestCase):
    """docstring for TestRquestsLoader"""

    def setUp(self):
        self.loader = RequestsLoader()

    def test_not_exist_file(self):
        with self.assertRaises(FileNotFoundError):
            self.loader.load_workbook('not_exist_file')

    def tearDown(self):
        pass

if __name__ == '__main__':
    print(sys.path)
    unittest.main()