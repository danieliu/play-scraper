# -*- coding: utf-8 -*-

import unittest

try:
    basestring
except NameError:
    basestring = (str, bytes)

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

ADDITIONAL_INFO_KEYS = {
    'content_rating',
    'current_version',
    'developer',
    'developer_address',
    'developer_email',
    'developer_url',
    'iap_range',
    'installs',
    'interactive_elements',
    'required_android_version',
    'size',
    'updated',
}


class ScraperTestBase(unittest.TestCase):
    def setUp(self):
        self.s = PlayScraper()


class PlayScraperTest(unittest.TestCase):
    def test_init_with_defaults(self):
        s = PlayScraper()
        self.assertEqual(settings.BASE_URL, s._base_url)
        self.assertEqual(settings.SUGGESTION_URL, s._suggestion_url)
        self.assertEqual(settings.SEARCH_URL, s._search_url)
        self.assertEqual(settings.PAGE_TOKENS, s._pagtok)
        self.assertEqual('en', s.language)
        self.assertEqual('us', s.geolocation)
        self.assertDictEqual({'hl': 'en',
                              'gl': 'us'},
                             s.params)

    def test_init_with_language_and_geolocation(self):
        s = PlayScraper(hl='ko', gl='kr')
        self.assertEqual('ko', s.language)
        self.assertEqual('kr', s.geolocation)
        self.assertDictEqual({'hl': 'ko',
                              'gl': 'kr'},
                             s.params)

    def test_invalid_language_code_raises(self):
        with self.assertRaises(ValueError) as e:
            PlayScraper(hl='invalid')
        self.assertEqual('invalid is not a valid language interface code.',
                         str(e.exception))

    def test_invalid_geolocation_code_raises(self):
        with self.assertRaises(ValueError) as e:
            PlayScraper(gl='invalid')
        self.assertEqual('invalid is not a valid geolocation country code.',
                         str(e.exception))


class DetailsTest(ScraperTestBase):
    def test_fetching_app_with_all_details(self):
        app_data = self.s.details('com.android.chrome')

        self.assertTrue(all(key in app_data for key in DETAIL_KEYS))
        self.assertEqual(len(DETAIL_KEYS), len(app_data.keys()))
        self.assertEqual('com.android.chrome', app_data['app_id'])
        self.assertEqual(['COMMUNICATION'], app_data['category'])
        self.assertEqual('1,000,000,000+', app_data['installs'])
        self.assertEqual('Google LLC', app_data['developer'])
        self.assertTrue(all(x is not None for x in app_data['screenshots']))

        # Ensure primitive types, not bs4 NavigableString
        for k, v in app_data.items():
            self.assertTrue(isinstance(
                v,
                (basestring, bool, dict, int, list, type(None))))

    def test_fetching_app_in_spanish(self):
        s = PlayScraper(hl='es', gl='es')
        app_data = s.details('com.android.chrome')
        self.assertTrue(all(key in app_data for key in DETAIL_KEYS))
        self.assertEqual(len(DETAIL_KEYS), len(app_data.keys()))
        self.assertEqual('com.android.chrome', app_data['app_id'])
        self.assertEqual(['COMMUNICATION'], app_data['category'])
        self.assertTrue(all(x is not None for x in app_data['screenshots']))

        # additional details, like installs, are all None because we currently
        # hardcode an English mapping for the various additional info section
        # titles.
        self.assertTrue(all([app_data[x] is None
                            for x in ADDITIONAL_INFO_KEYS]))


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

        self.assertEqual(1, len(apps))
        self.assertTrue(all(key in apps[0] for key in DETAIL_KEYS))
        self.assertEqual(len(DETAIL_KEYS), len(apps[0].keys()))

    def test_family_with_age_collection(self):
        apps = self.s.collection('TOP_FREE',
                                 'FAMILY',
                                 results=1,
                                 age='SIX_EIGHT')

        self.assertEqual(1, len(apps))
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))

    def test_promotion_collection_id(self):
        apps = self.s.collection('promotion_3000000d51_pre_registration_games',
                                 results=2)

        self.assertEqual(2, len(apps))
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))

    def test_different_language_and_country(self):
        s = PlayScraper(hl='da', gl='dk')
        apps = s.collection('TOP_PAID', 'LIFESTYLE', results=5)

        self.assertEqual(5, len(apps))
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))

    def test_invalid_collection_id(self):
        with self.assertRaises(ValueError) as e:
            self.s.collection('invalid_collection_id')
        self.assertEqual('Invalid collection_id \'invalid_collection_id\'.',
                         str(e.exception))

    def test_invalid_category_id(self):
        with self.assertRaises(ValueError) as e:
            self.s.collection('TOP_PAID', 'invalid_category_id')
        self.assertEqual('Invalid category_id \'invalid_category_id\'.',
                         str(e.exception))

    def test_invalid_num_results_over_120(self):
        with self.assertRaises(ValueError) as e:
            self.s.collection('TOP_PAID', 'LIFESTYLE', results=121)
        self.assertEqual('Number of results cannot be more than 120.',
                         str(e.exception))

    def test_invalid_page_x_results_over_500(self):
        with self.assertRaises(ValueError) as e:
            self.s.collection('TOP_PAID', 'LIFESTYLE', results=120, page=5)
        self.assertEqual('Start (page * results) cannot be greater than 500.',
                         str(e.exception))


class DeveloperTest(ScraperTestBase):
    def test_fetching_developer_default_results(self):
        apps = self.s.developer('Disney')

        self.assertEqual(settings.DEV_RESULTS, len(apps))
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))

    def test_maximum_results(self):
        # 'CrowdCompass by Cvent' has ~273 apps
        apps = self.s.developer('CrowdCompass by Cvent', results=120)

        self.assertGreaterEqual(len(apps), 100)
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))

    def test_over_max_results_fetches_five(self):
        apps = self.s.developer('CrowdCompass by Cvent', results=121)

        self.assertEqual(5, len(apps))
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))

    def test_fetch_developer_apps_detailed(self):
        apps = self.s.developer('Disney', results=3, detailed=True)

        self.assertEqual(3, len(apps))
        self.assertTrue(all(key in apps[0] for key in DETAIL_KEYS))
        self.assertEqual(len(DETAIL_KEYS), len(apps[0].keys()))

    def test_different_language_and_country(self):
        s = PlayScraper(hl='da', gl='dk')
        apps = s.developer('Google LLC', results=5)

        self.assertEqual(5, len(apps))
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))

    def test_developer_parameter_string_digits_invalid(self):
        with self.assertRaises(ValueError) as e:
            self.s.developer('5700313618786177705')
        self.assertEqual('Parameter \'developer\' must be the developer name, not the developer id.',
                         str(e.exception))

    def test_developer_parameter_int_invalid(self):
        with self.assertRaises(ValueError) as e:
            self.s.developer(1234)
        self.assertEqual('Parameter \'developer\' must be the developer name, not the developer id.',
                         str(e.exception))

    def test_developer_parameter_long_invalid(self):
        with self.assertRaises(ValueError) as e:
            self.s.developer(5700313618786177705)
        self.assertEqual('Parameter \'developer\' must be the developer name, not the developer id.',
                         str(e.exception))

    def test_developer_parameter_float_invalid(self):
        with self.assertRaises(ValueError) as e:
            self.s.developer(57003136187.86177705)
        self.assertEqual('Parameter \'developer\' must be the developer name, not the developer id.',
                         str(e.exception))

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

    def test_different_language_and_country(self):
        s = PlayScraper(hl='da', gl='dk')
        suggestions = s.suggestions('dog')

        self.assertGreater(len(suggestions), 0)


class SearchTest(ScraperTestBase):
    def test_basic_search(self):
        apps = self.s.search('cats')

        self.assertEqual(20, len(apps))
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))

    def test_search_with_app_detailed(self):
        apps = self.s.search('cats', detailed=True)

        self.assertEqual(20, len(apps))
        self.assertTrue(all(key in apps[0] for key in DETAIL_KEYS))
        self.assertEqual(len(DETAIL_KEYS), len(apps[0].keys()))

    def test_different_language_and_country(self):
        s = PlayScraper(hl='da', gl='dk')
        apps = s.search('dog')

        self.assertEqual(20, len(apps))
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))

    def test_page_out_of_range_not_between_0_and_12(self):
        with self.assertRaises(ValueError) as e:
            self.s.search('dog', page=13)
        self.assertEqual('Parameter \'page\' (13) must be between 0 and 12.',
                         str(e.exception))


class SimilarTest(ScraperTestBase):
    def test_similar_ok(self):
        apps = self.s.similar('com.android.chrome')

        self.assertGreater(len(apps), 0)
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))

    def test_similar_with_app_detailed(self):
        apps = self.s.similar('com.android.chrome', detailed=True)

        self.assertGreater(len(apps), 0)
        self.assertTrue(all(key in apps[0] for key in DETAIL_KEYS))
        self.assertEqual(len(DETAIL_KEYS), len(apps[0].keys()))

    def test_different_language_and_country(self):
        s = PlayScraper(hl='da', gl='dk')
        apps = s.similar('com.android.chrome')

        self.assertGreater(len(apps), 0)
        self.assertTrue(all(key in apps[0] for key in BASIC_KEYS))
        self.assertEqual(len(BASIC_KEYS), len(apps[0].keys()))


class CategoryTest(ScraperTestBase):
    def test_categories_ok(self):
        categories = self.s.categories()

        # This will fail when categories are removed over time, but not if
        # new categories are added.
        self.assertTrue(all(key in categories for key in CATEGORIES))

    def test_different_language_and_country(self):
        s = PlayScraper(hl='da', gl='dk')
        categories = s.categories()

        self.assertTrue(all(key in categories for key in CATEGORIES))
