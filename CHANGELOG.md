# Changelog

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
