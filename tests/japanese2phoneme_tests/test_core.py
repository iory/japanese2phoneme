import unittest

from japanese2phoneme import get_chunked_kana


class TestCore(unittest.TestCase):

    def test_get_chunked_kana(self):
        _, _, phoneme = get_chunked_kana('林檎')
        self.assertEqual(phoneme, ['r i ɴ g o'])

        _, _, phoneme = get_chunked_kana('りんご')
        self.assertEqual(phoneme, ['r i ɴ g o'])
