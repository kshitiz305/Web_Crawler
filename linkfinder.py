from bs4 import BeautifulSoup
from urllib.parse import urljoin

class LinkFinder:

    def __init__(self, base_url, page_url):
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def find_links(self, string):
        page = BeautifulSoup(string, "lxml")
        for link in page.find_all('a'):
            url = urljoin(self.base_url, link.get('href'))
            self.links.add(url)

    def page_links(self):
        return self.links

