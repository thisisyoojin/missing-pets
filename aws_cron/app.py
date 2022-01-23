import os
from scraper.scraper_func import scraper_functions
from stop_instance import invoke_lambda


if __name__ == "__main__":

    region = os.environ.get('region', '')
    access_key = os.environ.get('access_key', '')
    secret_key = os.environ.get('secret_key', '')
    
    func = scraper_functions['doglost']()
    invoke_lambda(region, access_key, secret_key)