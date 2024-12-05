import threading
from queue import Queue
from spider import Spider
from getdomain import *
from concurrent.futures import ThreadPoolExecutor



def extract_main_domain(url):
    parsed_url = urlparse(url)
    domain_parts = parsed_url.netloc.split('.')

    # Assuming the main domain is the second last part
    if len(domain_parts) > 2:
        main_domain = domain_parts[-2]
    else:
        main_domain = domain_parts[0]

    return main_domain

def starter(url):
    project_name = extract_main_domain(url)
    domain_name = get_domain_name(url)
    QUEUE_FILE = project_name + '/queue.txt'
    CRAWLED_FILE = project_name + '/crawled.txt'
    task_queue = Queue()
    spider_crawler = Spider(project_name, url, domain_name)

def crawl_webpages(urls,threads_count=None):
    with ThreadPoolExecutor(max_workers=threads_count) as executor:
        results = executor.map(starter, urls)
    return list(results)


urls = ['https://www.google.com/', 'https://www.arthtechglobal.com/']

THREAD_COUNT = 2
crawl_webpages(urls,THREAD_COUNT)
