# -*- coding: utf-8 -*-

BASE_URL = 'https://play.google.com/store/apps'
SUGGESTION_URL = 'https://market.android.com/suggest/SuggRequest'
SEARCH_URL = 'https://play.google.com/store/search'

CONCURRENT_REQUESTS = 10
USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/45.0.2454.101 Safari/537.36')

# Number of results to retrieve from a collection. Range(1 - 120)
NUM_RESULTS = 60

# Number of results to retrieve from a developer
DEV_RESULTS = 24

# Number of results to retrieve from similar. Range (1 - 60)
SIMILAR_RESULTS = 24

# pagTok post data strings to paginate through search results
PAGE_TOKENS = {
    0: '',
    1: 'GAEiAggU:S:ANO1ljLtUJw',
    2: 'GAEiAggo:S:ANO1ljIeRQQ',
    3: 'GAEiAgg8:S:ANO1ljIM1CI',
    4: 'GAEiAghQ:S:ANO1ljLxWBY',
    5: 'GAEiAghk:S:ANO1ljJkC4I',
    6: 'GAEiAgh4:S:ANO1ljJfGC4',
    7: 'GAEiAwiMAQ==:S:ANO1ljL7Yco',
    8: 'GAEiAwigAQ==:S:ANO1ljLMTko',
    9: 'GAEiAwi0AQ==:S:ANO1ljJ2maA',
    10: 'GAEiAwjIAQ==:S:ANO1ljIG2D4',
    11: 'GAEiAwjcAQ==:S:ANO1ljJ9Wk0',
    12: 'GAEiAwjwAQ==:S:ANO1ljLFcVI',
}

# Regex to find page tokens within scrip tags
TOKEN_RE = r'GAEiA[\w=]{3,7}:S:ANO1lj[\w]{5}'
