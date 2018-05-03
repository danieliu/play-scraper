# -*- coding: utf-8 -*-

import json
import logging
try:
    from urllib import quote_plus
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin, quote_plus

import requests
from bs4 import BeautifulSoup, SoupStrainer

from . import settings as s
from .lists import CATEGORIES, COLLECTIONS, AGE_RANGE
from .utils import (build_url, build_collection_url, send_request,
    generate_post_data, multi_app_request)


class PlayScraper(object):
    def __init__(self):
        self.categories = CATEGORIES
        self.collections = COLLECTIONS
        self.age = AGE_RANGE
        self._base_url = s.BASE_URL
        self._suggestion_url = s.SUGGESTION_URL
        self._search_url = s.SEARCH_URL
        self._pagtok = s.PAGE_TOKENS
        self._log = logging.getLogger(__name__)

    def _parse_card_info(self, soup):
        """Extracts basic app info from the app's card. Used when parsing pages
        with lists of apps.

        :param soup: a BeautifulSoup object of an app's card
        :return: a dictionary of available basic app info
        """
        app_id = soup.attrs['data-docid']
        url = urljoin(
            self._base_url, soup.select_one('a.card-click-target').attrs['href'])
        icon = urljoin(
            self._base_url,
            soup.select_one('img.cover-image').attrs['src'].split('=')[0])
        title = soup.select_one('a.title').attrs['title']

        dev = soup.select_one('a.subtitle')
        developer = dev.attrs['title']
        dev_id = dev.attrs['href'].split('=')[1]
        developer_id = dev_id if dev_id.isdigit() else None

        description = soup.select_one('div.description').text.strip()
        score = soup.select_one('div.tiny-star')
        if score is not None:
            score = score.attrs['aria-label'].strip().split(' ')[1]

        # Most apps will have 'Free' or their price
        try:
            price = soup.select_one('span.display-price').string
        except AttributeError:
            try:
                # Pre-register apps 'Coming Soon'
                price = soup.select_one('.price').string
            except AttributeError:
                # Country restricted, no price or buttons shown
                price = 'Not Available'

        free = (price == 'Free')
        if free is True:
            price = '0'

        return {
            'app_id': app_id,
            'url': url,
            'icon': icon,
            'title': title,
            'developer': developer,
            'developer_id': developer_id,
            'description': description,
            'score': score,
            'price': price,
            'free': free
        }

    def _parse_app_details(self, soup, app_id, url):
        """Extracts an app's details from its info page.

        :param soup: a strained BeautifulSoup object of an app
        :param app_id:
        :return: a dictionary of app details
        """
        title = soup.select_one('h1[itemprop=name]').string
        icon = urljoin(
            self._base_url,
            soup.select_one('img[itemprop=image]').attrs['src'].split('=')[0])
        screenshots = [urljoin(
            self._base_url,
            img.attrs['src']) for img in soup.select('img[itemprop=image]')[1:]]

        try:
            video = soup.find_all(
                lambda tag: tag.name == 'button' and tag.get('data-trailer-url') is not None
            )[0].attrs.get('data-trailer-url', None)

            if video is not None:
                video = video.split('?')[0]
        except (AttributeError, IndexError):
            video = None

        # Main category will be first
        category = [c.attrs['href'].split('/')[-1] for c in soup.select('a[itemprop=genre]')]

        description_soup = soup.select_one('div[itemprop=description]')
        if description_soup:
            description = "\n".join(description_soup.stripped_strings)
            description_html = description_soup.encode_contents().decode('utf-8')
        else:
            description = ''
            description_html = ''

        # Reviews & Ratings
        try:
            score = float(soup.select_one('div.BHMmbe').string)
        except AttributeError:
            score = None
            pass

        histogram = {}
        try:
            # convert string in the form of '6,652,775' to int
            reviews = int(list(soup.select_one('span.EymY4b').children)[1].string.replace(',', ''))
            ratings = [int(r['title'].replace(',', '')) for r in soup.select('span.L2o20d')]
            for i in range(5):
                histogram[5 - i] = ratings[i]
        except AttributeError:
            reviews = 0
            pass

        recent_changes = "\n".join([x.text.strip() for x in soup.select('div.DWPxHb')[1:]])
        editors_choice = bool(soup.select_one('span.giozf'))
        try:
            price = soup.select_one('meta[itemprop="price"]').attrs['content']
        except AttributeError:
            try:
                price = soup.select_one('div.preregistration-text-add').string.strip()
            except AttributeError:
                price = 'Not Available'

        free = (price == '0')

        # Additional information section
        additional_info = soup.select_one('div.xyOfqd')
        items = additional_info.select('span.htlgb')

        updated = items[1].string.strip() if len(items) > 1 else None
        size = items[3].string.strip() if len(items) > 3 else None
        installs = int(items[5].string.replace('+', '').replace(',', '')) if len(items) > 5 else None
        current_version = items[7].string.strip() if len(items) > 7 else None
        required_android_version = items[9].string.strip() if len(items) > 9 else None
        content_rating = items[11].text.strip() if len(items) > 11 else None
        interactive_elements = [it.strip() for it in items[13].string.split(',')] if len(items) > 13 else []
        developer = items[19].text.strip() if len(items) > 19 else None
        developer_info = list(items[21].children) if len(items) > 21 else None

        try:
            developer_email = developer_info[1].string
        except (AttributeError, IndexError):
            developer_email = None

        try:
            web_site = developer_info[0].select_one('a').attrs['href']
        except (AttributeError, IndexError):
            web_site = None

        try:
            developer_address = developer_info[3].string
        except IndexError:
            developer_address = None

        return {
            'app_id': app_id,
            'title': title,
            'icon': icon,
            'url': url,
            'screenshots': screenshots,
            'video': video,
            'category': category,
            'score': score,
            'histogram': histogram,
            'reviews': reviews,
            'description': description,
            'description_html': description_html,
            'recent_changes': recent_changes,
            'editors_choice': editors_choice,
            'price': price,
            'free': free,
            'updated': updated,
            'size': size,
            'installs': installs,
            'current_version': current_version,
            'required_android_version': required_android_version,
            'content_rating': content_rating,
            'interactive_elements': interactive_elements,
            'developer': developer,
            'developer_email': developer_email,
            'developer_address': developer_address,
            'web_site': web_site
        }

    def _parse_multiple_apps(self, list_response):
        """Extracts app ids from a list's Response object, sends GET requests to
        each app, parses detailed info and returns all apps in a list.

        :param list_response: the Response object from a list request
        :return: a list of app dictionaries
        """
        list_strainer = SoupStrainer('span', {'class': 'preview-overlay-container'})
        soup = BeautifulSoup(list_response.content, 'lxml', parse_only=list_strainer)

        app_ids = [x.attrs['data-docid'] for x in soup.select('span.preview-overlay-container')]
        responses = multi_app_request(app_ids)

        apps = []
        errors = []
        for i, p in enumerate(zip(responses, app_ids)):
            r, app_id = p
            if r is not None and r.status_code == requests.codes.ok:
                soup = BeautifulSoup(r.content, 'lxml')
                apps.append(self._parse_app_details(soup, app_id, r.url))
            else:
                errors.append(app_ids[i])

        if errors:
            self._log.error("There was an error parsing the following apps: {errors}.".format(
                errors=", ".join(errors)))

        return apps

    def details(self, app_id):
        """Sends a GET request and parses an application's details.

        :param app_id: the app to retrieve details from, e.g. 'com.nintendo.zaaa'
        :return: a dictionary of app details
        """
        url = build_url('details', app_id)

        try:
            response = send_request('GET', url)
            soup = BeautifulSoup(response.content, 'lxml')
        except requests.exceptions.HTTPError as e:
            raise ValueError('Invalid application ID: {app}. {error}'.format(
                app=app_id, error=e))

        return self._parse_app_details(soup, app_id, url)

    def collection(self, collection, category=None, results=None, page=None, age=None, detailed=False):
        """Sends a POST request and fetches a list of applications belonging to
        the collection and an optional category.

        :param collection: the collection id, e.g. 'NEW_FREE'.
        :param category: (optional) the category name, e.g. 'GAME_ACTION'.
        :param results: the number of apps to retrieve at a time.
        :param page: page number to retrieve; limitation: page * results <= 500.
        :param age: an age range to filter by (only for FAMILY categories)
        :param detailed: if True, sends request per app for its full detail
        :return: a list of app dictionaries
        """
        collection = self.collections[collection]
        category = '' if category is None else self.categories[category]

        results = s.NUM_RESULTS if results is None else results
        if results > 120:
            raise ValueError('Number of results cannot be more than 120.')

        page = 0 if page is None else page
        if page * results > 500:
            raise ValueError('Start (page * results) cannot be greater than 500.')

        params = {}
        if category.startswith('FAMILY') and age is not None:
            params['age'] = self.age[age]

        url = build_collection_url(category, collection)
        data = generate_post_data(results, page)
        response = send_request('POST', url, data, params)

        if detailed:
            apps = self._parse_multiple_apps(response)
        else:
            soup = BeautifulSoup(response.content, 'lxml')
            apps = [self._parse_card_info(app) for app in soup.select('div[data-uitype=500]')]

        return apps

    def developer(self, developer, results=None, page=None, detailed=False):
        """Sends a POST request and retrieves a list of the developer's published
        applications on the Play Store.

        :param developer: developer name to retrieve apps from, e.g. 'Disney'
        :param results: the number of app results to retrieve
        :param page: the page number to retrieve
        :param detailed: if True, sends request per app for its full detail
        :return: a list of app dictionaries
        """
        results = s.DEV_RESULTS if results is None else results
        page = 0 if page is None else page
        page_num = (results // 20) * page
        if not 0 <= page_num <= 12:
            raise ValueError('Page out of range. (results // 20) * page must be between 0 - 12')
        pagtok = self._pagtok[page_num]

        url = build_url('developer', developer)
        data = generate_post_data(results, 0, pagtok)
        response = send_request('POST', url, data)
        soup = BeautifulSoup(response.content, 'lxml')

        if detailed:
            apps = self._parse_multiple_apps(response)
        else:
            apps = [self._parse_card_info(app) for app in soup.select('div[data-uitype=500]')]

        return apps

    def suggestions(self, query):
        """Sends a GET request and retrieves a list of autocomplete suggestions
        matching the query term(s).

        :param query: search query term(s) to retrieve autocomplete suggestions
        :return: a list of suggested search queries, up to 5
        """
        if not query:
            raise ValueError("Cannot get suggestions for an empty query.")

        params = {
            'json': 1,
            'c': 0,
            'hl': 'en',
            'gl': 'us',
            'query': query
        }

        response = send_request('GET', self._suggestion_url, params=params)
        suggestions = [q['s'] for q in json.loads(response.content)]
        return suggestions

    def search(self, query, page=None, detailed=False):
        """Sends a POST request and retrieves a list of applications matching
        the query term(s).

        :param query: search query term(s) to retrieve matching apps
        :param page: the page number to retrieve. Max is 12.
        :param detailed: if True, sends request per app for its full detail
        :return: a list of apps matching search terms
        """
        page = 0 if page is None else page
        if page > len(self._pagtok) - 1:
            raise ValueError('Page out of range. Please choose a number between 0 - 12')

        pagtok = self._pagtok[page]
        data = generate_post_data(0, 0, pagtok)

        params = {
            'q': quote_plus(query),
            'c': 'apps'
        }

        response = send_request('POST', self._search_url, data, params)
        soup = BeautifulSoup(response.content, 'lxml')

        if detailed:
            apps = self._parse_multiple_apps(response)
        else:
            apps = [self._parse_card_info(app) for app in soup.select('div[data-uitype=500]')]

        return apps

    def similar(self, app_id, results=None, detailed=False):
        """Sends a POST request and retrieves a list of applications similar to
        the specified app.

        :param app_id: the app to retrieve details from, e.g. 'com.nintendo.zaaa'
        :param results: the number of apps to retrieve at a time.
        :param detailed: if True, sends request per app for its full detail
        :return: a list of similar apps
        """
        results = s.SIMILAR_RESULTS if results is None else results

        url = build_url('similar', app_id)
        data = generate_post_data(results)
        response = send_request('POST', url, data)
        soup = BeautifulSoup(response.content, 'lxml')

        if detailed:
            apps = self._parse_multiple_apps(response)
        else:
            apps = [self._parse_card_info(app) for app in soup.select('div[data-uitype=500]')]

        return apps
