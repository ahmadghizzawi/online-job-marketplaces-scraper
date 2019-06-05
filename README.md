# Online Job Marketplaces Scraper
This repository contains scripts that were used to crawl and scrape online job marketplaces such as TaskRabbit and Fiverr 
for research purposes. The way scraping is conducted is similar across all platforms that we scraped; we define a set queries where a query is a combination of parameters that yield a ranked 
list of users. For example, in TaskRabbit's case that would be a combination of a location and service
type, i.e. _Home Cleaners in New York_.

## IMPORTANT NOTE
The scripts are not fully stable. 

## Requirements
- Python 3.x: https://www.anaconda.com/distribution/ 
- ChromeDriver v < 73: https://chromedriver.storage.googleapis.com/index.html?path=2.46/

After downloading the ChromeDriver, make sure that you update ./Taskrabbit_crawler.py to point to the driver you downloaded.

### Dependencies
`pip install -r requirements.txt`

or

`pip3 install -r requirements.txt`

As sometimes in linux/macOS/windows pip refers to python 2.x as the default python language

## TaskRabbit
The TaskRabbit scraper was written in November 2018. Therefore, you might have to do some changes before scraping
depending on how severe the changes are. 

## Running the script
In order to run taskrabbit_crawler.py you need to execute the following command:
`python3 Taskrabbit_crawler.py -w webDriver -q queriesFiles `

webDriver option: in the webDriver option you need to provide the path to your chrome driver that you downloaded earlier. This parameter is required in order to execute the script 

queriesFiles option: will be the queries json file containing an id, task_title, city and a url. It needs to be placed in ./data/taskrabbit , in case you didn't provide an attribute for -f the crawler will generate a new queries file with the help of the spider where it default name will be final_queries.json

output option: the default output folder is ./Datasets/Taskrabbit/ . In case you want to change the output folder you need to create manually the folder in which you want to save the results and then pass the folder path with -o option.
You will need to run the following command:

`python3 Taskrabbit_crawler.py -w webDriver -q queriesFiles -o output`


## Results 
You can find the results of taskrabbit_crawler.py in ./Datasets/Taskrabbit/
in this folder you will find the time stamp folder created when you launched the scripts (format Year-Months_DayTHour-Min-Sec). Inside that folder there will be one folder named pics containing the pics crawled by the queries and a results folder containing the results of the differents json file for each successful query. Finally you will find also a json file named failed_queries.json containing the unsuccessful query

# Author
Ahmad Ghizzawi (ahg05@mail.aub.edu)
