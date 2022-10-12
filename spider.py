#from urllib.request import urlopen
import requests
from link_finder import LinkFinder
from general import *

class Spider:

    # Class variables (shared among all instances)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    paths_file = ''
    page_status_file = ''
    queue = set()
    crawled = set()
    paths = set()
    page_status = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.paths_file = Spider.project_name + '/paths.csv'
        Spider.page_status_file = Spider.project_name + '/page-status.csv'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queued: ' + str(len(Spider.queue)) + ' | Crawled: ' + str(len(Spider.crawled)))
            Spider.process_links(page_url, Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()
            Spider.paths = set()
            Spider.page_status = set()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            requests.Session().post(page_url)
            response = requests.Session().get(page_url)
            page_status = page_url + ',' + str(response.status_code)
            Spider.page_status.add(page_status)
            if response.headers['Content-Type'][:9] == 'text/html':
                html_string = response.text
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as inst:
            print('Error: cannot crawl page')
            print(inst)
            return set()
        return finder.page_links()

    @staticmethod
    def process_links(page_url, links):
        for link in links:
            path = page_url + ',' + link
            Spider.paths.add(path)
            if link in Spider.queue:
                continue
            if link in Spider.crawled:
                continue
            if '#' in link:
                continue
            if link[:6] =='mailto':
                continue
            if Spider.domain_name not in link:
                continue
            Spider.queue.add(link)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
        set_to_csv(Spider.paths, Spider.paths_file)
        set_to_csv(Spider.page_status, Spider.page_status_file)



