# -*- coding: utf-8 -*-

import unittest
import logging

from play_scraper.lists import CATEGORIES, COLLECTIONS
from play_scraper.utils import (
    build_url,
    build_collection_url,
    generate_post_data)


logging.disable(logging.CRITICAL)


class BasicSetup(unittest.TestCase):
    def setUp(self):
        self.category = CATEGORIES['GAME_ACTION']
        self.collection = COLLECTIONS['TOP_FREE']


class TestBuildUrl(unittest.TestCase):
    def test_building_app_url(self):
        expected = 'https://play.google.com/store/apps/details?id=com.facebook.orca'
        assert build_url('details', 'com.facebook.orca') == expected

    def test_building_simple_dev_name(self):
        expected = 'https://play.google.com/store/apps/developer?id=Disney'
        assert build_url('developer', 'Disney') == expected

    def test_building_multiple_word_dev_name(self):
        expected = 'https://play.google.com/store/apps/developer?id=SQUARE+ENIX+INC'
        assert build_url('developer', 'SQUARE ENIX INC') == expected


class TestBuildListUrl(BasicSetup):
    def test_list_url_no_args(self):
        expected = 'https://play.google.com/store/apps'
        assert build_collection_url() == expected

    def test_list_url_only_category(self):
        expected = 'https://play.google.com/store/apps/category/GAME_ACTION'
        assert build_collection_url(category=self.category) == expected

    def test_list_url_only_collection(self):
        expected = 'https://play.google.com/store/apps/collection/topselling_free'
        assert build_collection_url(collection=self.collection) == expected

    def test_list_url_both_args(self):
        expected = 'https://play.google.com/store/apps/category/GAME_ACTION/collection/topselling_free'
        assert build_collection_url(
            category=self.category, collection=self.collection) == expected


class TestGeneratePostData(unittest.TestCase):
    def setUp(self):
        self.results = 40
        self.page = 0
        self.pag_tok = 'GAEiAggU:S:ANO1ljLtUJw'

    def test_default_post_data(self):
        expected = {'ipf': 1, 'xhr': 1}
        assert generate_post_data() == expected

    def test_only_num_results(self):
        expected = {'ipf': 1, 'xhr': 1, 'num': self.results}
        assert generate_post_data(self.results) == expected

    def test_first_page_data(self):
        expected = {
            'ipf': 1,
            'xhr': 1,
            'start': self.page * self.results,
            'num': self.results
        }
        assert generate_post_data(self.results, self.page) == expected

    def test_page_token(self):
        expected = {
            'ipf': 1,
            'xhr': 1,
            'start': 0,
            'num': 0,
            'pagTok': self.pag_tok
        }
        assert generate_post_data(0, 0, self.pag_tok) == expected


if __name__ == '__main__':
    unittest.main()
