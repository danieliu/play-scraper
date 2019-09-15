# -*- coding: utf-8 -*-

import unittest
import logging

import play_scraper.settings as s
from play_scraper.lists import CATEGORIES, COLLECTIONS, AGE_RANGE
from play_scraper.utils import (
    build_url,
    build_collection_url,
    generate_post_data,
    send_request,
)


logging.disable(logging.CRITICAL)


class BasicSetup(unittest.TestCase):
    def setUp(self):
        self.category = CATEGORIES["GAME_ACTION"]
        self.collection = COLLECTIONS["TOP_FREE"]


class TestBuildUrl(unittest.TestCase):
    def test_building_app_url(self):
        expected = "https://play.google.com/store/apps/details?id=com.facebook.orca"
        self.assertEqual(expected, build_url("details", "com.facebook.orca"))

    def test_building_simple_dev_name(self):
        expected = "https://play.google.com/store/apps/developer?id=Disney"
        self.assertEqual(expected, build_url("developer", "Disney"))

    def test_building_multiple_word_dev_name(self):
        expected = "https://play.google.com/store/apps/developer?id=SQUARE+ENIX+INC"
        self.assertEqual(expected, build_url("developer", "SQUARE ENIX INC"))


class TestBuildListUrl(BasicSetup):
    def test_list_url_no_args(self):
        expected = "https://play.google.com/store/apps"
        self.assertEqual(build_collection_url(), expected)

    def test_list_url_only_category(self):
        expected = "https://play.google.com/store/apps/category/GAME_ACTION"
        self.assertEqual(build_collection_url(category=self.category), expected)

    def test_list_url_only_collection(self):
        expected = "https://play.google.com/store/apps/collection/topselling_free"
        self.assertEqual(expected, build_collection_url(collection=self.collection))

    def test_list_url_both_args(self):
        expected = "https://play.google.com/store/apps/category/GAME_ACTION/collection/topselling_free"
        self.assertEqual(
            expected,
            build_collection_url(category=self.category, collection=self.collection),
        )


class TestGeneratePostData(unittest.TestCase):
    def setUp(self):
        self.results = 40
        self.page = 0
        self.pag_tok = s.PAGE_TOKENS[2]

    def test_default_post_data(self):
        expected = {"ipf": 1, "xhr": 1}
        self.assertEqual(generate_post_data(), expected)

    def test_only_num_results(self):
        expected = {"ipf": 1, "xhr": 1, "num": self.results}
        self.assertEqual(generate_post_data(self.results), expected)

    def test_first_page_data(self):
        expected = {
            "ipf": 1,
            "xhr": 1,
            "start": self.page * self.results,
            "num": self.results,
        }
        self.assertEqual(generate_post_data(self.results, self.page), expected)

    def test_page_token(self):
        expected = {"ipf": 1, "xhr": 1, "start": 0, "num": 0, "pagTok": self.pag_tok}
        self.assertEqual(generate_post_data(0, 0, self.pag_tok), expected)


class TestSendRequest(unittest.TestCase):
    def setUp(self):
        self.url = "https://www.google.com/"
        self.age = AGE_RANGE["FIVE_UNDER"]

    def test_send_normal_request(self):
        method = "GET"
        response = send_request(method, self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.url, self.url)

    def test_request_with_params(self):
        method = "GET"
        params = {"q": "google play store"}
        response = send_request(method, self.url, params=params)
        expected_url = "{base}{params}".format(
            base=self.url, params="?q=google+play+store"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.url, expected_url)
