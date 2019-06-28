import unittest

from src.features.printout import print_image
from src.features.printout import add


class TestPrintout(unittest.TestCase):

    def setUp(self):
        self.return_message = "successful print"
        self.inn_a = 2
        self.inn_b = 3

    def test_print_images(self):
        test_return_message = print_image()
        self.assertEqual(self.return_message, test_return_message)

    def test_add(self):
        add_return_value = add(self.inn_a, self.inn_b)
        self.assertEqual(add_return_value, 5)

if __name__ == '__main__':
    unittest.main()
