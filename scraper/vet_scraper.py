from base.url_scrapers import UrlScraperWithNext


class Vet_Scraper(UrlScraperWithNext):

    def __init__(self, ROOT_DOMAIN, next_xpath, data_path):
        super().__init__(ROOT_DOMAIN, next_xpath=next_xpath)
        self.data_path = data_path
    

    def get_items_in_page(self):
        
        divs = self.driver.find_elements_by_xpath("//div[contains(@id, 'item')]")
        for d in divs:
            name, address, post_code, phone, email = None, None, None, None, None
            name = d.find_element_by_xpath(".//h2[@class='item-title']/a").text
            address = d.find_element_by_xpath(".//div[@class='item-address']").text
            post_code = d.find_element_by_xpath(".//div[@class='item-address']/span").text
            
            try:
                phone = d.find_element_by_xpath(".//span[contains(@class, 'tel')]").text.lstrip('phone2 ')
                email = d.find_element_by_xpath(".//a[contains(@class, 'email')]").text.lstrip('envelope ')
            
            except Exception as e:
                print(e)
            
            finally:
                self.write_to_json({'name': name, 'address': address, 'post_code': post_code, 'phone': phone, 'email': email}, self.data_path)
                

    
    def get_all_data(self):
        
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



