# Play Store Scraper

Scrapes and parses application data from the Google Play Store.

### Installation

```
pip install -r requirements.txt
```

### Usage

* [app](#app): Fetches the details of an application.
* [collection](#collection): Fetches a list of application details.

#### app

Fetch an application's details by its id.

For example:
```python
from play_scraper import PlayScraper

scraper = PlayScraper()
print(scraper.app('com.miniclip.basketballstars'))
```

Result:
```python
{   
    'app_id': 'com.miniclip.basketballstars',
    'category': [{'category_id': 'GAME_SPORTS', 'name': u'Sports', 'url': '/store/apps/category/GAME_SPORTS'}],
    'content_rating': u'Everyone',
    'current_version': u'1.0.3',
    'description': "The world's best multiplayer Basketball game on mobile, from the creators of multiple smash-hit online sports games!\nDribble, shoot, score, WIN! Grab the ball and take on the world with BASKETBALL STARS.\n ...",
    'description_html': 'The world\'s best multiplayer Basketball game on mobile, from the creators of multiple smash-hit online sports games!<p>Dribble, shoot, score, WIN! Grab the ball and take on the world with BASKETBALL STARS.</p> ...',
    'developer': u'Miniclip.com',
    'developer_address': u'Miniclip SA\nCase Postale 2671\n2001 Neuch\xe2tel\nSwitzerland',
    'developer_email': 'support@miniclip.com',
    'developer_url': 'http://www.miniclip.com/',
    'free': True,
    'histogram': {1: 13743, 2: 3757, 3: 9321, 4: 24500, 5: 108008},
    'icon': 'https://lh3.googleusercontent.com/Phk5qqQ1Fs-mQACNeuZjqsWIJJknpoSXBmQFi0vRw2IlO0nZ7H8O8rYUvwcVvfk-wdY=w300-rw',
    'in_app_purchases': u'In-app Products',
    'installs': [5000000, 10000000],
    'interactive_elements': [u'Digital Purchases'],
    'offers_iap': True,
    'price': '0',
    'recent_changes': u'\u2022 Weekly leaderboard competition \u2013 showcase your skills against the best in your country. Can you be the champion? ...',
    'required_android_version': u'4.0.3 and up',
    'reviews': 159329,
    'score': 4.313464641571045,
    'screenshots': ['https://lh3.googleusercontent.com/dxK8v2v3EcHqAt2mF-jeihBYhWq7iQRa0fGeIb0N5FEbnnUSgnDCcaPn1omYW6MHQg=h900-rw', ...],
    'size': u'43M',
    'thumbnails': ['https://lh3.googleusercontent.com/dxK8v2v3EcHqAt2mF-jeihBYhWq7iQRa0fGeIb0N5FEbnnUSgnDCcaPn1omYW6MHQg=h310-rw', ...],
    'title': u'Basketball Stars',
    'top_developer': True,
    'updated': u'March 14, 2016',
    'url': 'https://play.google.com/store/apps/details?id=com.miniclip.basketballstars',
    'video': None
}
```

#### collection

Fetch a full list of applications and their details.

* `collection` (optional, default `TOP_FREE`) See [settings](https://github.com/danieliu/PlayScraper/blob/master/play_scraper/settings.py#L23) for a list of options.
* `category` (optional) See [settings](https://github.com/danieliu/PlayScraper/blob/master/play_scraper/settings.py#L79) for a list of options.

For example:

```python
from play_scraper import PlayScraper

scraper = PlayScraper()
print scraper.collection(
    category='GAME_ACTION',
    collection='TRENDING')
```



### Tests

Running tests:

    python -m unittest discover [-v]
