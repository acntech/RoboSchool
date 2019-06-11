import unittest
from src.visualization.printout import print_image


class TestPrintout(unittest.TestCase):

    def setUp(self):
        self.return_message = "successful print"

    def test_print_images(self):
        test_return_message = print_image()
        self.assertEqual(self.return_message, test_return_message)


if __name__ == '__main__':
    unittest.main()
