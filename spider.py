import urllib.request
from linkfinder import LinkFinder
from general import *


class Spider:

    # Class variables (shared among all the spiders)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()           # Declaring an empty set for the waiting list
    crawled = set()         # Declaring an empty set for the crawled list

    # Initializing the variables
    def __init__(self, project_name, base_url, domain_name):
        self.project_name = project_name
        self.base_url = base_url
        self.domain_name = domain_name
        self.queue_file = self.project_name + '/output.txt'
        self.crawled_file = self.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page(f'{self.project_name} Spider', self.base_url)

    # Method to boot up the spider
    def boot(self):
        create_project_dir(self.project_name)
        create_data_files(self.project_name, self.base_url)
        self.queue = file_to_set(self.queue_file)
        self.crawled = file_to_set(self.crawled_file)

    # Method to crawl through a web page, get all the links and update the files
    def crawl_page(self,thread_name, page_url):
        if page_url not in self.crawled:
            print('\n', thread_name, ' now crawling: ', page_url)
            print('\nRemaining links: ', str(len(self.queue)))
            print('\nCompleted: ', str(len(self.crawled)))
            self.add_links_to_queue(self.get_links(page_url))
            self.queue.remove(page_url)
            self.crawled.add(page_url)
            self.update_files()

    # Method to get all the links in a web page
    def get_links(self,page_url):
        html_string = ''
        try:
            # with a unlimited load page the timeout has been set to 60 second
            response = urllib.request.urlopen(page_url,timeout=60)
            html_bytes = response.read()
            html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(self.base_url, page_url)
            finder.find_links(html_string)
            return finder.page_links()
        except TimeoutError as exe:
            print(f'{page_url} was loading after the timeout')
        except Exception as exe:
            print('Error crawling the page')
            return set()

    # Method to add the gathered links to the waiting list (queue)
    def add_links_to_queue(self,links):
        for link in links:
            if link not in self.crawled and link not in self.queue and self.domain_name in link:
                self.queue.add(link)

    # Method to update both queue file and crawled file
    def update_files(self):
        set_to_file(self.queue, self.queue_file)
        set_to_file(self.crawled, self.crawled_file)
