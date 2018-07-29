# -*- coding: utf-8 -*-

"""
Google Play Store Scraper

A web scraper for the Google Play Android app store.
"""

__version__ = '0.4.0'

import logging

from play_scraper.api import (
    collection,
    details,
    developer,
    search,
    similar,
    suggestions,
    categories,
)


# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


logging.getLogger(__name__).addHandler(NullHandler())
