# missing-pets

### Motivation
According to the research of pet insurers, five dogs go missing in the UK every single day. This means that 10% of dog owners in Britain have sadly experienced their dog go missing at least once in their lives. This project is a small gesture to help this situation.

Currently, missing/found/stray dog data is scattered on multiple websites with different structures of data. Some websites have well-structured data while some rely on vague descriptions. The data is also focused on the dog only, even though data of the last seen place might be crucial to find the missing dog. The goal of this project is to create a centralised dataset, which is consisting of dog and location-based data.

### pre-requisite
- linux
- python3

### How to run

When you want to scrape doglost website
```
python main.py --scraper='doglost'
```
When you want to scrape vet website
```
python main.py --scraper='vet'
```

### set up virtual-environment
```
python3 -m venv my_env
source my_env/bin/activate
pip install -r requirements.txt
```