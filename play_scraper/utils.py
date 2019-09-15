# -*- coding: utf-8 -*-

import logging
import re

try:
    from urllib import quote_plus
    from urlparse import urljoin, urlparse, parse_qs
except ImportError:
    from urllib.parse import quote_plus, urljoin, urlparse, parse_qs

import requests
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession

from play_scraper import settings as s

log = logging.getLogger(__name__)


def default_headers():
    return {
        "Origin": "https://play.google.com",
        "User-Agent": s.USER_AGENT,
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    }


def generate_post_data(results=None, page=None, pagtok=None, children=0):
    """
    Creates the post data for a POST request. Mainly for pagination and
    limiting results.

    :param results: the number of results to return.
    :param page: the page number; used to calculate start = page * results.
    :param pagtok: a page token string for pagination in search.
    :param children: number of apps under each collection (used only when
                     scraping a top-level category's collections).
    :return: a dictionary of post data.
    """
    data = {"ipf": 1, "xhr": 1}
    if children:
        data["numChildren"] = children
    if results is not None:
        if page is not None:
            start = 0 if page <= 0 else results * page
            data["start"] = start
        data["num"] = results
    if pagtok is not None:
        data["pagTok"] = pagtok
    return data


def build_url(method, id_string):
    """Creates the absolute url for a type of object. E.g. details, developer,
    or similar.

    :param method: the corresponding method to get for an id.
    :param id: an id string query parameter.
    :return: a URL string.
    """
    if method == "developer":
        id_string = quote_plus(id_string)

    url = "{base}/{method}?id={id}".format(base=s.BASE_URL, method=method, id=id_string)
    return url


def build_collection_url(category="", collection=""):
    """Creates the absolute url based on the category and collection ids.

    :param category: the category to filter by.
    :param collection: the collection to get.
    :return: a formatted url string.
    """
    if category:
        category = "/category/{cat}".format(cat=category)
    if collection:
        collection = "/collection/{col}".format(col=collection)

    url = "{base}{category}{collection}".format(
        base=s.BASE_URL, category=category, collection=collection
    )

    return url


def send_request(
    method,
    url,
    data=None,
    params=None,
    headers=None,
    timeout=30,
    verify=True,
    allow_redirects=False,
):
    """Sends a request to the url and returns the response.

    :param method: HTTP method to use.
    :param url: URL to send.
    :param data: Dictionary of post data to send.
    :param headers: Dictionary of headers to include.
    :param timeout: number of seconds before timing out the request
    :param verify: a bool for requesting SSL verification.
    :return: a Response object.
    """
    data = {} if data is None else data
    params = {} if params is None else params
    headers = default_headers() if headers is None else headers
    if not data and method == "POST":
        data = generate_post_data()

    try:
        response = requests.request(
            method=method,
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout,
            verify=verify,
            allow_redirects=allow_redirects,
        )
        if not response.status_code == requests.codes.ok:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        log.error(e)
        raise

    return response


def parse_additional_info(soup):
    """Parses an app's additional information section on its detail page.

    :param soup: the additional_info section BeautifulSoup object
    :return: a dictionary of the app's parsed additional info
    """
    # This is super ugly because the CSS is obfuscated and doesn't have good
    # distinguishing selectors available; each section's markup is nearly
    # identical, so we get the values with a similar function.
    section_titles_divs = [x for x in soup.select("div.hAyfc div.BgcNfc")]

    title_normalization = {
        "Updated": "updated",
        "Size": "size",
        "Installs": "installs",
        "Current Version": "current_version",
        "Requires Android": "required_android_version",
        "Content Rating": "content_rating",
        "In-app Products": "iap_range",
        "Interactive Elements": "interactive_elements",
        "Offered By": "developer",
        "Developer": "developer_info",
    }

    data = {
        "updated": None,
        "size": None,
        "installs": None,
        "current_version": None,
        "required_android_version": None,
        "content_rating": None,
        "iap_range": None,
        "interactive_elements": None,
        "developer": None,
        "developer_email": None,
        "developer_url": None,
        "developer_address": None,
    }

    for title_div in section_titles_divs:
        section_title = title_div.string
        if section_title in title_normalization:
            title_key = title_normalization[section_title]
            value_div = title_div.next_sibling.select_one("span.htlgb")

            if title_key == "content_rating":
                # last string in list is 'Learn more' link
                value = [rating.strip() for rating in value_div.strings][:-1]
            elif title_key == "interactive_elements":
                value = [ielement.strip() for ielement in value_div.strings]
            elif title_key == "iap_range":
                iaps = re.search(r"(\$\d+\.\d{2}) - (\$\d+\.\d{2})", value_div.string)
                if iaps:
                    value = iaps.groups()
            elif title_key == "developer_info":
                developer_email = value_div.select_one('a[href^="mailto:"]')
                if developer_email:
                    developer_email = developer_email.attrs["href"].split(":")[1]
                developer_url = value_div.select_one('a[href^="http"]')
                if developer_url:
                    developer_url = developer_url.attrs["href"]

                developer_address = value_div.select("div")[-1].contents[0]
                if developer_address.name is not None:
                    # If a bs4 Tag, it will have name attribute, e.g. 'a'
                    # Set the address to None for 'not found'
                    # The address div should just be a string, no name attr
                    developer_address = None
                if developer_address is not None:
                    developer_address = developer_address.strip()

                dev_data = {
                    "developer_email": developer_email,
                    "developer_url": developer_url,
                    "developer_address": developer_address,
                }
                data.update(dev_data)
                continue
            else:
                value = value_div.text

            data[title_key] = value
    return data


def parse_screenshot_src(img):
    """
    The screenshot img element's src isn't always present, and sometimes is set
    to a base64 encoded empty image because they're normally hidden in the
    scrollable carousel, for purposes of saving bandwidth and faster loading.

    Instead, it seems like we can grab the src url from data-src in those cases.

    :param img: the img bs4 element
    :return: the src url string
    """
    src = img.attrs.get("src")
    if src is None or not src.startswith("https://"):
        src = img.attrs.get("data-src")
    return src


def parse_app_details(soup):
    """Extracts an app's details from its info page.

    :param soup: a strained BeautifulSoup object of an app
    :return: a dictionary of app details
    """
    title = soup.select_one('h1[itemprop="name"] span').text
    icon = soup.select_one('img[class="T75of sHb2Xb"]').attrs["src"].split("=")[0]
    editors_choice = bool(soup.select_one('meta[itemprop="editorsChoiceBadgeUrl"]'))

    # Main category will be first
    category = [
        c.attrs["href"].split("/")[-1] for c in soup.select('a[itemprop="genre"]')
    ]

    # Let the user handle modifying the URL to fetch different resolutions
    # Removing the end `=w720-h310-rw` doesn't seem to give original res?
    # Check 'src' and 'data-src' since it can be one or the other
    screenshots = [
        parse_screenshot_src(img) for img in soup.select("button.Q4vdJd img.DYfLw")
    ]

    try:
        video = soup.select_one('button[data-trailer-url^="https"]').attrs.get(
            "data-trailer-url"
        )
        if video is not None:
            video = video.split("?")[0]
    except AttributeError:
        video = None

    description_soup = soup.select_one('div[itemprop="description"] span div')
    if description_soup:
        description = "\n".join(description_soup.stripped_strings)
        description_html = description_soup.encode_contents()
    else:
        description = description_html = None

    # Reviews & Ratings
    try:
        score = soup.select_one("div.BHMmbe").text
    except AttributeError:
        score = None

    histogram = {}
    try:
        reviews = int(
            soup.select_one('span[aria-label$="ratings"]').text.replace(",", "")
        )
        ratings_section = soup.select_one("div.VEF2C")
        num_ratings = [
            int(rating.attrs["title"].replace(",", ""))
            if rating.attrs.get("title")
            else None
            for rating in ratings_section.select('div span[style^="width:"]')
        ]
        for i in range(5):
            histogram[5 - i] = num_ratings[i]
    except AttributeError:
        reviews = 0

    try:

        changes_soup = soup.select('div[itemprop="description"] content')[1]
        recent_changes = "\n".join(
            [x.string.strip() if x.string is not None else "" for x in changes_soup]
        )
    except (IndexError, AttributeError):
        recent_changes = None

    try:
        price = soup.select_one('meta[itemprop="price"]').attrs["content"]
    except AttributeError:
        # App is probably pre-register, requires logged in to see
        try:
            price = soup.select_one("not-preregistered").string.strip()
        except AttributeError:
            price = None

    free = price == "0"

    additional_info_data = parse_additional_info(soup.select_one(".IxB2fe"))

    offers_iap = bool(additional_info_data.get("iap_range"))

    try:
        dev_id = soup.select_one("a.hrTbp.R8zArc").attrs["href"].split("=")[1]
    except IndexError:
        dev_id = None
    developer_id = dev_id if dev_id else None

    data = {
        "title": title,
        "icon": icon,
        "screenshots": screenshots,
        "video": video,
        "category": category,
        "score": score,
        "histogram": histogram,
        "reviews": reviews,
        "description": description,
        "description_html": description_html,
        "recent_changes": recent_changes,
        "editors_choice": editors_choice,
        "price": price,
        "free": free,
        "iap": offers_iap,
        "developer_id": developer_id,
    }

    data.update(additional_info_data)

    return data


def extract_id_query(url):
    """
    Parses a url and extracts the id query parameter value.

    :param url: either the relative or absolute url string containing an app id
    :return: the app id
    """
    if not url:
        return None

    absolute_url = url
    if not absolute_url.startswith("https"):
        absolute_url = urljoin(s.BASE_URL, url)

    query_string = urlparse(absolute_url).query
    app_id = parse_qs(query_string).get("id")[0]
    return app_id


def parse_cluster_card_info(soup):
    """
    App lists from GET requests follow a redirect to the /cluster page, which
    contains different HTML and selectors.

    :param soup: a BeautifulSoup object of an app's card
    :return: a dictionary of available basic app info
    """
    icon = soup.select_one("img")

    details_soup = soup.select_one("div.RZEgze")
    relative_url = details_soup.select_one("div.p63iDd > a")
    url = relative_url.attrs.get("href") if relative_url else None

    app_id = None
    if url:
        app_id = extract_id_query(url)

    title = details_soup.select_one("div.WsMG1c.nnK0zc")

    developer_soup = details_soup.select_one("a.mnKHRc")
    developer = None
    developer_id = None
    if developer_soup:
        developer = developer_soup.select_one("div.KoLSrc")
        developer_url = developer_soup.attrs.get("href") if developer else None
        developer_id = extract_id_query(developer_url)

    description = details_soup.select_one("div.b8cIId.f5NCO")

    score_soup = details_soup.select_one("div.pf5lIe div")
    score = None
    if score_soup:
        matches = re.search(r"([0-9]\.[0-9]) star", score_soup.text)
        score = matches.groups()[0] if matches else None

    price = None
    price_button = details_soup.select_one("button span.VfPpfd")
    if price_button:
        price = price_button.text

    full_price = None
    full_price_button = details_soup.select_one("button span.SUZt4c")
    if full_price_button:
        full_price = full_price_button.text

    free = price is None
    if free is True:
        price = "0"
        full_price = "0"

    return {
        "app_id": app_id,
        "url": url,
        "icon": icon.attrs.get("data-src") if icon else None,
        "title": title.text if title else None,
        "developer": developer.text if developer else None,
        "developer_id": developer_id,
        "description": description.text if description else None,
        "score": score,
        "full_price": full_price,
        "price": price,
        "free": free,
    }


def parse_card_info(soup):
    """Extracts basic app info from the app's card. Used when parsing pages
    with lists of apps.

    :param soup: a BeautifulSoup object of an app's card
    :return: a dictionary of available basic app info
    """
    app_id = soup.attrs["data-docid"]
    url = urljoin(s.BASE_URL, soup.select_one("a.card-click-target").attrs["href"])
    icon = urljoin(
        s.BASE_URL, soup.select_one("img.cover-image").attrs["src"].split("=")[0]
    )
    title = soup.select_one("a.title").attrs["title"]

    dev_soup = soup.select_one("a.subtitle")
    developer = dev_soup.attrs["title"]
    try:
        developer_id = dev_soup.attrs["href"].split("=")[1]
    except IndexError:
        developer_id = None

    description = soup.select_one("div.description").text.strip()
    score = soup.select_one("div.tiny-star")
    if score is not None:
        score = score.attrs["aria-label"].strip().split(" ")[1]

    try:
        price = soup.select_one("span.display-price").text
    except AttributeError:
        try:
            # Pre-register apps are 'Coming Soon'
            price = soup.select_one("a.price").text
        except AttributeError:
            # Country restricted, no price or buttons shown
            price = None

    full_price = None
    if price is not None:
        try:
            full_price = soup.select_one("span.full-price").text
        except AttributeError:
            full_price = None

    free = price is None
    if free is True:
        price = "0"

    return {
        "app_id": app_id,
        "url": url,
        "icon": icon,
        "title": title,
        "developer": developer,
        "developer_id": developer_id,
        "description": description,
        "score": score,
        "full_price": full_price,
        "price": price,
        "free": free,
    }


def parse_app_details_response_hook(response, *args, **kwargs):
    """
    Requests futures hook function to asynchronously parse app details as the
    responses are received. Mimics the `details` api.
    """
    if not response.status_code == requests.codes.ok:
        response.raise_for_status()
    soup = BeautifulSoup(response.content, "lxml", from_encoding="utf8")
    details = parse_app_details(soup)
    response.app_details_data = details


def multi_futures_app_request(
    app_ids, headers=None, verify=True, params=None, workers=s.CONCURRENT_REQUESTS
):
    """
    :param app_ids: a list of app IDs.
    :param headers: a dictionary of custom headers to use.
    :param verify: bool for requesting SSL verification.
    :return: a list of all apps' detail data
    """
    session = FuturesSession(max_workers=workers)

    headers = default_headers() if headers is None else headers
    responses = [
        session.get(
            build_url("details", app_id),
            headers=headers,
            verify=verify,
            params=params,
            hooks={"response": parse_app_details_response_hook},
        )
        for app_id in app_ids
    ]

    apps = []
    for i, response in enumerate(responses):
        try:
            result = response.result()
            app_json = result.app_details_data
            app_json.update({"app_id": app_ids[i], "url": result.url})
            apps.append(response.result().app_details_data)
        except requests.exceptions.RequestException as e:
            log.error(
                "Error occurred fetching {app}: {err}".format(
                    app=app_ids[i], err=str(e)
                )
            )

    return apps
