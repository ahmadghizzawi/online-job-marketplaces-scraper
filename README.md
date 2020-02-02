# Online Job Marketplaces Scraper
This repository contains scripts that were used to crawl and scrape online job marketplaces such as TaskRabbit and Fiverr
for research purposes. The way scraping is conducted is similar across all platforms that we scraped; we define a set
queries where a query is a combination of parameters that yield a ranked list of users. For example, in TaskRabbit's
case that would be a combination of a location and service type, i.e. _Home Cleaners in New York_.

## Setup
### Requirements
- Python 3.x: https://www.anaconda.com/distribution/
- ChromeDriver v < 73: https://chromedriver.storage.googleapis.com/index.html?path=2.46/ (This must be placed in the project's root directory)

### Dependencies
```bash
pip install -r requirements.txt
```

### Precommit Hooks (Optional)
```bash
pre-commit install
```

#### Automated Linting and static code checking pipeline
Read more here: https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/
![alt text](https://ljvmiranda921.github.io/assets/png/tuts/precommit_pipeline.png)

## Supported Platforms
The table below lays out the supported platforms, and the last time data was crawled 
off that platform. You might have to do some changes to the code before scraping
depending on whether any significant changes occurred to the website since the last
crawl date.

|  Platform  | Last Crawled |
|:----------:|:------------:|
| TaskRabbit |  June, 2019  |
| MisterTemp |  June, 2019  |

### Crawl Platform
In order to crawl a platform, you need to execute the following command:

```bash
usage: run_crawler.py [-h] -p  -w  [-q] [-o] [-t]
  -p , --platform      Platform to crawl. One of: [taskrabbit, mistertemp]
  -w , --webdriver     The PATH of the chromedriver
optional arguments:
  -h, --help           show this help message and exit
  -q , --queriesfile   The files containing the queries you wish to work with
  -o , --output        The output directory containing the results, pics, and 
                       the failed queries
  -t , --threads       The number of threads you want to use. Defaults to 1.

```

#### MisterTemp Example 
```bash
python run_crawler.py -p mistertemp -w ./chromedriver -q data/mistertemp/queries.json
```

#### TaskRabbit Example 
```bash
python run_crawler.py -p taskrabbit -w ./chromedriver -q data/taskrabbit/final-queries.json
```


### Output
The output of the crawling run will be under the folder `dataset/PLATFORM/TIMESTAMP` with two
folders `pics` and `results`, and will have the following structure: 
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

### Failed queries
Failed queries are dumped in `failed_queries.json` inside the timestamped folder.

## Crawling a new platform
To crawl a new platform, you would need to implement the abstract class [OJMCrawler](https://github.com/ahmadghizzawi/online-job-marketplaces-scraper/blob/master/src/crawler.py#L78-L124). You could use the [taskrabbit](https://github.com/ahmadghizzawi/online-job-marketplaces-scraper/blob/master/src/taskrabbit_crawler.py) and [mistertemp](https://github.com/ahmadghizzawi/online-job-marketplaces-scraper/blob/master/src/mistertemp_crawler.py) as examples to get you started.


# Authors
Ahmad Ghizzawi (ahg05@mail.aub.edu)

Sultan Mourthadhoi (sultan.mourthadhoi@etu.univ-grenoble-alpes.fr)

Yann Bourreau (yann.bourreau@gmail.com)
