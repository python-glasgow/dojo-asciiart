import unittest
from team3 import ascii_art_generator


class TestAscii(unittest.TestCase):
    def test_image(self):
        # self.maxDiff = 100000
        actual = ascii_art_generator.generate_art('python-logo.png')
        with open('python-logo-ascii.txt', 'r') as file:
            expected = "".join(row for row in file)
        self.assertEqual(actual, expected)

    def test_writing(self):
        ascii_art_generator.write_art('python-logo.png', 'python-logo-ascii.txt')