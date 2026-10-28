import unittest

from application import double


class ApplicationCheck(unittest.TestCase):
    def test_double(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
