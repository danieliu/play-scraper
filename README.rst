Play Store Scraper
==================

Scrapes and parses application data from the Google Play Store.

Installation
------------

Either install requirements in a virtualenv or run the setup.

::

    pip install -r requirements.txt
    python setup.py install

Usage
-----

-  `details <#details>`__: Fetch an application's details
-  `collection <#collection>`__: Fetch a list of applications and their
   details.
-  `developer <#developer>`__: Fetch a developer's offered applications.
-  `suggestions <#suggestions>`__: Fetch a list of query string
   suggestions.
-  `search <#search>`__: Fetch applications matching a search query.
-  `similar <#similar>`__: Fetch an application's similar apps.

details
~~~~~~~

Fetch an application's details.

Options:

-  ``app_id`` the app id to get, e.g. ``com.android.chrome`` for Google
   Chrome.

.. code:: python

    >>> import play_scraper
    >>> print play_scraper.details('com.android.chrome')
    { 
        'app_id': 'com.android.chrome',
        'category': ['COMMUNICATION'],
        'content_rating': u'Everyone',
        'current_version': u'Varies with device',
        'description': u'Browse fast on your Android phone and tablet with the Google Chrome browser you love on desktop. Pick up where ...',
        'description_html': u'Browse fast on your Android phone and tablet with the Google Chrome browser you love on desktop. Pick up where you left off on your other devices with tab sync, search by voice, and save up to 50% of data usage while browsing. <br/>',
        'developer': u'Google Inc.',
        'developer_address': u'1600 Amphitheatre Parkway, Mountain View 94043',
        'developer_email': 'apps-help@google.com',
        'developer_id': '5700313618786177705',
        'developer_url': 'http://www.google.com/chrome/android',
        'editors_choice': False,
        'free': True,
        'histogram': { 1: 353226, 2: 159357, 3: 328319, 4: 738938, 5: 2691357},
        'iap': False,
        'iap_range': None,
        'icon': 'https://lh3.ggpht.com/O0aW5qsyCkR2i7Bu-jUU1b5BWA_NygJ6ui4MgaAvL7gfqvVWqkOBscDaq4pn-vkwByUx',
        'installs': [1000000000, 5000000000],
        'interactive_elements': [u'Unrestricted Internet'],
        'price': '0',
        'recent_changes': u'Bug fixes and speedy performance improvements.',
        'required_android_version': u'Varies with device',
        'reviews': 4271197,
        'score': 4.230531692504883,
        'screenshots': [ 'https://lh4.ggpht.com/6D21o4j_OJUnVCTARqcdajTmX_5_8UJtzVuN91smALZBuMq0p3MIvwZj2qofXeqmFIU=h900-rw', ...],
        'size': u'Varies with device',
        'thumbnails': [ 'https://lh4.ggpht.com/6D21o4j_OJUnVCTARqcdajTmX_5_8UJtzVuN91smALZBuMq0p3MIvwZj2qofXeqmFIU=h310-rw', ...],
        'title': u'Chrome Browser - Google',
        'top_developer': True,
        'updated': u'March 25, 2016',
        'url': 'https://play.google.com/store/apps/details?id=com.android.chrome',
        'video': None
    }

collection
~~~~~~~~~~

Fetch a list of applications from a collection, optionally filtered by
category.

Options:

-  ``collection`` a
   `collection <https://github.com/danieliu/play-scraper/blob/master/play_scraper/lists.py#L3>`__
   to fetch.
-  ``category`` (default None) a
   `category <https://github.com/danieliu/play-scraper/blob/master/play_scraper/lists.py#L12>`__
   to filter by.
-  ``results`` (default 60, max 120) the number of apps to fetch.
-  ``page`` (default 0) the page number to fetch. Limit:
   ``page * results <= 500``.
-  ``age`` (default None) an `age
   range <https://github.com/danieliu/play-scraper/blob/master/play_scraper/lists.py#L67>`__
   to filter by. (Only for FAMILY categories)
-  ``detailed`` (default False) if True, sends a request per app to
   fetch the full `details <#details>`__.

.. code:: python

    >>> import play_scraper
    >>> print play_scraper.collection(
            collection='TRENDING',
            category='GAME_RACING',
            results=5,
            page=1)
    [ { 'app_id': 'com.gigabitgames.offroad',
        'description': u'The most realistic off-road game on Android. Its your world, you conquer it.',
        'developer': 'Gigabit Games',
        'developer_id': '9169751687364421253',
        'free': True,
        'icon': 'https://lh3.googleusercontent.com/73m8eqn_YUzbTMV986wG2C_zd8_PNSR0GBxf_d6GKbBLa0gUA8OYy0dOP9PCKFYMyX0',
        'price': '0',
        'score': '4.2',
        'title': 'Gigabit Off-Road',
        'url': 'https://play.google.com/store/apps/details?id=com.gigabitgames.offroad'},
      { 'app_id': 'com.sbkgames.rallyracerdirt',
        'description': u'Drift like a pro, race in dirt, hill climb, asphalt drift, be a rally racer.',
        'developer': 'sbkgames',
        'developer_id': None,
        'free': True,
        'icon': 'https://lh3.googleusercontent.com/BiONHFMzbVA32q5bvo9L1YHD4Ss02VSF5IZxCqWgdULZp2rKmeaMpBWRwMd2XlvxLw',
        'price': '0',
        'score': '4.2',
        'title': 'Rally Racer Dirt',
        'url': 'https://play.google.com/store/apps/details?id=com.sbkgames.rallyracerdirt'}, ...]

developer
~~~~~~~~~

Fetch a developer's offered applications.

Options:

-  ``developer`` the developer name to fetch applications, e.g.
   ``Disney``. (Case sensitive)
-  ``results`` (default 24, max 120) the number of apps to fetch.
   (Developer may have more or less published apps)
-  ``page`` (default 0) the page number to fetch. Limit:
   ``0 < (results // 20) * page < 12``
-  ``detailed`` (default False) if True, sends a request per app to
   fetch the full details as in `details <#details>`__.

.. code:: python

    >>> import play_scraper
    >>> print play_scraper.developer('Disney', results=5)
    [ { 'app_id': 'com.disney.disneycrossyroad_goo',
        'description': u'An all-new take on the ultimate 8-bit endless adventure to cross the road!',
        'developer': 'Disney',
        'developer_id': None,
        'free': True,
        'icon': 'https://lh3.googleusercontent.com/mHHQ-GA_hu8shAEtzj8trGBOJK7dtMrmV4XXvjl49MQbIDHytb8kQenB4IaUB9NvYA',
        'price': '0',
        'score': '4.5',
        'title': 'Disney Crossy Road',
        'url': 'https://play.google.com/store/apps/details?id=com.disney.disneycrossyroad_goo'},
      { 'app_id': 'com.disney.disneymoviesanywhere_goo',
        'description': u'Watch Disney, Disney/Pixar, Marvel & Star Wars movies w/ Disney Movies Anywhere.',
        'developer': 'Disney',
        'developer_id': None,
        'free': True,
        'icon': 'https://lh3.googleusercontent.com/J75JRuJvlOQ9K5H7RpSyGu1q909Qy6GJs9RW51KlE2CvyfPX14SGG-HRGnsfDfIETfg',
        'price': '0',
        'score': '3.9',
        'title': 'Disney Movies Anywhere',
        'url': 'https://play.google.com/store/apps/details?id=com.disney.disneymoviesanywhere_goo'}, ...]

suggestions
~~~~~~~~~~~

Fetch a list of autocompleted query suggestions.

.. code:: python

    >>> import play_scraper
    >>> print play_scraper.suggestions('cat')
    [u'cat games', u'cat simulator', u'cat sounds', u'cat games for cats']

search
~~~~~~

Fetch a list of applications matching a search query. Retrieves ``20``
apps at a time.

Options:

-  ``query`` query term(s) to search for.
-  ``page`` (default 0, max 12) page number of results to retrieve.
-  ``detailed`` (default False) if True, sends a request per app to
   fetch the full details as in `details <#details>`__.

.. code:: python

    >>> import play_scraper
    >>> print play_scraper.search('dogs', page=2)
    [ { 'app_id': 'jp.pascal.mydogmyroomfree',
        'description': u'Take a picture of the room as you like, and keep a cute puppy in your own room!!',
        'developer': 'pascal inc.',
        'developer_id': None,
        'free': True,
        'icon': 'https://lh5.ggpht.com/WlGXYIHU0cljFIaNBloRHtznuBo3pAt4B1ynnfiXPTsjoqKDfX5Rxo9U15iDZXuRZe32',
        'price': '0',
        'score': '3.7',
        'title': 'My Dog My Room Free',
        'url': 'https://play.google.com/store/apps/details?id=jp.pascal.mydogmyroomfree'},
      { 'app_id': 'com.sweefitstudios.drawdogs',
        'description': u'An app that teaches you how to draw dogs step by step',
        'developer': 'Sweefit Studios',
        'developer_id': '8890723712967774017',
        'free': True,
        'icon': 'https://lh3.googleusercontent.com/qt6hpHGwu6-viUAKkw9nv3iH_IQYMvBfHwc1X-TbcjOOgbqH67K6SJITi64FzBhQRKk',
        'price': '0',
        'score': '4.3',
        'title': 'How to Draw Dogs',
        'url': 'https://play.google.com/store/apps/details?id=com.sweefitstudios.drawdogs'}, ...]

similar
~~~~~~~

Fetch a list of similar applications.

Options:

-  ``app_id`` the app id to get, e.g. ``com.supercell.clashofclans`` for
   Clash of Clans.
-  ``results`` (default 24, max 60) the number of apps to fetch.
-  ``detailed`` (default False) if True, sends a request per app to
   fetch the full details as in `details <#details>`__.

.. code:: python

    >>> import play_scraper
    >>> print play_scraper.similar('com.supercell.clashofclans', results=5)
    [ { 'app_id': 'com.supercell.clashroyale',
        'description': u'Clash Royale is a real-time, head-to-head battle game set in the Clash Universe.',
        'developer': 'Supercell',
        'developer_id': '6715068722362591614',
        'free': True,
        'icon': 'https://lh3.googleusercontent.com/K-MNjDiO2WwRNwJqPZu8Wd5eOmFEjLYkEEgjZlv35hTiua_VylRPb04Lig3YZXLERvI',
        'price': '0',
        'score': '4.5',
        'title': 'Clash Royale',
        'url': 'https://play.google.com/store/apps/details?id=com.supercell.clashroyale'},
      { 'app_id': 'com.hcg.cok.gp',
        'description': u'Clash of Kings - Build a Kingdom & fight in MMO combat to stand against the ages',
        'developer': 'Elex Wireless',
        'developer_id': None,
        'free': True,
        'icon': 'https://lh5.ggpht.com/wjNgsM2TGmbxbN-jDNAUNTIIq32OSx83Tx4Vl3jOudqzUEi1yTVCcMtnoGnZGGyXRA',
        'price': '0',
        'score': '4.2',
        'title': 'Clash of Kings',
        'url': 'https://play.google.com/store/apps/details?id=com.hcg.cok.gp'}, ...]

Tests
-----

Run tests:

::

    python -m unittest discover