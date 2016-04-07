# -*- coding: utf-8 -*-

import requests
import settings
from urlparse import urljoin

from bs4 import BeautifulSoup

from logger import configure_logging


class PlayScraper(object):
	def __init__(self):
		self._base_url = settings.BASE_URL
		self._verify = settings.VERIFY_SSL
		self._headers = settings.HEADERS
		self._num_results = settings.NUM_RESULTS
		self._num_collections = settings.NUM_COLLECTIONS
		self._base_collections = settings.BASE_COLLECTIONS.values()
		self._logger = configure_logging()

	def _build_app_url(self, app_id=None):
		"""
		Create the app's absolute url by id
		"""
		if not app_id:
			raise ValueError("No App ID provided.")
		return "{base}/details?id={app_id}".format(
			base=self._base_url,
			app_id=app_id)

	def _build_list_url(self, category="", collection=""):
		"""
		Creates the absolute url based on the category and collection id's.
		"""
		if category:
			category = "/category/{cat_id}".format(cat_id=category)
		if collection:
			collection = "/collection/{col_name}".format(col_name=collection)
		return "{base}{category}{collection}".format(
			base=self._base_url,
			category=category,
			collection=collection)

	def _get_category_list(self):
		"""
		GET the main store and create a list of all available app
		categories and their respective relative URLs.
		"""
		data = {}
		home_page = self._build_list_url()
		soup = self._get_soup(home_page)
		categories = soup.select('a.child-submenu-link')
		for cat in categories:
			url = cat.attrs['href']
			data[cat.string] = {
				'name': cat.string,
				'url': url,
				'category_id': url.split('/')[-1]}
		return data

	def _get_soup(self, url, data={}, method='POST'):
		"""
		Sends a request to URL and turns the response into a soup object.
		"""
		if not data and method == 'POST':
			data = self._generate_post_data()
		try:
			self._logger.info("Sending {method} to '{url}'.".format(
				method=method, url=url))
			response = requests.request(
				method=method,
				url=url,
				data=data,
				headers=self._headers,
				verify=self._verify)
			if response.status_code == requests.codes.ok:
				soup = BeautifulSoup(response.content, 'lxml')
				return soup
			else:
				response.raise_for_status()
		except requests.exceptions.RequestException as e:
			self._logger.error("{e} at {url}".format(e=e, url=url))
			raise

	def _generate_post_data(self, results=None, page=None, children=0):
		"""
		Creates the post data for a POST request, mainly for pagination
		and limiting results.
		"""
		data = {
			'ipf': 1,
			'xhr': 1
		}
		if children:
			data['numChildren'] = children
		if results is not None and page is not None:
			start = 0 if page <= 0 else results * page
			data['start'] = start
			data['num'] = results
		return data

	def _get_collections(self, soup):
		"""
		Parse collection titles, ids, and URLs from the top-level category and
		return them in a list.
		"""
		collections = []
		links = soup.select('a.see-more')
		for a in links:
			name = a.parent.previous_sibling.previous_sibling.string
			url = a.attrs['href']
			collection = url.split('/')[-1]
			if collection not in self._base_collections:
				collections.append({
					'name': name,
					'url': url,
					'collection': collection
				})
		return collections

	def parse_app(self, app_id):
		"""
		Gets an app's details.
		"""
		url = self._build_app_url(app_id)
		soup = self._get_soup(url, method="GET")

		title = soup.select_one('div.id-app-title').string
		icon = urljoin(self._base_url, soup.select_one('img.cover-image').attrs['src'])
		screenshots = [
			urljoin(self._base_url, s.attrs['src']) for s in soup.select('img.full-screenshot')]
		thumbnails = [
			urljoin(self._base_url, s.attrs['src']) for s in soup.select('img.screenshot')]

		try:
			video = soup.select_one('span.preview-overlay-container').attrs.get('data-video-url', None)
			if video:
				video = video.split('?')[0]
		except AttributeError:
			video = None

		category = [{
			'category_id': c.attrs['href'].split('/')[-1],
			'category': c.span.string} for c in soup.select('.category')]

		description_soup = soup.select_one('.show-more-content.text-body div')
		description = "\n".join([x.replace(u"’", u"'").encode('utf-8') for x in description_soup.stripped_strings])
		description_html = "".join([str(x.encode('utf-8')).replace("’", "'") for x in description_soup.contents])

		# Reviews & Ratings
		try:
			score = float(soup.select_one('meta[itemprop="ratingValue"]').attrs['content'])
		except AttributeError:
			score = None
			pass

		histogram = {}
		try:
			reviews = int(soup.select_one('meta[itemprop="ratingCount"]').attrs['content'])
			ratings = [int(r.string.replace(',', '')) for r in soup.select('span.bar-number')]
			for i in range(5):
				histogram[5 - i] = ratings[i]
		except AttributeError:
			reviews = None
			pass

		recent_changes = "\n".join([x.string.strip() for x in soup.select('.recent-change')])
		top_developer = bool(soup.select_one('meta[itemprop="topDeveloperBadgeUrl"]'))
		price = soup.select_one('meta[itemprop="price"]').attrs['content']
		free = (price == '0')

		# Additional information section
		additional_info = soup.select_one('.metadata .details-section-contents')
		updated = additional_info.select_one('div[itemprop="datePublished"]').string
		size = additional_info.select_one('div[itemprop="fileSize"]')
		if size:
			size = size.string.strip()

		installs = [int(n.replace(',', '')) for n in additional_info.select_one(
			'div[itemprop="numDownloads"]').string.strip().split(" - ")]

		current_version = additional_info.select_one('div[itemprop="softwareVersion"]')
		if current_version:
			current_version = current_version.string.strip()

		required_android_version = additional_info.select_one('div[itemprop="operatingSystems"]').string.strip()
		content_rating = additional_info.select_one('div[itemprop="contentRating"]').string

		meta_info = additional_info.select('.title')
		meta_info_titles = [x.string.strip() for x in meta_info]
		try:
			i_elements_index = meta_info_titles.index('Interactive Elements')
			interactive_elements = meta_info[i_elements_index].next_sibling.next_sibling.string.split(', ')
		except ValueError:
			interactive_elements = []
			pass

		offers_iap = bool(soup.select_one('.inapp-msg'))
		in_app_purchases = None
		if offers_iap:
			try:
				iap_price_index = meta_info_titles.index('In-app Products')
				in_app_purchases = meta_info[iap_price_index].string
			except ValueError:
				self._logger.warning(
					"Could not find In-app Products price range for '{app}'".format(
						app=app_id))
				pass

		developer = soup.select_one('span[itemprop="name"]').string
		developer_email = additional_info.select_one('a[href^="mailto"]').attrs['href'].split(":")[1]
		developer_url = additional_info.select_one('a[href^="https://www.google.com"]')
		if developer_url:
			developer_url = developer_url.attrs['href'].split("&")[0].split("=")[1]
		developer_address = additional_info.select_one('.physical-address')
		if developer_address:
			developer_address = developer_address.string

		self._logger.info("Parsed app '{app}' details".format(app=title.encode('utf-8')))

		return {
			'app_id': app_id,
			'title': title,
			'icon': icon,
			'url': url,
			'screenshots': screenshots,
			'thumbnails': thumbnails,
			'video': video,
			'category': category,
			'score': score,
			'histogram': histogram,
			'reviews': reviews,
			'description': description,
			'description_html': description_html,
			'recent_changes': recent_changes,
			'top_developer': top_developer,
			'price': price,
			'free': free,
			'updated': updated,
			'size': size,
			'installs': installs,
			'current_version': current_version,
			'required_android_version': required_android_version,
			'content_rating': content_rating,
			'interactive_elements': interactive_elements,
			'offers_iap': offers_iap,
			'in_app_purchases': in_app_purchases,
			'developer': developer,
			'developer_email': developer_email,
			'developer_url': developer_url,
			'developer_address': developer_address
		}

	def parse_collection(self, **kwargs):
		"""
		Crawls through a collection, paginating as necessary and returns parsed
		apps in a list.
		"""
		col = kwargs.pop('collection', None)
		if not col:
			raise ValueError("No collection specified.")

		cat = kwargs.pop('category', '')
		page = 0
		apps = []
		url = self._build_list_url(cat['category_id'], col)

		while True:
			self._logger.info("Retrieving page {page} of {col}".format(
				page=page, col=col))

			post_data = self._generate_post_data(self._num_results, page)
			soup = self._get_soup(url, post_data)
			current_apps = [x.attrs['data-docid'] for x in soup.select('.card-content')]

			for app_id in current_apps:
				apps.append(self.parse_app(app_id))

			if len(current_apps) < self._num_results:
				break

			page += 1

		self._logger.info("Parsed {num} apps from {cat}'s {col}".format(
			num=len(apps), cat=cat['name'], col=col))

		return apps

	def parse_category(self, **kwargs):
		"""
		Main scraping function.

		Sends a POST request to a category's url, paginates and retrieves all
		collection urls.
		Crawls each collection to scrape app urls and IDs.
		Parse each app's details.
		"""
		category = kwargs.pop('category', settings.CATEGORIES[0])
		category_url = self._build_list_url(category['category_id'])

		results = settings.NUM_COLLECTIONS
		page = 0
		children = 1
		collections = []

		while True:
			post_data = self._generate_post_data(results, page, children)
			soup = self._get_soup(category_url, post_data)
			current = self._get_collections(soup)
			collections += current

			# 4/5/2016 Note: Play Store adds an ad now so may be one less
			# collection end loop when less than expected number of results, i.e.
			# reached max available collections
			if len(current) < (results - 1):
				break

			page += 1

		apps = []
		for c in collections:
			apps += self.parse_collection(c)

		return apps
