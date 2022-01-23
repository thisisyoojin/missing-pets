from scraper import *
from scraper.doglost import Doglost
from scraper.vet_scraper import Vet_Scraper


vet_params ={
    "ROOT_DOMAIN": "https://findavet.rcvs.org.uk/find-a-vet-practice/?filter-choice=location&filter-keyword=+&filter-searchtype=practice#primary-navigation",
    "next_xpath": "//ol[@class='paging']/li[@class='next']/a",
    "data_path": "./barkley/data/vet_data.json"
}

doglost_params = {
    "ROOT_DOMAIN": "https://www.doglost.co.uk/dog-search.php?status=Lost&page=434",
    "fpaths" : {
        "prev": "./data/doglost/url_prev",
        "cur": "./data/doglost/url_cur"
    },
    "option": None, 
    "next_xpath": "//div[@id='resultsPager']/a[text()='Next'][1]", 
    "items_xpath": "//tr[@class='lost']", 
}

scraper_functions = {
    "vet": Vet_Scraper(**vet_params).get_all_data(),
    "doglost": Doglost(**doglost_params).get_all_data(),
}