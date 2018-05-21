# Play Store Scraper

Scrapes and parses application data from the Google Play Store.

### Installation

Install with pip.

```
pip install play-scraper
```

### Usage

* [details](#details): Fetch an application's details
* [collection](#collection): Fetch a list of applications and their details.
* [developer](#developer): Fetch a developer's offered applications.
* [suggestions](#suggestions): Fetch a list of query string suggestions.
* [search](#search): Fetch applications matching a search query.
* [similar](#similar): Fetch an application's similar apps.
* [categories](#categories): Fetch a list of available categories.

#### details

Fetch an application's details.

Options:

* `app_id` the app id to get, e.g. `com.android.chrome` for Google Chrome.

```python
>>> import play_scraper
>>> print play_scraper.details('com.android.chrome')
{
    'app_id': 'com.android.chrome',
    'category': ['COMMUNICATION'],
    'content_rating': ['Everyone'],
    'current_version': 'Varies with device',
    'description': 'Google Chrome is a fast, easy to use, and secure web browser. Designed for Android, Chrome brings you personalized news ...',
    'description_html': 'Google Chrome is a fast, easy to ... Chrome web browser experience you love across all your devices.<br/> <br/> <b>Browse fast and type less.</b> ...',
    'developer': 'Google LLC',
    'developer_address': '1600 Amphitheatre Parkway, Mountain View 94043',
    'developer_email': 'apps-help@google.com',
    'developer_id': '5700313618786177705',
    'developer_url': 'http://www.google.com/chrome/android',
    'editors_choice': False,
    'free': True,
    'histogram': { 1: 672180, 2: 288519, 3: 735220, 4: 1560066, 5: 6033423},
    'iap': False,
    'iap_range': None,
    'icon': 'https://lh3.googleusercontent.com/nYhPnY2I-e9rpqnid9u9aAODz4C04OycEGxqHG5vxFnA35OGmLMrrUmhM9eaHKJ7liB-',
    'installs': '1,000,000,000+',
    'interactive_elements': ['Unrestricted Internet'],
    'price': '0',
    'recent_changes': u"Thanks for choosing Chrome! You can now find your saved passwords more easily \u2013 just tap the new Search icon in Settings > Passwords. We've also included stability and performance improvements.",
    'required_android_version': 'Varies with device',
    'reviews': 9289408,
    'score': '4.3',
    'screenshots': [ 'https://lh3.googleusercontent.com/lKPDNfsO2QhJD9i77rGDTiH5ILjXlXwPsRi194hhkY4BsbaXbpCFrdjWvcU1zttUwqXz=w720-h310-rw', ...],
    'size': 'Varies with device',
    'title': 'Google Chrome: Fast & Secure',
    'updated': 'May 10, 2018',
    'url': 'https://play.google.com/store/apps/details?id=com.android.chrome',
    'video': None
}
```

#### collection

Fetch a list of applications from a collection, optionally filtered by category.

Options:

* `collection` a [collection](https://github.com/danieliu/play-scraper/blob/master/play_scraper/lists.py#L3) to fetch.
* `category` (default None) a [category](https://github.com/danieliu/play-scraper/blob/master/play_scraper/lists.py#L12) to filter by.
* `results` (default 60, max 120) the number of apps to fetch.
* `page` (default 0) the page number to fetch. Limit: `page * results <= 500`.
* `age` (default None) an [age range](https://github.com/danieliu/play-scraper/blob/master/play_scraper/lists.py#L67) to filter by. (Only for FAMILY categories)
* `detailed` (default False) if True, sends a request per app to fetch the full [details](#details).

```python
>>> import play_scraper
>>> print play_scraper.collection(
        collection='TRENDING',
        category='GAME_RACING',
        results=5,
        page=1)
[ { 'app_id': 'blaze.andthemonstermachinesferr',
    'description': 'Blaze The Monster Truck Mud Mountain Rescue - Monster Machines game for kids',
    'developer': 'app Star',
    'developer_id': 'app+Star',
    'free': True,
    'full_price': None,
    'icon': 'https://lh3.googleusercontent.com/cUk9UciJkqFUE4HVBiif9JUD8rWEXJCewG2JKVK9abWRaK3AMmIaSB61xlKGzIdw8w',
    'price': '0',
    'score': '4.3',
    'title': 'Blaze and the Monster Machines Free',
    'url': 'https://play.google.com/store/apps/details?id=blaze.andthemonstermachinesferr'},
  { 'app_id': 'com.notdoppler.earntodie2',
    'description': 'Drive your car through a zombie apocalypse in this epic sequel to Earn to Die!',
    'developer': 'Not Doppler',
    'developer_id': 'Not+Doppler',
    'free': True,
    'full_price': None,
    'icon': 'https://lh3.googleusercontent.com/PeYxYz56AltCaJaRu5OebqewOTqUoR9vU_jPavcphz1CywaU4d69My-cc9Stzx4DTTI',
    'price': '0',
    'score': '4.6',
    'title': 'Earn to Die 2',
    'url': 'https://play.google.com/store/apps/details?id=com.notdoppler.earntodie2'}, ...]
```

#### developer

Fetch a developer's offered applications.

Options:

* `developer` the developer name to fetch applications, e.g. `Disney`. (Case sensitive)
* `results` (default 24, max 120) the number of apps to fetch. (Developer may have more or less published apps)
* `page` (default 0) the page number to fetch. Limit: `0 < (results // 20) * page < 12`
* `detailed` (default False) if True, sends a request per app to fetch the full details as in [details](#details).

```python
>>> import play_scraper
>>> print play_scraper.developer('Disney', results=5)
[ { 'app_id': 'com.disney.datg.videoplatforms.android.watchdc',
    'description': 'Disney Channel, Disney XD & Disney Junior\u2019s new home for shows, games & live TV!',
    'developer': 'Disney',
    'developer_id': 'Disney',
    'free': True,
    'full_price': None,
    'icon': 'https://lh3.googleusercontent.com/C6CkMLr6s5bglWHr-2tH0Tdm138_6LCaevR14_fGV9kEPsoCF5t-L5pOQyOic4WsAnoU',
    'price': '0',
    'score': '4.3',
    'title': 'DisneyNOW \u2013 TV Shows & Games',
    'url': 'https://play.google.com/store/apps/details?id=com.disney.datg.videoplatforms.android.watchdc'},
  { 'app_id': 'com.disney.wdw.android',
    'description': 'Walt Disney World Resort maps, wait times, tickets, FastPass+, dining & more.',
    'developer': 'Disney',
    'developer_id': 'Disney',
    'free': True,
    'full_price': None,
    'icon': 'https://lh3.googleusercontent.com/NERZ9v0bPh_RBFRAbJe9cgGvk_DDIQCyWJc0YQ6LhRSGC51tQErHa8Rs9oFmzPRb9KQ',
    'price': '0',
    'score': '4.7',
    'title': 'My Disney Experience',
    'url': 'https://play.google.com/store/apps/details?id=com.disney.wdw.android'}, ...]
```

#### suggestions

Fetch a list of autocompleted query suggestions.

```python
>>> import play_scraper
>>> print play_scraper.suggestions('cat')
['cat games', 'cats', 'cat simulator', 'catan', 'cats in the cradle']
```

#### search

Fetch a list of applications matching a search query. Retrieves `20` apps at a time.

Options:

* `query` query term(s) to search for.
* `page` (default 0, max 12) page number of results to retrieve.
* `detailed` (default False) if True, sends a request per app to fetch the full details as in [details](#details).

```python
>>> import play_scraper
>>> print play_scraper.search('dogs', page=2)
[ { 'app_id': 'com.tivola.doghotel',
    'description': 'Be head of your own hotel and care for labradors, terrier and many more dogs!',
    'developer': 'Tivola',
    'developer_id': '8927372468482477196',
    'free': True,
    'full_price': None,
    'icon': 'https://lh3.googleusercontent.com/_PS_uqG8tjaqS014cN4bNUxQlHKsICWPW6bALReSrpK85CdI-ZkUOA3MT-vO20mVCP1w',
    'price': '0',
    'score': '4.4',
    'title': 'DogHotel : My Dog Boarding Kennel',
    'url': 'https://play.google.com/store/apps/details?id=com.tivola.doghotel'},
  { 'app_id': 'com.clan.of.dogs',
    'description': 'Clan of Dogs 3D Animal Adventure Simulator',
    'developer': 'Wild Foot Games',
    'developer_id': '6061726228463739055',
    'free': True,
    'full_price': None,
    'icon': 'https://lh3.googleusercontent.com/JO2cxKk5L3onmu2dchAeRRZyWJuJ5q7veWenP7uSZfItcJLsq1pZPIEoDqc_QNOqp-Q',
    'price': '0',
    'score': '4.2',
    'title': 'Clan of Dogs',
    'url': 'https://play.google.com/store/apps/details?id=com.clan.of.dogs'}, ...]
```

#### similar

Fetch a list of similar applications.

Options:

* `app_id` the app id to get, e.g. `com.supercell.clashofclans` for Clash of Clans.
* `results` (default 24, max 60) the number of apps to fetch.
* `detailed` (default False) if True, sends a request per app to fetch the full details as in [details](#details).

```python
>>> import play_scraper
>>> print play_scraper.similar('com.supercell.clashofclans', results=5)
[ { 'app_id': 'com.supercell.clashroyale',
    'description': 'Clash Royale is a real-time, head-to-head battle game set in the Clash Universe.',
    'developer': 'Supercell',
    'developer_id': '6715068722362591614',
    'free': True,
    'full_price': None,
    'icon': 'https://lh3.googleusercontent.com/K-MNjDiO2WwRNwJqPZu8Wd5eOmFEjLYkEEgjZlv35hTiua_VylRPb04Lig3YZXLERvI',
    'price': '0',
    'score': '4.6',
    'title': 'Clash Royale',
    'url': 'https://play.google.com/store/apps/details?id=com.supercell.clashroyale'},
  { 'app_id': 'com.supercell.boombeach',
    'description': 'Storm the beach and win the day!',
    'developer': 'Supercell',
    'developer_id': '6715068722362591614',
    'free': True,
    'full_price': None,
    'icon': 'https://lh3.googleusercontent.com/sw4Zb0qt_0-Iqm4YHpXEaGhmj6e3GlHmYroBI8oBuBr4JpRnFF37VmMDaqLMT-MDvhg',
    'price': '0',
    'score': '4.5',
    'title': 'Boom Beach',
    'url': 'https://play.google.com/store/apps/details?id=com.supercell.boombeach'}, ...]
```

#### categories

Fetch a list of available categories.

```python
>>> import play_scraper
>>> play_scraper.categories()
{'ANDROID_WEAR': { 'category_id': 'ANDROID_WEAR',
                 'name': 'Wear OS by Google',
                 'url': 'https://play.google.com/store/apps/category/ANDROID_WEAR'},
 'ART_AND_DESIGN': { 'category_id': 'ART_AND_DESIGN',
                     'name': 'Art & Design',
                     'url': 'https://play.google.com/store/apps/category/ART_AND_DESIGN'}, ...}
```

### Tests

Run tests:
```
make test
```
