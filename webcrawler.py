# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

url = 'http://www.thm-troisdorf.de/'

class WebCrawler():

    _base_url = ''
    _site_map = {}
    _links = set()

    def __init__(self, url):
        self._base_url = str(url).rstrip('/')

    def _get_links(self, url):

        links = []
        req = requests.get(self._base_url + url)
        if req.status_code != 200:
            return

        soup = BeautifulSoup(req.text, "html.parser")
        for item in soup.find_all('a'):
            href = str(item.get('href'))
            if href and href.startswith('/'):
                links.append(href)
        return links

    def _crawl_url(self, urls):
        for url in urls:
            if url not in self._links:
                self._links.add(url)
                links = self._get_links(url)
                self._crawl_url(links)

    def parse(self):
        self._site_map = self._crawl_url(['/'])
        for link in self._links:
            print link


wc = WebCrawler(url)
wc.parse()