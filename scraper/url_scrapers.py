from scraper import Scraper
import time

class UrlScraper(Scraper):
    """
    Base url scraper

    Method
    read_urls(): read urls from database
    get_new_urls(): compare between database and current crawled urls. get only new urls to pass to page_scrapers.
    """
    def __init__(ROOT_DOMAIN, option=None):
        super().__init__(ROOT_DOMAIN, option)

    def read_urls():
        pass

    def get_new_urls():
        pass


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


    def get_all_urls_to_file(self, fpath):
        
        self.start()
        current_page = self.ROOT_DOMAIN
        next = True
        
        while next:
            self.get_page_by_url(current_page)
            cur_urls = self.get_urls_in_current_page()
            self.urls.extend(cur_urls)
            
            next = self.get_next_page(current_page)
            current_page = next
            self.write_to_text('\n'+'\n'.join(cur_urls), fpath)

        self.close()
        print('Finished getting urls.')



class UrlScraperWithScroll(UrlScraper):
    """
    Scraping all urls through all pages
    """

    def __init__(self, ROOT_DOMAIN):
        super().__init__(ROOT_DOMAIN)

    def find_next_items_with_xpath():
        """
        should return xpath
        """
        raise NotImplementedError("please implement locat_next_item function")


    def get_urls_in_current_page(self, last_id, write_to_file=True):

        # if last_id:
        #     xpath = f"//div[@id='{last_id}']//following-sibling::div[contains(@id, 'gi-')]"
        # else:
        #     xpath = "//div[contains(@id, 'gi-')]"

        # items = self.driver.find_elements_by_xpath(xpath)
        items = self.find_next_items_with_xpath()
        item_id = None

        for item in items:
            item_id = item.get_attribute('id')
            suffix = item.find_element_by_xpath(".//a").get_attribute('href')
            item_url = f"{self.ROOT_DOMAIN}{suffix}"
            if write_to_file:
                self.write_to_json({
                    "id": item_id,
                    "item_url": item_url
                }, "./barkley/data/animal_search/lost_urls.json")
        
        return item_id


    def get_all_urls(self, field):

        SCROLL_PAUSE_TIME = 1
        last_id = None
        self.start()
        self.get_page_by_url(f"{self.ROOT_DOMAIN}/search/{field}")
        

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Get 30 item urls
            last_id = self.get_30_urls(last_id)
            
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


    def get_info_from_page(self):

        self.start()
        self.get_page_by_url("https://www.animalsearchuk.co.uk/ALP399353")
        
        pet_info = {}
        header = self.driver.find_element_by_xpath("//div[contains(@class, 'lost')]")
        
        titles = header.find_element_by_xpath(".//h1").text.split()
        for th, t in zip(['status', 'species', 'name'], titles):
            pet_info[th] = t

        pet_info['id'] = header.find_element_by_xpath(".//h2").text
        pet_info['last_seen_address'] = header.find_element_by_xpath(".//h3").text
        pet_info['situation'] = header.find_element_by_xpath(".//h4").text.split(':')[1].strip()
        
        descs = header.find_elements_by_xpath(".//ul[@class='hl']/li")
        for h, desc in zip(['colour', 'gender', 'breed', 'last_seen_date'], descs):
            pet_info[h] = desc.text

        details = self.driver.find_elements_by_xpath("//h2[contains(text(), 'Missing On')]/ancestor::div[1]/p")
        pet_info['age'] = details[1].text
        pet_info['description'] = details[2].text

        pet_info['circumstances'] = self.driver.find_element_by_xpath("//h2[contains(text(), 'Circumstances')]/following-sibling::p").text
        pet_info['chipped'] = self.driver.find_element_by_xpath("//img[contains(@src, 'chip')]/ancestor::div[1]/following-sibling::p").text
        pet_info['collar'] = self.driver.find_element_by_xpath("//img[contains(@src, 'collar')]/ancestor::div[1]/following-sibling::p").text
        pet_info['neutered'] = self.driver.find_element_by_xpath("//i[contains(@class, 'fa-venus-mars')]/ancestor::div[1]/following-sibling::p").text
        
        
        img_src = self.driver.find_element_by_xpath("//div[@class='has-img']/ancestor::a[1]").get_attribute('href')
        
        file_name = f"{pet_info['id']}.jpg"
        fpath = f"./barkley/data/animal_search/img/{file_name}"
        self.download_img_file(img_src, fpath)
        self.save_img_to_s3(fpath, f"animal_search/{file_name}")
        pet_info['img_url'] = f"s3://barkley-imgs/animal_search/{file_name}"
        
        
        query = self.create_insert_query("lost_animalsearch", pet_info)
        conn = db.connect()
        conn.execute(query)
