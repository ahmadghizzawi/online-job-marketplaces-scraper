# Online Job Marketplaces Scraper
This repository contains scripts that were used to crawl and scrape online job marketplaces such as TaskRabbit and Fiverr 
for research purposes. The way scraping is conducted is similar across all platforms that we scraped; we define a set 
queries where a query is a combination of parameters that yield a ranked list of users. For example, in TaskRabbit's 
case that would be a combination of a location and service type, i.e. _Home Cleaners in New York_.

## Setup
### Requirements
- Python 3.x: https://www.anaconda.com/distribution/ 
- ChromeDriver v < 73: https://chromedriver.storage.googleapis.com/index.html?path=2.46/

### Dependencies
```bash
pip install -r requirements.txt
```

### Precommit Hooks
```bash
pre-commit install
```

#### Automated Linting and static code checking pipeline
Read more here: https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/
![alt text](https://ljvmiranda921.github.io/assets/png/tuts/precommit_pipeline.png)

## TaskRabbit
The TaskRabbit scraper was written in *June 2019*. Therefore, you might have to do some changes before scraping
depending on how severe the changes are. 

### Crawl TaskRabbit
In order to run taskrabbit_crawler.py you need to execute the following command:

```bash
usage: taskrabbit_crawler.py [-h] -w  [-q] [-o] [-t]

taskrabbit crawler

optional arguments:
  -h, --help       show this help message and exit
  -w , --web       The path to your chrome web driver
  -q , --queries   The path to the file containing the queries you wish to
                   work with
  -o , --output    The output directory containing the results, pics and the
                   failed queries
  -t , --threads   The number of threads you want to work with
```

#### Example

```bash
python taskrabbit_crawler.py -w ./chromedriver -q queries.json 
```

would grab the chromedriver placed in the online-job-marketplaces-scraper folder and use the queries placed in the 
data/taskrabbit folder. The output folder would be the default ouput folder which is 
dataset/taskrabbit.

## MisterTemp
MisterTemp scraper was written in *June 2019*. Therefore, you might have to do some changes before scraping
depending on how severe the changes are. 

### Crawl MisterTemp
In order to run mistertemp_crawler.py you need to execute the following command:

```bash
mistertemp crawler

optional arguments:
  -h, --help           show this help message and exit
  -w , --webdriver     The PATH of the chromedriver
  -q , --queriesfile   The files containing the queries you wish to work with
  -o , --output        The output directory containing the results, and pics 
  -t , --workers       The number of threads you want to use

```
#### Example
```bash
python mistertemp_crawler.py -w ./chromedriver -q queries.json -t 5
```

would grab the chromedriver placed in the online-job-marketplaces-scraper folder and use the queries placed in the 
data/mistertemp folder. It would also use 5 threads and the output folder would be the default ouput folder which is 
dataset/mistertemp.

## Results 
```
└── datasets
    ├── mistertemp
    │   └── 2019-06-05T16-46-32
    │       ├── pics
    │       └── results
    └── taskrabbit
        └── 2019-06-05T16-46-32
            ├── pics
            └── results    
```
# Authors
Ahmad Ghizzawi (ahg05@mail.aub.edu)

Sultan Mourthadhoi (sultan.mourthadhoi@etu.univ-grenoble-alpes.fr)

Yann Bourreau (yann.bourreau@gmail.com)