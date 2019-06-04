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

As sometimes in linux/macOS/windows pip refers to python 2.x

## TaskRabbit
The TaskRabbit scraper was written in November 2018. Therefore, you might have to do some changes before scraping
depending on how severe the changes are. 

## Running the script
In order to run Taskrabbit_crawler.py you need to execute the following command:
`python3 Taskrabbit_crawler.py -f queriesFiles `

queriesFiles option: will be the queries json file containing an id, task_title, city and a url. It needs to be placed in ./data/taskrabbit , in case you didn't provide an attribute for -f the crawler will generate a new queries file with the help of the spider where it default name will be final_queries.json

resultFolder option: the default result folder is ./Datasets/Taskrabbit/results . In case you want to change the results folder you need to create a new folder in ./Datasets/Taskrabbit/ with the wanted name and then pass the folder name with -r option. The results will be in a new sub directory with the time when the crawler is executed (format : MonthsDay-Hour-Min). You will need to run the following command:

`python3 Taskrabbit_crawler.py -f queriesFiles -r resultFolder`

picsFolder option: the default pic folder is ./Datasets/Taskrabbit/pics . In case you want to change the pics folder you need to create a new folder in ./Datasets/Taskrabbit/ with the wanted name and then pass the folder name with -p option. The results will be in a new sub directory with the time when the crawler is executed (format : MonthsDay-Hour-Min). You will need to run the following command:

`python3 Taskrabbit_crawler.py -f queriesFiles -p picsFolder`

## Results 
You can find the results of Taskrabbit_crawler.py in ./Datasets/Taskrabbit/ 
In the pics folder you will find the some sub_folder containing the pics gathered from the crawler, the sub_folder are differents in their timeStamps where each one is created when the crawler was launched. Same goes with results folder where we find the json file of each query.

# Author
Ahmad Ghizzawi (ahg05@mail.aub.edu)
