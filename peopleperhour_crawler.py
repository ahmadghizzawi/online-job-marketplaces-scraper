import argparse
import json
import os
import re
import subprocess
import time
import urllib.request
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify


def crawl_site(city, url, driver_path):
    # Path to your chromedriver.exe directory
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(driver_path, options=options)
    # Load webpage
    browser.get(url)
    browser.implicitly_wait(1)

    element = browser.find_element_by_css_selector(
        "div.pull-right.drop-filters-trigger"
    )
    element.find_elements_by_tag_name("a")[0].click()
    suite = browser.find_elements_by_xpath('//input[@id="location-input"]')[0]
    suite.send_keys(city)
    chopper_list = browser.find_elements_by_css_selector(
        "div.tt-dataset-location-input-typeahead"
    )[0]
    city = chopper_list.find_element_by_css_selector("p")
    city.click()
    time.sleep(2)
    list_url = []
    list_element = browser.find_elements_by_css_selector(
        "div.items.clearfix.items-results"
    )[0].find_elements_by_xpath("child::*")
    for element in list_element:
        list_url.append(
            element.find_elements_by_tag_name("a")[0].get_attribute("href")
        )
    time.sleep(100)


def main():
    crawl_site(
        "london",
        "https://www.peopleperhour.com/hire-freelancers/designers/freelance-elearning-designer",
        "/home/boubou/Stage/chromedriver",
    )


main()
