import unittest

from gencontent import *

class TestContentGen(unittest.TestCase):
    def test_extract_title(self):
        markdown = '# mama aqui dodge ram         '
        self.assertEqual('mama aqui dodge ram', extract_title(markdown))

    def test_extract_title_error(self):
        markdown = 'eu juro por mim mesmo por deus por meus pais'
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()