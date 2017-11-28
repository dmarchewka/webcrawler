# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

url = 'https://www.xml-sitemaps.com'

class WebCrawler():

    _base_url = ''
    _site_map = ''
    _links = set()

    def __init__(self, url):
        self._base_url = url
        if not str(self._base_url).endswith('/'):
            self._base_url += '/'

    def _get_links(self, url):

        links = []
        req = requests.get(self._base_url + url)
        if req.status_code != 200:
            return

        soup = BeautifulSoup(req.text, "html.parser")
        for item in soup.find_all('a'):
            href = str(item.get('href')).replace(self._base_url, '')
            if href and not href.startswith('http') and href.find('java') == -1:
                links.append(href)
        return links

    def _search_site_map(self, urls):
        for url in urls:
            if url not in self._links:
                self._links.add(url)
                links = self._get_links(url)
                for link in links:
                    if 'sitemap.xml' in link:
                        self._site_map = self._base_url +  link
                        return
                self._search_site_map(links)

    def get_site_map(self):
        self._search_site_map(['/'])
        if self._site_map:
            req = requests.get(self._site_map)

            if req.status_code != 200:
                print 'Site map cannot be found %s' % req.status_code
                return

            print req.text

wc = WebCrawler(url)
wc.get_site_map()