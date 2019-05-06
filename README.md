# Online Job Marketplaces Scraper
This repository contains scripts that were used to crawl and scrape online job marketplaces such as TaskRabbit and Fiverr 
for research purposes. The way scraping is conducted is similar across all platforms that we scraped; we define a set queries where a query is a combination of parameters that yield a ranked 
list of users. For example, in TaskRabbit's case that would be a combination of a location and service
type, i.e. _Home Cleaners in New York_.

## Requirements
- Python 3.x: https://www.anaconda.com/distribution/ 
- ChromeDriver v < 73: https://chromedriver.storage.googleapis.com/index.html?path=2.46/

After downloading the ChromeDriver, make sure that you update src/taskrabbit/scrapers/services_by_city.py
to point to driver you downloaded.

### Dependencies
`pip install -r requirements.txt`

## TaskRabbit
The TaskRabbit scraper was written in November 2018. Therefore, you might have to do minor changes before scraping
depending on how severe the changes are. 

# Author
Ahmad Ghizzawi (ahg05@mail.aub.edu)
