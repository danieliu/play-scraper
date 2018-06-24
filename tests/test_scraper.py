# -*- coding: utf-8 -*-

import unittest

from play_scraper import settings
from play_scraper.lists import CATEGORIES
from play_scraper.scraper import PlayScraper


BASIC_KEYS = {
    'app_id',
    'description',
    'developer',
    'developer_id',
    'free',
    'full_price',
    'icon',
    'price',
    'score',
    'title',
    'url',
}
DETAIL_KEYS = {
    'app_id',
    'category',
    'content_rating',
    'current_version',
    'description',
    'description_html',
    'developer',
    'developer_address',
    'developer_email',
    'developer_id',
    'developer_url',
    'editors_choice',
    'free',
    'histogram',
    'iap',
    'iap_range',
    'icon',
    'installs',
    'interactive_elements',
    'price',
    'recent_changes',
    'required_android_version',
    'reviews',
    'score',
    'screenshots',
    'size',
    'title',
    'updated',
    'url',
    'video',
}


class ScraperTestBase(unittest.TestCase):
    def setUp(self):
        self.s = PlayScraper()


class DetailsTest(ScraperTestBase):
    def test_fetching_app_with_all_details(self):
        app_data = self.s.details('com.android.chrome')

        self.assertTrue(all(key in app_data for key in DETAIL_KEYS))
        self.assertEqual(len(DETAIL_KEYS), len(app_data.keys()))
        self.assertEqual('com.android.chrome', app_data['app_id'])
        self.assertEqual(['COMMUNICATION'], app_data['category'])
        self.assertEqual('1,000,000,000+', app_data['installs'])
        self.assertEqual('Google LLC', app_data['developer'])

        # Ensure primitive types, not bs4 NavigableString
        for k, v in app_data.items():
            self.assertTrue(isinstance(
                v,
                (basestring, bool, dict, int, list, type(None))))


class CollectionTest(ScraperTestBase):
    def test_non_detailed_collection(self):
        apps = self.s.collection('NEW_FREE', results=2)

        self.assertEqual(2, len(apps))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))

        for app in apps:
            # Ensure primitive types, not bs4 NavigableString
            for k, v in app.items():
                self.assertTrue(isinstance(
                    v,
                    (basestring, bool, dict, int, list, type(None))))

    def test_default_num_results(self):
        apps = self.s.collection('NEW_FREE', page=1)

        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))
        self.assertEqual(settings.NUM_RESULTS, len(apps))

    def test_detailed_collection(self):
        apps = self.s.collection('TOP_FREE', results=1, detailed=True)

        self.assertEqual(len(apps), 1)
        self.assertTrue(all(key in apps[0] for key in DETAIL_KEYS))
        self.assertEqual(len(DETAIL_KEYS), len(apps[0].keys()))

    def test_family_with_age_collection(self):
        apps = self.s.collection('TOP_FREE', 'FAMILY', results=1, age='SIX_EIGHT')

        self.assertEqual(len(apps), 1)
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))

    def test_promotion_collection_id(self):
        apps = self.s.collection('promotion_3000000d51_pre_registration_games',
                                 results=2)

        self.assertEqual(2, len(apps))
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))

    def test_invalid_collection_id(self):
        with self.assertRaises(ValueError):
            self.s.collection('invalid_collection_id')


class DeveloperTest(ScraperTestBase):
    def test_fetching_developer_default_results(self):
        apps = self.s.developer('Disney')

        self.assertEqual(settings.DEV_RESULTS, len(apps))
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))

    def test_maximum_results(self):
        # 'CrowdCompass by Cvent' has ~273 apps
        apps = self.s.developer('CrowdCompass by Cvent', results=120)

        self.assertEqual(120, len(apps))
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))

    def test_over_max_results_fetches_five(self):
        apps = self.s.developer('CrowdCompass by Cvent', results=121)

        self.assertEqual(5, len(apps))
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))

    def test_page_out_of_range(self):
        with self.assertRaises(ValueError):
            self.s.developer('CrowdCompass by Cvent',
                             results=20,
                             page=13)


class SuggestionTest(ScraperTestBase):
    def test_empty_query(self):
        with self.assertRaises(ValueError):
            self.s.suggestions('')

    def test_query_suggestions(self):
        suggestions = self.s.suggestions('cat')

        self.assertGreater(len(suggestions), 0)


class SearchTest(ScraperTestBase):
    def test_basic_search(self):
        apps = self.s.search('cats')

        self.assertEqual(20, len(apps))
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))


class SimilarTest(ScraperTestBase):
    def test_similar_ok(self):
        apps = self.s.similar('com.android.chrome')

        self.assertGreater(len(apps), 0)
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))


class CategoryTest(ScraperTestBase):
    def test_categories_ok(self):
        categories = self.s.categories()

        # This will fail when categories are removed over time, but not if
        # new categories are added.
        self.assertTrue(all(key in categories for key in CATEGORIES))


if __name__ == '__main__':
    unittest.main()
