from scraper import UrlScraper

class District_scraper(UrlScraper):
    """
    
    """
    
    def __init__(self, ROOT_DOMAIN, next_xpath='', data_path=''):
        super().__init__(ROOT_DOMAIN, next_xpath=next_xpath)
        self.data_path = data_path
    

    def get_items_in_page(self):
    
        table = self.driver.find_element_by_xpath("//table[contains(@class, 'postcodeDistrictsTable')]")
        
        headers = table.find_elements_by_xpath(".//thead/tr/th")
        self.write_to_text('|'.join([h.text for h in headers])+'\n', 'test.txt')

        rows = table.find_elements_by_xpath(".//tbody/tr")
        for row in rows:
            r_data = row.find_elements_by_xpath(".//td")
            self.write_to_text('|'.join([r.text for r in r_data])+'\n', 'test.txt')

    
    def get_all_items(self):
        
        self.start()
        idx, next = 0, True
        current_page = self.ROOT_DOMAIN
        
        while next:
            self.get_page_by_url(current_page)
            self.get_items_in_page()
            
            idx += 1
            print(f'page {idx} extracted')

            next = self.get_next(current_page)
            print(next)
            current_page = next
            

        print('Finished extracting data')


    



if __name__ == "__main__":

    params = {
        "ROOT_DOMAIN": "https://www.doogal.co.uk/PostcodeDistricts.php",
        "next_xpath": "//li[@class='next']/a[@rel='next']"
    }

    gc = District_scraper(**params)
    gc.get_all_items()