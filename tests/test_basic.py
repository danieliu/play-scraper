import unittest

from scraper.scraper import PlayScraper


class TestBasicFunction(unittest.TestCase):
    def test_assert(self):
        self.assertTrue(True)

    def test_play_scraper(self):
        s = PlayScraper()
        self.assertTrue(isinstance(s, PlayScraper))


if __name__ == '__main__':
    unittest.main()
