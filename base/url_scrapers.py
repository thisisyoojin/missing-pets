import os
import time
from scraper import Scraper

class UrlScraper(Scraper):
    """
    Base url scraper
    
    Init params
    ROOT_DOMAIN
    fpaths(Required) -> dict: dictionary including keys with prev, cur. Values are file paths.

    Method
    read_urls(fpath): read urls from file
    extract_new_urls(prev_fpath, cur_fpath): compare between database and current crawled urls. get only new urls to pass to page_scrapers.
    """

    def __init__(self, ROOT_DOMAIN, fpaths, option=None):
        super().__init__(ROOT_DOMAIN, option)
        fpaths['prev'], fpaths['cur'] = self.prev_fpath, self.cur_fpath

    
    def read_urls(self, fpath):
        if os.path.isfile(fpath):
            with open(fpath, 'r') as f:
                urls = f.readlines()
        else:
            urls = []
        return urls


    def write_urls(self, data, fpath):
        with open(fpath, type) as f:
            f.write(data)
        time.sleep(2)


    def extract_new_urls(self):
        set_prev = set(self.read_urls(self.prev_fpath))
        set_cur = set(self.read_urls(self.cur_fpath))
        os.rename(self.cur_fpath, self.prev_fpath)
        return set_cur.difference(set_prev)



class UrlScraperWithNext(UrlScraper):
    """
    Url Scraper With Next

    Init params
    ROOT_DOMAIN(string):
    option(Firefox selenium option):
    next_xpath(string):
    items_xpath(string):
    anchor_xpath(string):
    """

    def __init__(self, ROOT_DOMAIN, option=None, next_xpath='', items_xpath='', anchor_xpath=''):
        super().__init__(ROOT_DOMAIN, option)
        self.urls = []
        self.next_xpath = next_xpath
        self.items_xpath = items_xpath
        self.anchor_xpath = anchor_xpath


    def get_urls_in_current_page(self):
        urls = []
        items = self.driver.find_elements_by_xpath(self.items_xpath)
        for itm in items:
            url = itm.find_element_by_xpath(self.anchor_xpath).get_attribute('href')
            urls.append(url)
        return urls

    
    def get_next(self, cur_page):
        try:
            next_page = self.driver.find_element_by_xpath(self.next_xpath).get_attribute('href')
            while cur_page == next_page:
                time.sleep(2)
                next_page = self.driver.find_element_by_xpath(self.next_xpath).get_attribute('href')
            return next_page
        except:
            print('There is no next page.')
            return None


    def get_all_urls(self):
        
        self.start()
        current_page = self.ROOT_DOMAIN

        next = True
        
        while next:
            self.get_page_by_url(current_page)
            cur_urls = self.get_urls_in_current_page()
            self.urls.extend(cur_urls)
            
            next = self.get_next_page(current_page)
            current_page = next
            self.write_urls('\n'+'\n'.join(cur_urls), self.cur_fpath)

        self.close()
        print('Finished getting urls.')



class UrlScraperWithScroll(UrlScraper):
    """
    Scraping all urls through all pages
    """

    def __init__(self, ROOT_DOMAIN, item_xpath='', xpath_from_last_id=''):
        super().__init__(ROOT_DOMAIN)
        self.item_xpath = item_xpath
        self.xpath_from_last_id = xpath_from_last_id

    
    def find_next_items(self, item_xpath, xpath_from_last_id, last_id):
        """
        should return xpath
        """
        if last_id:
            # e.g.f"//div[@id='{last_id}']//following-sibling::div[contains(@id, 'gi-')]"
            xpath = xpath_from_last_id
        else:
            # e.g. "//div[contains(@id, 'gi-')]"
            xpath = item_xpath
        
        return self.driver.find_elements_by_xpath(xpath)
    


    def get_urls_from_items(self, last_id):

        items = self.find_next_items(last_id)
        item_id = None
        urls = []

        for item in items:
            item_id = item.get_attribute('id')
            suffix = item.find_element_by_xpath(".//a").get_attribute('href')
            urls.append(f"{self.ROOT_DOMAIN}{suffix}")
        
        self.write_urls('\n'+'\n'.join(urls), self.cur_fpath)
        
        return item_id


    def get_all_urls(self, field):

        SCROLL_PAUSE_TIME = 2
        last_id = None
        self.start()
        self.get_page_by_url(f"{self.ROOT_DOMAIN}/search/{field}")
        

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Get 30 item urls
            last_id = self.get_urls_from_items(last_id)
            
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
