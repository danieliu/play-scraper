# -*- coding: utf-8 -*-

import json
import urlparse
import urllib

import requests
from bs4 import BeautifulSoup, SoupStrainer

import settings as s
from .lists import CATEGORIES, COLLECTIONS
from .utils import (build_url, build_collection_url, send_request,
    generate_post_data, multi_app_request)


class PlayScraper(object):
    def __init__(self):
        self.categories = CATEGORIES
        self.collections = COLLECTIONS
        self._base_url = s.BASE_URL
        self._suggestion_url = s.SUGGESTION_URL
        self._search_url = s.SEARCH_URL
        self._pagtok = s.PAGE_TOKENS

    def _parse_card_info(self, soup):
        """Extracts basic app info from the app's card. Used when parsing pages
        with lists of apps.

        :param soup: a BeautifulSoup object of an app's card
        :return: a dictionary of available basic app info
        """
        app_id = soup.attrs['data-docid']
        url = urlparse.urljoin(
            self._base_url, soup.select_one('a.card-click-target').attrs['href'])
        icon = urlparse.urljoin(
            self._base_url,
            soup.select_one('img.cover-image').attrs['src'].split('=')[0])
        title = soup.select_one('a.title').attrs['title']
        developer = soup.select_one('a.subtitle').attrs['title']
        description = soup.select_one('div.description').text.strip()
        score = soup.select_one('div.tiny-star')
        if score is not None:
            score = score.attrs['aria-label'].strip().split(' ')[1]
        price = soup.select_one('span.display-price').string
        free = (price == 'Free')
        if free is True:
            price = '0'

        return {
            'app_id': app_id,
            'url': url,
            'icon': icon,
            'title': title,
            'developer': developer,
            'description': description,
            'score': score,
            'price': price,
            'free': free
        }

    def _parse_app_details(self, soup):
        """Extracts an app's details from its info page.

        :param soup: a strained BeautifulSoup object of an app
        :return: a dictionary of app details
        """
        app_id = soup.select_one('span.play-button').attrs['data-docid']
        url = soup.select_one('meta[itemprop="url"]').attrs['content']
        title = soup.select_one('div.id-app-title').string
        icon = urlparse.urljoin(
            self._base_url,
            soup.select_one('img.cover-image').attrs['src'].split('=')[0])
        screenshots = [urlparse.urljoin(
            self._base_url,
            img.attrs['src']) for img in soup.select('img.full-screenshot')]
        thumbnails = [urlparse.urljoin(
            self._base_url,
            img.attrs['src']) for img in soup.select('img.screenshot')]

        try:
            video = soup.select_one('span.preview-overlay-container').attrs.get('data-video-url', None)
            if video is not None:
                video = video.split('?')[0]
        except AttributeError:
            video = None

        # Main category will be first
        category = [{
            'name': c.span.string,
            'category_id': c.attrs['href'].split('/')[-1],
            'url': urlparse.urljoin(
                self._base_url, c.attrs['href'])} for c in soup.select('.category')]

        description_soup = soup.select_one('div.show-more-content.text-body div')
        description = "\n".join([x.replace(u"’", u"'").encode('utf-8') for x in description_soup.stripped_strings])
        description_html = "".join([str(x.encode('utf-8')).replace("’", "'") for x in description_soup.contents])

        # Reviews & Ratings
        try:
            score = float(soup.select_one('meta[itemprop="ratingValue"]').attrs['content'])
        except AttributeError:
            score = None
            pass

        histogram = {}
        try:
            reviews = int(soup.select_one('meta[itemprop="ratingCount"]').attrs['content'])
            ratings_section = soup.select_one('div.rating-histogram')
            ratings = [int(r.string.replace(',', '')) for r in ratings_section.select('span.bar-number')]
            for i in range(5):
                histogram[5 - i] = ratings[i]
        except AttributeError:
            reviews = None
            pass

        recent_changes = "\n".join([x.string.strip() for x in soup.select('div.recent-change')])
        top_developer = bool(soup.select_one('meta[itemprop="topDeveloperBadgeUrl"]'))
        editors_choice = bool(soup.select_one('meta[itemprop="editorsChoiceBadgeUrl"]'))
        price = soup.select_one('meta[itemprop="price"]').attrs['content']
        free = (price == '0')

        # Additional information section
        additional_info = soup.select_one('div.metadata div.details-section-contents')
        updated = additional_info.select_one('div[itemprop="datePublished"]').string
        size = additional_info.select_one('div[itemprop="fileSize"]')
        if size:
            size = size.string.strip()

        try:
            installs = [int(n.replace(',', '')) for n in additional_info.select_one(
                'div[itemprop="numDownloads"]').string.strip().split(" - ")]
        except AttributeError:
            installs = [0, 0]

        current_version = additional_info.select_one('div[itemprop="softwareVersion"]')
        if current_version:
            current_version = current_version.string.strip()

        required_android_version = additional_info.select_one('div[itemprop="operatingSystems"]').string.strip()
        content_rating = additional_info.select_one('div[itemprop="contentRating"]').string

        meta_info = additional_info.select('.title')
        meta_info_titles = [x.string.strip() for x in meta_info]
        try:
            i_elements_index = meta_info_titles.index('Interactive Elements')
            interactive_elements = meta_info[i_elements_index].next_sibling.next_sibling.string.split(', ')
        except ValueError:
            interactive_elements = []
            pass

        offers_iap = bool(soup.select_one('div.inapp-msg'))
        iap_range = None
        if offers_iap:
            try:
                iap_price_index = meta_info_titles.index('In-app Products')
                iap_range = meta_info[iap_price_index].string
            except ValueError:
                iap_range = 'Not Available'
                pass

        developer = soup.select_one('span[itemprop="name"]').string
        developer_email = additional_info.select_one('a[href^="mailto"]').attrs['href'].split(":")[1]
        developer_url = additional_info.select_one('a[href^="https://www.google.com"]')
        if developer_url:
            developer_url = developer_url.attrs['href'].split("&")[0].split("=")[1]
        developer_address = additional_info.select_one('.physical-address')
        if developer_address:
            developer_address = developer_address.string

        return {
            'app_id': app_id,
            'title': title,
            'icon': icon,
            'url': url,
            'screenshots': screenshots,
            'thumbnails': thumbnails,
            'video': video,
            'category': category,
            'score': score,
            'histogram': histogram,
            'reviews': reviews,
            'description': description,
            'description_html': description_html,
            'recent_changes': recent_changes,
            'top_developer': top_developer,
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
            'iap': offers_iap,
            'iap_range': iap_range,
            'developer': developer,
            'developer_email': developer_email,
            'developer_url': developer_url,
            'developer_address': developer_address
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

        app_strainer = SoupStrainer('div', {'class': 'main-content'})
        apps = []
        errors = []
        for i, r in enumerate(responses):
            if r is not None and r.status_code == requests.codes.ok:
                soup = BeautifulSoup(r.content, 'lxml', parse_only=app_strainer)
                apps.append(self._parse_app_details(soup))
            else:
                errors.append(app_ids[i])
        return apps

    def details(self, app_id):
        """Sends a GET request and parses an application's details.

        :param app_id: the app to retrieve details from, e.g. 'com.nintendo.zaaa'
        :return: a dictionary of app details
        """
        url = build_url('details', app_id)
        response = send_request('GET', url)
        soup = BeautifulSoup(response.content, 'lxml')
        return self._parse_app_details(soup)

    def collection(self, collection, category=None, results=None, page=None, detailed=False):
        """Sends a POST request and fetches a list of applications belonging to
        the collection and an optional category.

        :param collection: the collection id, e.g. 'NEW_FREE'.
        :param category: (optional) the category name, e.g. 'GAME_ACTION'.
        :param results: the number of apps to retrieve at a time.
        :param page: page number to retrieve; limitation: page * results <= 500.
        :param detailed: if True, sends request per app for its full detail
        :return: a list of app dictionaries
        """
        collection = self.collections[collection]
        category = '' if category is None else self.categories[category]
        results = s.NUM_RESULTS if results is None else results
        page = 0 if page is None else page

        url = build_collection_url(category, collection)
        data = generate_post_data(results, page)
        response = send_request('POST', url, data)

        if detailed:
            apps = self._parse_multiple_apps(response)
        else:
            soup = BeautifulSoup(response.content, 'lxml')
            apps = [self._parse_card_info(app) for app in soup.select('div[data-uitype=500]')]

        return apps

    def developer(self, developer, results=None, detailed=False):
        """Sends a POST request and retrieves a list of the developer's published
        applications on the Play Store.

        :param developer: developer name to retrieve apps from, e.g. 'Disney'
        :param results: the number of app results to retrieve
        :param detailed: if True, sends request per app for its full detail
        :return: a list of app dictionaries
        """
        results = s.DEV_RESULTS if results is None else results
        url = build_url('developer', developer)
        data = generate_post_data(results)
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
        pagtok = self._pagtok[page]
        data = generate_post_data(0, 0, pagtok)

        params = {
            'q': urllib.quote_plus(query),
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
