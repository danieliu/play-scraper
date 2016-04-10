# -*- coding: utf-8 -*-

import requests
from urlparse import urljoin

import grequests
from bs4 import BeautifulSoup

from logger import configure_logging
from settings import (BASE_URL, HEADERS, VERIFY_SSL, CONCURRENT_REQUESTS,
    NUM_COLLECTIONS, NUM_RESULTS, CATEGORIES, COLLECTIONS)


class PlayScraper(object):
    def __init__(self, **kwargs):
        self.categories = CATEGORIES
        self.collections = COLLECTIONS
        self._base_url = BASE_URL
        self._verify = VERIFY_SSL
        self._headers = HEADERS
        self._num_results = NUM_RESULTS
        self._num_collections = NUM_COLLECTIONS
        self._logger = configure_logging()

    def _handle_grequest_exception(self, request, exception):
        self._logger.error("{exception} with {url}".format(
            exception=exception, url=request.url))
        return None

    def _app_url(self, app_id):
        """
        Returns a full url string to the corresponding app id
        """
        return "{base}/details?id={app_id}".format(
            base=self._base_url,
            app_id=app_id)

    def _list_url(self, category='', collection=''):
        """
        Creates the absolute url based on the category and collection id's.
        """
        if category:
            category = "/category/{cat_id}".format(cat_id=category['category_id'])
        if collection:
            collection = "/collection/{col_id}".format(col_id=collection['collection_id'])
        return "{base}{category}{collection}".format(
            base=self._base_url,
            category=category,
            collection=collection)

    def _get_soup(self, url, method='POST', data={}):
        """
        Sends a request to the url and turns the response into a soup object.
        """
        if not data and method == 'POST':
            data = self._generate_post_data()
        try:
            self._logger.info("Sending {method} to '{url}'".format(
                method=method, url=url))
            response = requests.request(
                method=method,
                url=url,
                data=data,
                headers=self._headers,
                verify=self._verify)
            if response.status_code == requests.codes.ok:
                soup = BeautifulSoup(response.content, 'lxml')
                self._logger.info("Soup created.")
                return soup
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self._logger.error("{e} at {url}".format(e=e, url=url))
            raise

    def _generate_post_data(self, results=None, page=None, children=0):
        """
        Creates the post data for a POST request. Mainly for pagination and
        limiting results.
        """
        data = {
            'ipf': 1,
            'xhr': 1
        }
        if children:
            data['numChildren'] = children
        if results is not None and page is not None:
            start = 0 if page <= 0 else results * page
            data['start'] = start
            data['num'] = results
        return data

    def _get_categories(self):
        """
        Sends a GET request to the front page (base url of the app store),
        parses and returns a list of all available categories.

        May contain some promotions, e.g. "Popular Characters"
        """
        categories = {}
        home_page = self._base_url
        soup = self._get_soup(home_page)
        category_links = soup.select('a.child-submenu-link')
        for cat in category_links:
            url = cat.attrs['href']
            categories[cat.string] = {
                'name': cat.string,
                'url': url,
                'category_id': url.split('/')[-1]}
        return categories

    def _get_collections(self, soup):
        """
        Parse collection titles, ids, and URLs from the top-level category and
        return them in a list.
        """
        collections = []
        links = soup.select('a.see-more')
        for a in links:
            name = a.parent.previous_sibling.previous_sibling.string
            url = a.attrs['href']
            collection = url.split('/')[-1]
            if collection not in self.collections:
                collections.append({
                    'name': name,
                    'url': url,
                    'collection': collection
                })
        return collections

    def _get_app_details(self, soup):
        app_id = soup.select_one('span.play-button').attrs['data-docid']
        url = soup.select_one('link[rel="canonical"]').attrs['href']
        title = soup.select_one('div.id-app-title').string
        icon = urljoin(self._base_url, soup.select_one('img.cover-image').attrs['src'])
        screenshots = [
            urljoin(self._base_url, s.attrs['src']) for s in soup.select('img.full-screenshot')]
        thumbnails = [
            urljoin(self._base_url, s.attrs['src']) for s in soup.select('img.screenshot')]

        try:
            video = soup.select_one('span.preview-overlay-container').attrs.get('data-video-url', None)
            if video:
                video = video.split('?')[0]
        except AttributeError:
            video = None

        # Main category will be first
        category = [{
            'name': c.span.string,
            'category_id': c.attrs['href'].split('/')[-1],
            'url': c.attrs['href']} for c in soup.select('.category')]

        description_soup = soup.select_one('.show-more-content.text-body div')
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
            ratings = [int(r.string.replace(',', '')) for r in soup.select('span.bar-number')]
            for i in range(5):
                histogram[5 - i] = ratings[i]
        except AttributeError:
            reviews = None
            pass

        recent_changes = "\n".join([x.string.strip() for x in soup.select('.recent-change')])
        top_developer = bool(soup.select_one('meta[itemprop="topDeveloperBadgeUrl"]'))
        price = soup.select_one('meta[itemprop="price"]').attrs['content']
        free = (price == '0')

        # Additional information section
        additional_info = soup.select_one('.metadata .details-section-contents')
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

        offers_iap = bool(soup.select_one('.inapp-msg'))
        in_app_purchases = None
        if offers_iap:
            try:
                iap_price_index = meta_info_titles.index('In-app Products')
                in_app_purchases = meta_info[iap_price_index].string
            except ValueError:
                self._logger.warning(
                    "In-app purchases range not found for '{app}'".format(
                        app=app_id))
                pass

        developer = soup.select_one('span[itemprop="name"]').string
        developer_email = additional_info.select_one('a[href^="mailto"]').attrs['href'].split(":")[1]
        developer_url = additional_info.select_one('a[href^="https://www.google.com"]')
        if developer_url:
            developer_url = developer_url.attrs['href'].split("&")[0].split("=")[1]
        developer_address = additional_info.select_one('.physical-address')
        if developer_address:
            developer_address = developer_address.string

        self._logger.info("Parsed app details for '{app}'".format(app=title.encode('utf-8')))

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
            'price': price,
            'free': free,
            'updated': updated,
            'size': size,
            'installs': installs,
            'current_version': current_version,
            'required_android_version': required_android_version,
            'content_rating': content_rating,
            'interactive_elements': interactive_elements,
            'offers_iap': offers_iap,
            'in_app_purchases': in_app_purchases,
            'developer': developer,
            'developer_email': developer_email,
            'developer_url': developer_url,
            'developer_address': developer_address
        }

    def app(self, app_id=None):
        """
        Fetches an application's details.
        """
        if not app_id:
            raise ValueError("No App ID provided.")

        url = self._app_url(app_id)
        soup = self._get_soup(url, method='GET')
        return self._get_app_details(soup)

    def collection(self, **kwargs):
        """
        Fetches applications from a collection and returns their details in a list

        :param collection: (optional, defaults to TOP_FREE) the collection name,
            e.g. TOP_NEW_FREE
        :param category: (optional) the category name, e.g. ANDROID_WEAR.
        """
        collection_id = kwargs.pop('collection', 'TOP_FREE')
        category_id = kwargs.pop('category', '')

        collection = self.collections[collection_id]
        if category_id:
            category = self.categories[category_id]

        url = self._list_url(category_id, collection_id)
        page = 0
        apps = []

        while True:
            self._logger.info("Retrieving page {page} of {col}".format(
                page=page, col=collection['name']))

            post_data = self._generate_post_data(self._num_results, page)
            soup = self._get_soup(url, data=post_data)
            current_apps = [x.attrs['data-docid'] for x in soup.select('.card-content')]

            reqs = (grequests.request(
                method='GET',
                url=self._app_url(app_id),
                headers=self._headers,
                verify=self._verify) for app_id in current_apps)
            responses = grequests.map(
                reqs,
                size=CONCURRENT_REQUESTS,
                exception_handler=self._handle_grequest_exception)

            self._logger.info("Parsing {num} apps...".format(num=len(responses)))

            for i, response in enumerate(responses):
                if not response:
                    self._logger.info("No response for '{app_id}'".format(
                        app_id=current_apps[i]))
                else:
                    if not response.status_code == requests.codes.ok:
                        self._logger.error("{e} at {url}".format(
                            e=response.status_code,
                            url=response.url))
                    else:
                        soup = BeautifulSoup(response.content, 'lxml')
                        apps.append(self._get_app_details(soup))

            page += 1

            if len(current_apps) < self._num_results or page * self._num_results > 500:
                break

        self._logger.info("Parsed {num} apps from {cat}'s {col}".format(
            num=len(apps), cat=category['name'], col=collection['name']))

        return apps

    def category(self, **kwargs):
        """
        Main scraping function.

        Sends a POST request to a category's url, paginates and retrieves all
        collection urls.
        Crawls each collection to scrape app urls and IDs.
        Parse each app's details.
        """
        category = kwargs.pop('category', None)
        if not category:
            raise ValueError("No category specified.")
        category_url = self._list_url(category)

        results = self._NUM_COLLECTIONS
        page = 0
        children = 1
        collections = []

        while True:
            post_data = self._generate_post_data(results, page, children)
            soup = self._get_soup(category_url, data=post_data)
            current = self._get_collections(soup)
            collections += current

            # 4/5/2016 Note: Play Store adds an ad now so may be one less
            # collection end loop when less than expected number of results, i.e.
            # reached max available collections
            if len(current) < (results - 1):
                break

            page += 1

        apps = []
        for c in collections:
            apps += self.parse_collection(c)

        return apps
