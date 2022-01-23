from selenium import webdriver
import time
import requests


class Scraper:
    """
    Scraper base class. Other scraper will be inherited from this class.

    Init Params
    ROOT_DOMAIN: domain address to scrap
    option: firefox option
    
    Method
    self.start(): start firefox webdriver
    self.get_page_by_url(url, time): browse to url and wait for given time (default:5 sec)
    self.download_img_file(src_url, fpath): save image file from source url to filepath
    self.close(): close firfox webdriver
    """

    def __init__(self, ROOT_DOMAIN, option=None):
        self.ROOT_DOMAIN = ROOT_DOMAIN
        self.option = option
        self.driver = None

    def start(self):
        self.driver = webdriver.Firefox(self.option)

    def get_page_by_url(self, url, wait_for=5):
        self.driver.get(url)
        time.sleep(wait_for)


    def download_img_file(self, src_url, fpath):
        response = requests.get(src_url)
        with open(fpath, 'wb+') as f:
            f.write(response.content)


    def close(self):
        self.driver.close()


