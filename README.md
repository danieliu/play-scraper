# Play Store Scraper

Scrapes and parses application data from the Google Play Store.

### Installation

Either install requirements in a virtualenv or run the setup.
```
pip install -r requirements.txt
python setup.py install
```

### Usage

* [details](#details): Fetch an application's details
* [collection](#collection): Fetch a list of applications and their details.
* [developer](#developer): Fetch a developer's offered applications.
* [suggestions](#suggestions): Fetch a list of query string suggestions.
* [search](#search): Fetch applications matching a search query.
* [similar](#similar): Fetch an application's similar apps.

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
    'content_rating': u'Everyone',
    'current_version': u'Varies with device',
    'description': u'Browse fast on your Android phone and tablet with the Google Chrome browser you love on desktop. Pick up where ...',
    'description_html': u'Browse fast on your Android phone and tablet with the Google Chrome browser you love on desktop. Pick up where you left off on your other devices with tab sync, search by voice, and save up to 50% of data usage while browsing. <br/> ...',
    'developer': u'Google Inc.',
    'developer_address': u'1600 Amphitheatre Parkway, Mountain View 94043',
    'developer_email': 'apps-help@google.com',
    'developer_url': 'http://www.google.com/chrome/android',
    'editors_choice': False,
    'free': True,
    'histogram': { 1: 351453, 2: 158643, 3: 326653, 4: 735367, 5: 2679600},
    'iap': False,
    'iap_range': None,
    'icon': 'https://lh3.ggpht.com/O0aW5qsyCkR2i7Bu-jUU1b5BWA_NygJ6ui4MgaAvL7gfqvVWqkOBscDaq4pn-vkwByUx',
    'installs': [1000000000, 5000000000],
    'interactive_elements': [u'Unrestricted Internet'],
    'price': '0',
    'recent_changes': u'Bug fixes and speedy performance improvements.',
    'required_android_version': u'Varies with device',
    'reviews': 4251716,
    'score': 4.230801582336426,
    'screenshots': [ 'https://lh4.ggpht.com/6D21o4j_OJUnVCTARqcdajTmX_5_8UJtzVuN91smALZBuMq0p3MIvwZj2qofXeqmFIU=h900-rw', ...],
    'size': u'Varies with device',
    'thumbnails': [ 'https://lh4.ggpht.com/6D21o4j_OJUnVCTARqcdajTmX_5_8UJtzVuN91smALZBuMq0p3MIvwZj2qofXeqmFIU=h310-rw', ...],
    'title': u'Chrome Browser - Google',
    'top_developer': True,
    'updated': u'March 25, 2016',
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
* `page` (default 0) the page number to get. Limit: `page * results <= 500`.
* `age` (default None) an [age range](https://github.com/danieliu/play-scraper/blob/master/play_scraper/lists.py#L67) to filter by. (Only for FAMILY categories)
* `detailed` (default False) if True, sends a request per app to fetch the full [details](#details).

```python
>>> import play_scraper
>>> print play_scraper.collection(
        collection='TRENDING',
        category='GAME_RACING',
        results=5,
        page=1)
[ { 'app_id': 'com.horsepower1.doorslammers2',
    'description': u'Door Slammers 2 Online Drag Racing',
    'developer': 'Horsepower 1 Studios',
    'free': True,
    'icon': 'https://lh3.googleusercontent.com/zUousZ3vkqxTEyknUa2YV4KENr2UYKxN-3jQYhOgZ3qCFJL8RwYpTjyA2M4j33fQTcs',
    'price': '0',
    'score': '4.7',
    'title': 'Door Slammers',
    'url': 'https://play.google.com/store/apps/details?id=com.horsepower1.doorslammers2'},
  { 'app_id': 'com.craneballs.artdrive',
    'description': u'Paint the world a better place, one neighborhood at a time.',
    'developer': 'Craneballs',
    'free': True,
    'icon': 'https://lh3.googleusercontent.com/bMI0BCxhJIr-5KZfHG9Nwt7ikFvfW5chJaWzks_WIgod9loaWzpjKk98qpqlYIujUs4',
    'price': '0',
    'score': '4.1',
    'title': 'Splash Cars',
    'url': 'https://play.google.com/store/apps/details?id=com.craneballs.artdrive'}, ...]
```

#### developer

Fetch a developer's offered applications.

Options:

* `developer` the developer name to fetch applications, e.g. `Disney`. (Case sensitive)
* `results` (default 24) the number of apps to fetch. (Developer may have more or less published apps)
* `detailed` (default False) if True, sends a request per app to fetch the full details as in [details](#details).

```python
>>> import play_scraper
>>> print play_scraper.developer('Disney', results=5)
[ { 'app_id': 'com.disney.disneycrossyroad_goo',
    'description': u'An all-new take on the ultimate 8-bit endless adventure to cross the road!',
    'developer': 'Disney',
    'free': True,
    'icon': 'https://lh3.googleusercontent.com/mHHQ-GA_hu8shAEtzj8trGBOJK7dtMrmV4XXvjl49MQbIDHytb8kQenB4IaUB9NvYA',
    'price': '0',
    'score': '4.5',
    'title': 'Disney Crossy Road',
    'url': 'https://play.google.com/store/apps/details?id=com.disney.disneycrossyroad_goo'},
  { 'app_id': 'com.disney.disneydescendants_goo',
    'description': u'Join Mal, Evie, Jay & Carlos for a wickedly fun adventure in Descendants!',
    'developer': 'Disney',
    'free': True,
    'icon': 'https://lh3.googleusercontent.com/uzyRRHl7Jxy_TN1WKvp0rf1q9sS05JcTzmhILZI16Gbu4N7TGP88nHSQTPfBKwor5g',
    'price': '0',
    'score': '3.7',
    'title': 'Descendants',
    'url': 'https://play.google.com/store/apps/details?id=com.disney.disneydescendants_goo'}, ...]
```

#### suggestions

Fetch a list of autocompleted query suggestions.

```python
>>> import play_scraper
>>> print play_scraper.suggestions('cat')
[u'cat games', u'cat simulator', u'cat sounds', u'cat games for cats']
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
[ { 'app_id': 'com.lily.times.dog1.all',
    'description': u'Talking Puppy repeats everything you say with a funny voice.',
    'developer': 'Talking Baby',
    'free': True,
    'icon': 'https://lh6.ggpht.com/HkguMATxZvedgR3_FHTgg_UPtR7TR_lvVDIlx7t42tD5r6EPPTlctKb9rMdL9nnkmQ',
    'price': '0',
    'score': '4.4',
    'title': 'Talking Puppy',
    'url': 'https://play.google.com/store/apps/details?id=com.lily.times.dog1.all'},
  { 'app_id': 'org.hanoo.dogtraining',
    'description': u'Please prefer downloading the new version: DogTraining2',
    'developer': 'hanoo.org',
    'free': True,
    'icon': 'https://lh3.googleusercontent.com/mzTl58Q8aWRSBGejWvoqm-UoPvxVV5tOevt8Rp4pZUKe2b1hKykeT4EMo4-2ngcSzF2Q',
    'price': '0',
    'score': '3.3',
    'title': 'Dog Training',
    'url': 'https://play.google.com/store/apps/details?id=org.hanoo.dogtraining'}, ...]
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
    'description': u'Clash Royale is a real-time, head-to-head battle game set in the Clash Universe.',
    'developer': 'Supercell',
    'free': True,
    'icon': 'https://lh3.googleusercontent.com/K-MNjDiO2WwRNwJqPZu8Wd5eOmFEjLYkEEgjZlv35hTiua_VylRPb04Lig3YZXLERvI',
    'price': '0',
    'score': '4.5',
    'title': 'Clash Royale',
    'url': 'https://play.google.com/store/apps/details?id=com.supercell.clashroyale'},
  { 'app_id': 'com.hcg.cok.gp',
    'description': u'Clash of Kings - Build a Kingdom & fight in MMO combat to stand against the ages',
    'developer': 'Elex Wireless',
    'free': True,
    'icon': 'https://lh5.ggpht.com/wjNgsM2TGmbxbN-jDNAUNTIIq32OSx83Tx4Vl3jOudqzUEi1yTVCcMtnoGnZGGyXRA',
    'price': '0',
    'score': '4.2',
    'title': 'Clash of Kings',
    'url': 'https://play.google.com/store/apps/details?id=com.hcg.cok.gp'}, ...]
```

### Tests

Run tests:
```
python -m unittest discover
```
