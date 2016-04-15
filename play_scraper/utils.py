# -*- coding: utf-8 -*-

import urllib

import requests
import grequests
from bs4 import BeautifulSoup, SoupStrainer

from .logger import configure_logging


BASE_URL = 'https://play.google.com/store/apps'
SUGGESTION_URL = 'https://market.android.com/suggest/SuggRequest'

CONCURRENT_REQUESTS = 10
USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/45.0.2454.101 Safari/537.36')

logger = configure_logging()


def _handle_grequest_exception(request, exception):
    print("{exception} with {url}".format(exception=exception, url=request.url))
    return None


def default_headers():
    return {
        'Origin': 'https://play.google.com',
        'User-Agent': USER_AGENT,
        'Content-obj_type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }


def generate_post_data(results=None, page=None, children=0):
    """
    Creates the post data for a POST request. Mainly for pagination and
    limiting results.

    :param results: the number of results to return
    :param page: the page number; used to calculate start = page * results
    :param children: number of apps under each collection (used only when scraping
        a top-level category's collections)
    :return: a dictionary of post data
    """
    data = {
        'ipf': 1,
        'xhr': 1
    }
    if children:
        data['numChildren'] = children
    if results is not None:
        if page is not None:
            start = 0 if page <= 0 else results * page
            data['start'] = start
        data['num'] = results

    return data


def build_url(obj_type, id_string):
    """Creates the absolute url for a type of object. E.g. details, developer,
    or similar.

    :param obj_type: the object type to get
    :param id: the id query parameter string
    :return: a URL string
    """
    if obj_type == 'developer':
        id_string = urllib.quote_plus(id_string)

    url = "{base}/{obj_type}?id={id}".format(
        base=BASE_URL, obj_type=obj_type, id=id_string)
    return url


def build_collection_url(category='', collection=''):
    """
    Creates the absolute url based on the category and collection id's.
    """
    if category:
        category = "/category/{cat_id}".format(cat_id=category['category_id'])
    if collection:
        collection = "/collection/{col_id}".format(col_id=collection['collection_id'])

    url = "{base}{category}{collection}".format(
        base=BASE_URL,
        category=category,
        collection=collection)

    return url


def send_request(method, url, data=None, params=None, headers=None, verify=True):
    """Sends a request to the url and returns the response.

    :param method: HTTP method to use.
    :param url: URL to send.
    :param data: Dictionary of post data to send.
    :param headers: Dictionary of headers to include.
    :param verify: Bool for request SSL verification.
    """
    data = {} if data is None else data
    params = {} if params is None else params
    headers = default_headers() if headers is None else headers
    if not data and method == 'POST':
        data = generate_post_data()

    try:
        response = requests.request(
            method=method,
            url=url,
            data=data,
            params=params,
            headers=headers,
            verify=verify)
        if not response.status_code == requests.codes.ok:
            response.raise_for_status()
    except requests.exceptions.RequestException:
        return None

    return response


def multi_request(apps, size=None, headers=None, verify=True):
    """Sends requests to each app and returns a list of responses.

    :param apps: List of app IDs
    """
    size = CONCURRENT_REQUESTS if size is None else size
    headers = default_headers() if headers is None else headers

    reqs = (
        grequests.get(
            build_url('details', app_id),
            headers=headers,
            verify=verify) for app_id in apps)

    responses = grequests.map(
        reqs,
        size=size,
        exception_handler=_handle_grequest_exception)

    return responses


def get_categories():
    """
    Sends a GET request to the front page (base url of the app store),
    parses and returns a list of all available categories.

    Note: May contain some promotions, e.g. "Popular Characters"
    """
    categories = {}
    strainer = SoupStrainer('a', {'class': 'child-submenu-link'})

    response = send_request('GET', BASE_URL)
    soup = BeautifulSoup(response.content, 'lxml', parse_only=strainer)
    category_links = soup.select('a.child-submenu-link')

    for cat in category_links:
        url = cat.attrs['href']
        category_id = url.split('/')[-1]
        categories[category_id] = {
            'name': cat.string,
            'url': url,
            'category_id': category_id}

    return categories
