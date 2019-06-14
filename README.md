# Online Job Marketplaces Scraper
This repository contains scripts that were used to crawl and scrape online job marketplaces such as TaskRabbit and Fiverr 
for research purposes. The way scraping is conducted is similar across all platforms that we scraped; we define a set 
queries where a query is a combination of parameters that yield a ranked list of users. For example, in TaskRabbit's 
case that would be a combination of a location and service type, i.e. _Home Cleaners in New York_.

## Requirements
- Python 3.x: https://www.anaconda.com/distribution/ 
- ChromeDriver v < 73: https://chromedriver.storage.googleapis.com/index.html?path=2.46/

### Dependencies
`pip install -r requirements.txt`

## TaskRabbit
The TaskRabbit scraper was written in November 2018. Therefore, you might have to do some changes before scraping
depending on how severe the changes are. 

### Crawl TaskRabbit
In order to run taskrabbit_crawler.py you need to execute the following command:
`python Taskrabbit_crawler.py -w webDriver -q queriesFiles `

webDriver option: in the webDriver option you need to provide the path to your chrome driver that you downloaded earlier. This parameter is required in order to execute the script 

queriesFiles option: will be the queries json file containing an id, task_title, city and a url. It needs to be placed in ./data/taskrabbit , in case you didn't provide an attribute for -f the crawler will generate a new queries file with the help of the spider where it default name will be final_queries.json

output option: the default output folder is ./datasets/taskrabbit/ . In case you want to change the output folder you need to create manually the folder in which you want to save the results and then pass the folder path with -o option.
You will need to run the following command:

`python Taskrabbit_crawler.py -w webDriver -q queriesFiles -o output`

## Mistertemp
The TaskRabbit scraper was written in June 2019.

### Crawl TaskRabbit
In order to run mistertemp_crawler.py you need to execute the following command:
`python mistertemp.py.py -w webDriver -q queriesFiles 
`
mistertemp_crawler.py has one more parameter than taskrabbit_crawler.py.add
Threads option: The mistertemp crawler uses only one thread originilay. To increase the speed of the computation choose the number of threads the program will use with the attribute -t


## Results 
You can find the results of taskrabbit_crawler.py in ./datasets/taskrabbit/
in this folder you will find the time stamp folder created when you launched the scripts (format Year-Months_DayTHour-Min-Sec). Inside that folder there will be one folder named pics containing the pics crawled by the queries and a results folder containing the results of the differents json file for each successful query. Finally you will find also a json file named failed_queries.json containing the unsuccessful query

# Authors
Ahmad Ghizzawi (ahg05@mail.aub.edu)

Sultan Mourthadhoi (sultan.mourthadhoi@etu.univ-grenoble-alpes.fr)
