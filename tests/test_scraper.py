# -*- coding: utf-8 -*-

import unittest

from play_scraper.scraper import PlayScraper
from play_scraper import settings


BASIC_KEYS = 10
DETAILED_KEYS = 27


class ScraperTestBase(unittest.TestCase):
    def setUp(self):
        self.s = PlayScraper()


class TestScrapingDetails(ScraperTestBase):
    def test_fetching_app_with_all_details(self):
        app = self.s.details('com.android.chrome')

        self.assertEqual(len(app.keys()), DETAILED_KEYS)
        self.assertEqual(app['app_id'], 'com.android.chrome')
        self.assertEqual(app['category'], ['COMMUNICATION'])
        self.assertEqual(app['installs'], 1000000000)
        self.assertFalse(app['editors_choice'])


class TestScrapingCollections(ScraperTestBase):
    def test_fetching_collection_non_detailed(self):
        apps = self.s.collection('NEW_FREE', results=2)
        apps_p2 = self.s.collection('NEW_FREE', page=1)

        self.assertEqual(len(apps), 2)
        self.assertEqual(len(apps[0].keys()), BASIC_KEYS)
        self.assertEqual(len(apps_p2), settings.NUM_RESULTS)
        self.assertNotEqual(apps, apps_p2)

    def test_fetching_collection_detailed(self):
        apps = self.s.collection('TOP_FREE', results=1, detailed=True)

        self.assertEqual(len(apps), 1)
        self.assertEqual(len(apps[0].keys()), DETAILED_KEYS)

    def test_fetching_collection_family_category(self):
        apps = self.s.collection('TOP_FREE', results=1, age='SIX_EIGHT')

        self.assertEqual(len(apps), 1)
        self.assertEqual(len(apps[0].keys()), BASIC_KEYS)


class TestScrapingDeveloperApps(ScraperTestBase):
    def test_fetching_developer_default_results(self):
        apps = self.s.developer('Disney')

        self.assertEqual(len(apps), settings.DEV_RESULTS)
        self.assertEqual(len(apps[0].keys()), BASIC_KEYS)

    def test_maximum_results(self):
        # 'CrowdCompass by Cvent' has ~273 apps
        apps = self.s.developer('CrowdCompass by Cvent', results=120)
        self.assertEqual(len(apps), 120)

    def test_over_max_results_fetches_five(self):
        maximum = self.s.developer('CrowdCompass by Cvent', results=121)
        num_apps = len(maximum)

        self.assertEqual(num_apps, 5)

    def test_page_out_of_range(self):
        with self.assertRaises(ValueError):
            self.s.developer(
                'CrowdCompass by Cvent',
                results=20,
                page=13)


class TestSuggestionQueries(ScraperTestBase):
    def test_empty_query(self):
        with self.assertRaises(ValueError):
            self.s.suggestions('')

    def test_query_suggestions(self):
        suggestions = self.s.suggestions('cat')

        self.assertGreater(len(suggestions), 0)


class TestSearchQuery(ScraperTestBase):
    def test_basic_search(self):
        apps = self.s.search('cats')

        self.assertEqual(len(apps), 20)


if __name__ == '__main__':
    unittest.main()
