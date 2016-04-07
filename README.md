# Play Store Scraper

Scrapes and parses application data from the Google Play Store.

## Installation

Preferably use virtualenv, and install the dependencies:

	$ pip install -r requirements.txt

## Usage

* [parse_app](#parse_app): Parses available details of an application by id.
* [parse_category](#parse_category): Retrieves a list of apps 

#### parse_app

Parses available details of an application by id.

Example:
```python
scraper = PlayStoreScraper()
scraper.parse_app('com.miniclip.basketballstars')
```

Result:
```python
{
	'app_id': 'com.miniclip.basketballstars',
	'histogram': { 1: 7485, 2: 1961, 3: 4790, 4: 12401, 5: 59051},
	'icon': 'https://lh3.googleusercontent.com/Phk5qqQ1Fs-mQACNeuZjqsWIJJknpoSXBmQFi0vRw2IlO0nZ7H8O8rYUvwcVvfk-wdY=w300-rw',
	'reviews': 85688,
	'score': 4.325413227081299,
	'screenshots': ['https://lh3.googleusercontent.com/dxK8v2v3EcHqAt2mF-jeihBYhWq7iQRa0fGeIb0N5FEbnnUSgnDCcaPn1omYW6MHQg=h900-rw', ...],
	'thumbnails': ['https://lh3.googleusercontent.com/dxK8v2v3EcHqAt2mF-jeihBYhWq7iQRa0fGeIb0N5FEbnnUSgnDCcaPn1omYW6MHQg=h310-rw', ...],
	'title': u'Basketball Stars',
	'url': 'https://play.google.com/store/apps/details?id=com.miniclip.basketballstars'
}
```


# Notes

Begin with getting a list of all available categories:
	
	links = soup.find_all('a', 'child-submenu-link')
	for a in links:
		category_name = a.string
		category_url = a.attrs['href']

In each category, scrape the list of available collections:

	collections = soup.find_all('a', 'see-more')
	for a in collections:
		collection_name = a.parent.previous_sibling.string
		collection_url = a.attrs['href']



* Play around with `_generate_post_data` for sending simple post request to an app detail page. Output to .html and check if response is without all the headers like when crawling categories and collections.

* Use SoupStrainer to parse only relevant parts? Might be hard for app details but for categories and collections


### Tests

Run the following in the root project directory:

	python -m unittest discover [-v]
