
from base.scraper import Scraper
from base.url_scrapers import UrlScraperWithNext


class Doglost(UrlScraperWithNext):
    
    def __init__(self, ROOT_DOMAIN, fpaths, option=None, next_xpath='', items_xpath=''):
        super().__init__(ROOT_DOMAIN, fpaths, option, next_xpath, items_xpath)
        self.get_all_urls()
        self.urls_to_read = self.extract_new_urls()


    def get_data_per_page(self, url):
        
        self.get_page_by_url(url)
        fields = self.driver.find_elements_by_xpath("//ul[@id='dogDetails']/li[not(contains(@class, 'dogLink'))]")
        data = {}
        for field in fields:
            f = field.text.split('\n')
            if len(f) > 1:
                data[f[0]] = f[1]
        
        # pics = self.driver.find_elements_by_xpath("//ul[@id='dogPics']//img")
        # src_urls = [p.get_attribute('src') for p in pics]
        # img_paths = []
        # for s in src_urls:
        #     img_path = f"./barkley/data/pet_data/imgs/{s.split('/')[-1]}"
        #     img_paths.append(img_path)
        #     self.save_img_file(s, img_path)

        # dd['img_urls'] = img_paths



    def get_all_data(self, start, end):
        
        self.start()
        partial_urls = self.urls_to_read[start:end]
        for url in partial_urls:
            self.get_data_per_page(url)
        self.close()
        return f"{start}-{end} extracted"