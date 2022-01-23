import os
from scraper.scraper_func import scraper_functions


if __name__ == "__main__":
    func = scraper_functions[os.environ.get('scraper')]
    func()