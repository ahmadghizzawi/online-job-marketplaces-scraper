import argparse
import json
import os
import subprocess
import time
import urllib.request
import concurrent.futures
import sys
import asyncio
import threading

from src.crawler import OJMCrawler, RankingItem
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify
from urllib.parse import urlparse


class MistertempCrawler(OJMCrawler):
    def crawl(self):
        query = self.query
        # Load webpage
        self.browser.get(query.url)
        self.browser.implicitly_wait(1)
        # Enter task and city
        self.browser.find_element_by_class_name(
            "react-autosuggest__input"
        ).send_keys(query.title)
        self.browser.find_element_by_xpath(
            "//input[@placeholder='Ville']"
        ).send_keys(query.city)
        time.sleep(1)
        self.browser.find_element_by_css_selector("button").click()

        time.sleep(2)
        self.browser.find_element_by_class_name(
            "filter-checkbox-photo-video"
        ).click()
        time.sleep(1)
        list_workers = []
        iteration_number = 0
        try:
            # If there is only one page of result than there is no button to go to
            # the next page
            number_of_pages = int(
                self.browser.find_element_by_xpath(
                    "//button[@class='next']/preceding-sibling::button"
                ).text
            )
        except NoSuchElementException:
            number_of_pages = 1

        for k in range(number_of_pages):
            i = iteration_number
            iteration_number = 0
            try:
                while True:
                    iteration_number += 1
                    picture = self.browser.find_element_by_xpath(
                        '(//div[@class="avatar-container"]/img)['
                        + str(iteration_number)
                        + "]"
                    ).get_attribute("src")
                    o = urlparse(picture)
                    name_img = o.path.split("/")[-1]

                    worker_dict = RankingItem(
                        name_img,
                        picture,
                        iteration_number,
                        {
                            "page": i,
                            "rating": "",
                            "query": slugify(query.city + "_" + query.title),
                            "experience_time": self.browser.find_element_by_xpath(
                                '(//div[@class="xp"])['
                                + str(iteration_number)
                                + "]"
                            ).text,
                        },
                    )

                    try:
                        worker_dict.metadata["rating"] = (
                            self.browser.find_element_by_xpath(
                                '(//div[@class="rating"])['
                                + str(iteration_number)
                                + "]"
                            ).text,
                        )
                    except NoSuchElementException:
                        # No rating
                        worker_dict.metadata["rating"] = None

                    list_workers.append(worker_dict)

            except NoSuchElementException:
                if number_of_pages != 1:
                    self.browser.find_element_by_class_name("next").click()
                iteration_number += i
                time.sleep(3)

        # Write the list of workers found in a json file
        # Must create results folder in the directory of datasets

        self.browser.close()
        return list_workers
