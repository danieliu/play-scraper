# -*- coding: utf-8 -*-

import unittest

from play_scraper.scraper import PlayScraper
from play_scraper.settings import NUM_RESULTS


BASIC_KEYS = 10
DETAILED_KEYS = 32


class TestScraperMethods(unittest.TestCase):
    def setUp(self):
        self.s = PlayScraper()

    def test_fetching_app_and_details(self):
        app = self.s.details('com.android.chrome')

        self.assertEqual(len(app.keys()), DETAILED_KEYS)
        self.assertEqual(app['app_id'], 'com.android.chrome')

    def test_fetching_collection_non_detailed(self):
        apps = self.s.collection('NEW_FREE', results=2)
        page2 = self.s.collection('NEW_FREE', page=1)

        self.assertEqual(len(apps), 2)
        self.assertEqual(len(apps[0].keys()), BASIC_KEYS)
        self.assertEqual(len(page2), NUM_RESULTS)
        self.assertNotEqual(apps, page2)

    def test_fetching_collection_detailed(self):
        apps = self.s.collection('TOP_FREE', results=1, detailed=True)

        self.assertEqual(len(apps), 1)
        self.assertEqual(len(apps[0].keys()), DETAILED_KEYS)

    def test_fetching_collection_family_category(self):
        apps = self.s.collection('TOP_FREE', results=1, age='SIX_EIGHT')

        self.assertEqual(len(apps), 1)
        self.assertEqual(len(apps[0].keys()), BASIC_KEYS)

    def test_fetching_developer(self):
        apps = self.s.developer('Disney', results=5)

        self.assertEqual(len(apps), 5)
        self.assertEqual(len(apps[0].keys()), BASIC_KEYS)


if __name__ == '__main__':
    unittest.main()
