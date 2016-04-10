import unittest
import logging

from bs4 import BeautifulSoup

from play_scraper.scraper import PlayScraper


logging.disable(logging.CRITICAL)


class ScraperTests(unittest.TestCase):
    def setUp(self):
        self.scraper = PlayScraper()
        self.category = self.scraper.categories['GAME_ACTION']
        self.collection = self.scraper.collections['TOP_FREE']

    def test_building_app_url(self):
        app_id = 'com.facebook.orca'
        generated_url = self.scraper._app_url(app_id)
        self.assertEqual(
            generated_url, 'https://play.google.com/store/apps/details?id=com.facebook.orca')

    def test_list_url_no_args(self):
        url = self.scraper._list_url()
        self.assertEqual(
            url, 'https://play.google.com/store/apps')

    def test_list_url_only_category(self):
        url = self.scraper._list_url(category=self.category)
        self.assertEqual(
            url, 'https://play.google.com/store/apps/category/GAME_ACTION')

    def test_list_url_only_collection(self):
        url = self.scraper._list_url(collection=self.collection)
        self.assertEqual(
            url, 'https://play.google.com/store/apps/collection/topselling_free')

    def test_list_url_both_args(self):
        url = self.scraper._list_url(category=self.category, collection=self.collection)
        self.assertEqual(
            url, 'https://play.google.com/store/apps/category/GAME_ACTION/collection/topselling_free')

    def test_normal_post_data(self):
        data = self.scraper._generate_post_data()
        self.assertEqual(data, {'ipf': 1, 'xhr': 1})

    def test_getting_soup_and_(self):
        soup = self.scraper._get_soup(
            url=self.scraper._base_url,
            method='GET')
        self.assertIsInstance(soup, BeautifulSoup)

if __name__ == '__main__':
    unittest.main()
