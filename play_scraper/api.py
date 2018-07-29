# -*- coding: utf-8 -*-

"""
play_scraper.api

:copyright: (c) 2016 Daniel Liu.
:license: MIT, see LICENSE for more details.

"""

from play_scraper import scraper


def details(app_id, **kwargs):
    """Sends a GET request to the app's info page, parses the app's details, and
    returns them as a dict.

    :param app_id: the app to retrieve details from, e.g. 'com.nintendo.zaaa'
    :return: a dictionary of app details
    """
    s = scraper.PlayScraper(**kwargs)
    return s.details(app_id)


def collection(collection, category=None, **kwargs):
    """Sends a POST request to the collection url, gets each app's details, and
    returns them in a list.

    List of acceptable collections and categories can be found in settings.

    :param collection: the collection ID as a string.
    :param category: the category ID as a string.
    :param results: the number of app results to retrieve
    :param page: the page number, calculates collection start index. is limited
        to page * results <= 500
    :param age: an age range to filter by (only for FAMILY categories)
    :param detailed: if True, sends request per app for full detail
    :return: a list of app dictionaries
    """
    s = scraper.PlayScraper(**kwargs)
    return s.collection(collection, category, **kwargs)


def developer(developer, **kwargs):
    """Sends a POST request to the developer's page, extracts their apps' basic
    info, and returns them in a list.

    :param developer: developer name to retrieve apps from, e.g. 'Disney'
    :param results: the number of app results to retrieve
    :param page: the page number to retrieve
    :param detailed: if True, sends request per app for full detail
    :return: a list of app dictionaries
    """
    s = scraper.PlayScraper(**kwargs)
    return s.developer(developer, **kwargs)


def suggestions(query, **kwargs):
    """Sends a GET request to the Play Store's suggestion API and returns up to
    five autocompleted suggested query strings in a list.

    :param query: the query string to get autocomplete suggestions
    :return: a list of suggestion strings
    """
    s = scraper.PlayScraper(**kwargs)
    return s.suggestions(query)


def search(query, **kwargs):
    """Sends a POST request and retrieves a list of applications matching
    the query term(s).

    :param query: search query term(s) to retrieve matching apps
    :param page: the page number to retrieve; max is 12
    :param detailed: if True, sends request per app for its full detail
    :return: a list of apps matching search terms
    """
    s = scraper.PlayScraper(**kwargs)
    return s.search(query, **kwargs)


def similar(app_id, **kwargs):
    """Sends a GET request, follows the redirect, and retrieves a list of
    applications similar to the specified app.

    :param app_id: the app to retrieve details from, e.g. 'com.nintendo.zaaa'
    :param detailed: if True, sends request per app for its full detail
    :return: a list of similar apps
    """
    s = scraper.PlayScraper(**kwargs)
    return s.similar(app_id, **kwargs)


def categories(**kwargs):
    """Sends a GET request to the front page (app store base url), parses and
    returns a list of all available categories.

    Note: May contain some promotions, e.g. "Popular Characters"
    """
    s = scraper.PlayScraper(**kwargs)
    return s.categories()
