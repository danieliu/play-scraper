# -*- coding: utf-8 -*-

import json
import logging
import re
try:
    from urllib import quote_plus
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin, quote_plus

import requests
from bs4 import BeautifulSoup, SoupStrainer

from play_scraper import settings as s
from play_scraper.lists import AGE_RANGE, CATEGORIES, COLLECTIONS
from play_scraper.utils import (
    build_collection_url,
    build_url,
    generate_post_data,
    multi_app_request,
    send_request,
)


class PlayScraper(object):
    def __init__(self):
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

        dev_soup = soup.select_one('a.subtitle')
        developer = dev_soup.attrs['title']
        developer_id = dev_soup.attrs['href'].split('=')[1]

        description = soup.select_one('div.description').text.strip()
        score = soup.select_one('div.tiny-star')
        if score is not None:
            score = score.attrs['aria-label'].strip().split(' ')[1]

        try:
            price = soup.select_one('span.display-price').string
        except AttributeError:
            try:
                # Pre-register apps are 'Coming Soon'
                price = soup.select_one('a.price').string
            except AttributeError:
                # Country restricted, no price or buttons shown
                price = None

        full_price = None
        if price is not None:
            try:
                full_price = soup.select_one('span.full-price').string
            except AttributeError:
                full_price = None

        free = (price is None)
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
            'full_price': full_price,
            'price': price,
            'free': free
        }

    def _parse_additional_info(self, soup):
        """Parses an app's additional information section on its detail page.

        :param soup: the additional_info section BeautifulSoup object
        :return: a dictionary of the app's parsed additional info
        """
        # This is super ugly because the CSS is obfuscated and doesn't have good
        # distinguishing selectors available; each section's markup is nearly
        # identical, so we get the values with a similar function.
        section_titles_divs = [x for x in soup.select('div.hAyfc div.BgcNfc')]
        get_value_span = lambda x: x.next_sibling.select_one('span.htlgb')

        title_normalization = {
            'Updated': 'updated',
            'Size': 'size',
            'Installs': 'installs',
            'Current Version': 'current_version',
            'Requires Android': 'required_android_version',
            'Content Rating': 'content_rating',
            'In-app Products': 'iap_range',
            'Interactive Elements': 'interactive_elements',
            'Offered By': 'developer',
            'Developer': 'developer_info',
        }

        data = {
            'updated': None,
            'size': None,
            'installs': None,
            'current_version': None,
            'required_android_version': None,
            'content_rating': None,
            'iap_range': None,
            'interactive_elements': None,
            'developer': None,
            'developer_email': None,
            'developer_url': None,
            'developer_address': None,
        }

        for title_div in section_titles_divs:
            section_title = title_div.string
            if section_title in title_normalization:
                title_key = title_normalization[section_title]
                value_div = get_value_span(title_div)

                if title_key == 'content_rating':
                    # last string in list is 'Learn more' link
                    value = [rating.strip()
                             for rating in value_div.strings][:-1]
                elif title_key == 'interactive_elements':
                    value = [ielement.strip()
                             for ielement in value_div.strings]
                elif title_key == 'iap_range':
                    iaps = re.search(r'(\$\d+\.\d{2}) - (\$\d+\.\d{2})',
                                     value_div.string)
                    if iaps:
                        value = iaps.groups()
                elif title_key == 'developer_info':
                    developer_email = value_div.select_one('a[href^="mailto:"]')
                    if developer_email:
                        developer_email = (developer_email.attrs['href']
                                                          .split(':')[1])
                    developer_url = value_div.select_one('a[href^="http"]')
                    if developer_url:
                        developer_url = developer_url.attrs['href']

                    developer_address = value_div.select('div')[-1].contents[0]
                    if developer_address.name is not None:
                        # If a bs4 Tag, it will have name attribute, e.g. 'a'
                        # Set the address to None for 'not found'
                        # The address div should just be a string, no name attr
                        developer_address = None
                    dev_data = {'developer_email': developer_email,
                                'developer_url': developer_url,
                                'developer_address': developer_address}
                    data.update(dev_data)
                    continue
                else:
                    value = value_div.string

                data[title_key] = value
        return data

    def _parse_app_details(self, soup):
        """Extracts an app's details from its info page.

        :param soup: a strained BeautifulSoup object of an app
        :return: a dictionary of app details
        """
        title = soup.select_one('h1[itemprop="name"] span').string
        icon = (soup.select_one('img[alt="Cover art"]')
                    .attrs['src']
                    .split('=')[0])
        editors_choice = bool(soup.select_one('meta[itemprop="editorsChoiceBadgeUrl"]'))

        # Main category will be first
        category = [c.attrs['href'].split('/')[-1]
                    for c in soup.select('a[itemprop="genre"]')]

        # Let the user handle modifying the URL to fetch different resolutions
        # Removing the end `=w720-h310-rw` doesn't seem to give original res?
        screenshots = [img.attrs['src']
                       for img in soup.select('img[alt="Screenshot Image"]')]

        try:
            video = (soup.select_one('button[data-trailer-url^="https"]')
                         .attrs.get('data-trailer-url'))
            if video is not None:
                video = video.split('?')[0]
        except AttributeError:
            video = None

        description_soup = soup.select_one(
            'div[itemprop="description"] content div')
        if description_soup:
            description = '\n'.join(description_soup.stripped_strings)
            description_html = description_soup.encode_contents()
        else:
            description = description_html = None

       # Reviews & Ratings
        try:
            score = soup.select_one('div.BHMmbe').text
        except AttributeError:
            score = None

        histogram = {}
        try:
            reviews = int(soup.select_one('span[aria-label$="ratings"]')
                              .text
                              .replace(',', ''))
            ratings_section = soup.select_one('div.VEF2C')
            num_ratings = [int(rating.attrs['title'].replace(',', ''))
                           for rating in ratings_section.select(
                               'div span[style^="width:"]')]
            for i in range(5):
                histogram[5 - i] = num_ratings[i]
        except AttributeError:
            reviews = 0


        try:
            changes_soup = soup.select('div[itemprop="description"] content')[1]
            recent_changes = '\n'.join([x.string.strip() for x in changes_soup])
        except (IndexError, AttributeError):
            recent_changes = None

        try:
            price = soup.select_one('meta[itemprop="price"]').attrs['content']
        except AttributeError:
            # App is probably pre-register, requires logged in to see
            try:
                price = soup.select_one('not-preregistered').string.strip()
            except AttributeError:
                price = None

        free = (price == '0')

        additional_info_data = self._parse_additional_info(
            soup.select_one('.xyOfqd'))

        offers_iap = bool(additional_info_data.get('iap_range'))

        dev_id = soup.select_one('a.hrTbp.R8zArc').attrs['href'].split('=')[1]
        developer_id = dev_id if dev_id else None

        data = {
            'title': title,
            'icon': icon,
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
            'iap': offers_iap,
            'developer_id': developer_id,
        }

        data.update(additional_info_data)

        return data

    def _parse_multiple_apps(self, list_response):
        """Extracts app ids from a list's Response object, sends GET requests to
        each app, parses detailed info and returns all apps in a list.

        :param list_response: the Response object from a list request
        :return: a list of app dictionaries
        """
        list_strainer = SoupStrainer('span',
                                     {'class': 'preview-overlay-container'})
        soup = BeautifulSoup(list_response.content,
                             'lxml',
                             from_encoding='utf8',
                             parse_only=list_strainer)

        app_ids = [x.attrs['data-docid']
                   for x in soup.select('span.preview-overlay-container')]
        responses = multi_app_request(app_ids)

        app_strainer = SoupStrainer('div', {'class': 'LXrl4c'})
        apps = []
        errors = []
        for i, r in enumerate(responses):
            if r is not None and r.status_code == requests.codes.ok:
                soup = BeautifulSoup(r.content,
                                     'lxml',
                                     from_encoding='utf8',
                                     parse_only=app_strainer)
                app_json = self._parse_app_details(soup)
                app_json.update({
                    'app_id': app_ids[i],
                    'url': r.url,
                })
                apps.append(app_json)
            else:
                errors.append(app_ids[i])

        if errors:
            self._log.error('There was an error parsing the following apps: {errors}.'.format(
                errors=', '.join(errors)))

        return apps

    def details(self, app_id):
        """Sends a GET request and parses an application's details.

        :param app_id: the app to retrieve details, e.g. 'com.nintendo.zaaa'
        :return: a dictionary of app details
        """
        url = build_url('details', app_id)

        try:
            response = send_request('GET', url)
            soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf8')
        except requests.exceptions.HTTPError as e:
            raise ValueError('Invalid application ID: {app}. {error}'.format(
                app=app_id, error=e))

        app_json = self._parse_app_details(soup)
        app_json.update({
            'app_id': app_id,
            'url': url,
        })
        return app_json

    def collection(self, collection_id, category_id=None, results=None,
                   page=None, age=None, detailed=False):
        """Sends a POST request and fetches a list of applications belonging to
        the collection and an optional category.

        :param collection_id: the collection id, e.g. 'NEW_FREE'.
        :param category_id: (optional) the category id, e.g. 'GAME_ACTION'.
        :param results: the number of apps to retrieve at a time.
        :param page: page number to retrieve; limitation: page * results <= 500.
        :param age: an age range to filter by (only for FAMILY categories)
        :param detailed: if True, sends request per app for its full detail
        :return: a list of app dictionaries
        """
        if (collection_id not in COLLECTIONS and
                not collection_id.startswith('promotion')):
            raise ValueError('Invalid collection_id.')
        if collection_id in COLLECTIONS:
            collection_name = COLLECTIONS[collection_id]
        else:
            collection_name = collection_id

        category = '' if category_id is None else CATEGORIES.get(category_id)
        if category is None:
            raise ValueError('Invalid category_id.')

        results = s.NUM_RESULTS if results is None else results
        if results > 120:
            raise ValueError('Number of results cannot be more than 120.')

        page = 0 if page is None else page
        if page * results > 500:
            raise ValueError('Start (page * results) cannot be greater than 500.')

        params = {}
        if category.startswith('FAMILY') and age is not None:
            params['age'] = AGE_RANGE[age]

        url = build_collection_url(category, collection_name)
        data = generate_post_data(results, page)
        response = send_request('POST', url, data, params)

        if detailed:
            apps = self._parse_multiple_apps(response)
        else:
            soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf8')
            apps = [self._parse_card_info(app_card)
                    for app_card in soup.select('div[data-uitype=500]')]

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

        if detailed:
            apps = self._parse_multiple_apps(response)
        else:
            soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf8')
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
        soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf8')

        if detailed:
            apps = self._parse_multiple_apps(response)
        else:
            apps = [self._parse_card_info(app) for app in soup.select('div[data-uitype=500]')]

        return apps

    def similar(self, app_id, detailed=False):
        """Sends a GET request, follows the redirect, and retrieves a list of
        applications similar to the specified app.

        :param app_id: the app to retrieve details from, e.g. 'com.nintendo.zaaa'
        :param detailed: if True, sends request per app for its full detail
        :return: a list of similar apps
        """
        url = build_url('similar', app_id)
        response = send_request('GET', url, allow_redirects=True)
        soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf8')

        if detailed:
            apps = self._parse_multiple_apps(response)
        else:
            apps = [self._parse_card_info(app) for app in soup.select('div[data-uitype=500]')]

        return apps

    def categories(self):
        """Sends a GET request to the front page (app store base url), parses
        and returns a list of all available categories.

        Note: May contain some promotions, e.g. "Popular Characters"
        """
        categories = {}
        strainer = SoupStrainer('a', {'class': 'child-submenu-link'})

        response = send_request('GET', s.BASE_URL)
        soup = BeautifulSoup(response.content,
                             'lxml',
                             from_encoding='utf8',
                             parse_only=strainer)
        category_links = soup.select('a.child-submenu-link')
        age = '?age='

        for cat in category_links:
            url = urljoin(s.BASE_URL, cat.attrs['href'])
            category_id = url.split('/')[-1]
            name = cat.string

            if age in category_id:
                category_id = 'FAMILY'
                url = url.split('?')[0]
                name = 'Family'

            if category_id not in categories:
                categories[category_id] = {
                    'name': name,
                    'url': url,
                    'category_id': category_id}

        return categories

