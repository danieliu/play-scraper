# Changelog

### 0.5.0: 2018-12-11

* Fix category css selector
* Fix screenshot css selector
* Update requests version
* Fix missing kwargs for `search` and `similar`

### 0.4.2: 2018-10-01

* Added manifest to fix install-option, and update requires

### 0.4.1: 2018-08-12

* Remove `**kwargs` in favor of specified kwargs
* Update required `lxml` version

### 0.4.0: 2018-07-28

* Replace `grequests` with `requests-futures`
* Include Python 3.7 in multiversion testing
* Moved parsing functions into utils
* Add test coverage

### 0.3.2: 2018-07-23

* Avoid using the `alt` attribute as a selector because specifying a language will change the value.

### 0.3.1: 2018-07-22

* Quick fix on import error in `scraper.py`

### 0.3.0: 2018-07-22

* Add option to change the `hl` and `gl` query parameters for specifying language and geolocation (country), respectively.

### 0.2.5: 2018-07-22

* Raise when passed a developer_id instead of the developer name to `.developer()`

### 0.2.4: 2018-07-02

* None type check before calling `developer_address.strip()`
* Set test to check >= because number of apps fetched non-deterministic since we actually scrape

### 0.2.3: 2018-06-24

* Fix Python3 compatibility (basestring, unicode())

### 0.2.2: 2018-06-24

* Use Python primitive types instead of BeautifulSoup4's `NavigableString`

### 0.2.1: 2018-05-26

* Use requests[security] to fix SSL recursion errors

### 0.2.0: 2018-05-20

* Update parsing for details, collections, similar
* Fix and add tests for all of these
* Expose previously unused category list util as api

### 0.1.12: 2018-05-12

* Clean up some code here and there.
* Use absolute imports instead of relative.
* Switch README back to markdown now that PyPi supports it.

### 0.1.11: 2016-05-06

* Arabic in Current Version metadata fix

### 0.1.10: 2016-04-27

* Price not available (due to country restrictions?) and better handling with pre-register apps

### 0.1.9: 2016-04-26

* No description/description_html error handling, e.g. with app 'kumagames.onikuma' in detailed scrape

### 0.1.8: 2016-04-24

* Removed logging configs and replaced with nullhandler

### 0.1.7: 2016-04-24

* Pagination for developer method, using page tokens
* Added page token regex to settings for parsing out of response html script tags

### 0.1.6: 2016-04-23

* Added handling of 'pre-register' apps with more generalized selectors in basic card info and detailed parsing

### 0.1.5: 2016-04-22

* Fixed App detail URL and IAP range parsing with a proper selector and correctly traversing to the next next sibling, respectively
* Fixed error when developer email not available

### 0.1.4: 2016-04-21

* Added number of results and page number limit checks
* App ID raises exception when 404

### 0.1.3: 2016-04-20

* Python3 urllib.parse.quote_plus compatibility in scraper/utils
* Python3 import fixes
* No reviews (ratings) set to 0 instead of None
* Developer ID included when available
* Removed file logging

### 0.1.2: 2016-04-17

* Bugfix: AGE_RANGE params for fetching collections in the FAMILY category
* Bugfix: description_html doesn't include parent div  anymore
* README examples updates

### 0.1.1: 2016-04-17

* Added urljoin import compatibility for Python 3
* Simplified parsing description to just use unicode
