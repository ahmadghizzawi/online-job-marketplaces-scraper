from abc import ABC, abstractmethod
from selenium import webdriver
from slugify import slugify
from selenium.webdriver import ChromeOptions
from typing import List


class RankingItem:
    """
        Represent a single worker in a ranked list of workers.
    """
    def __init__(self, id: str, picture_url: str, rank: int, metadata: dict=None):
        """
        :param id: ranking item id. Should be some unique identifier for the item in the list crawled item. For example,
                   in TaskRabbit, this would be the worker id.
        :param picture_url: the URL of the worker's picture.
        :param rank: the rank of the worker in the ranking list.
        :param metadata: a dictionary of any other crawled information about the ranking item.
        """
        self.id = id
        self.picture_url = picture_url
        self.rank = rank
        self.metadata = {} if metadata is None else metadata


class Query:
    def __init__(self, url: str, title: str, city: str, country: str=None, id=None):
        """
        :param url: url of the query.
        :param title: title of the query. In TaskRabbit, this would be Home Cleaning for example.
        :param city: city where the query is.
        :param country: country where the query is.
        :param id: id of the query if available. If not, a combination of the title and city will be used.
        """
        self.url = url
        self.title = title
        self.city = city
        self.country = country

        if id is None:
            self.id = slugify(title + '-' + city)
        else:
            self.id = id


class OJMCrawler(ABC):
    """
    Online job marketplace crawler abstract class.
    """
    def __init__(self, query: Query, chromedriver_path, options: ChromeOptions=None):
        """
        :param query: query to be crawled
        :param chromedriver_path: path of the chrome driver
        :param options: ChromeOptions object to be passed to ChromeWebDriver
        """
        self.query = query

        if options is None:
            options = ChromeOptions()
            options.add_argument("headless")
            # Necessary for headless option otherwise the code raises an exception
            options.add_argument("--window-size=1920,1080")
        self.browser = self.__initialize_webdriver(chromedriver_path, options)

    @staticmethod
    def __initialize_webdriver(chromedriver_path, options: ChromeOptions):
        """
        Initializes the chrome webdriver with the options passed.

        :param chromedriver_path: the path to the Chrome webdriver on your machine
        :param options: options to be passed to Chrome webdriver
        :return:
        """
        return webdriver.Chrome(chromedriver_path, chrome_options=options)

    @abstractmethod
    def crawl(self) -> List[RankingItem]:
        """
        Crawls the given query from a platform. Must return a list of RankingItem.

        :return: list of ranking items that were crawled
        """
        raise NotImplementedError

    def exit(self):
        """
        Cleans up post-crawling. It's usage is still pending.
        """
        raise NotImplementedError
