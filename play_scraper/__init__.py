"""
Google Play Store Scraper

A web scraper for the Google Play Android app store.
"""

__version__ = '0.1.0'

from .api import details, collection, developer, suggestions, search
from .scraper import PlayScraper
