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


def crawl_site(city, url, driver_path, task, output_path):
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
    time.sleep(2)
    city_pos = chopper_list.find_element_by_css_selector("p")
    city_pos.click()
    time.sleep(2)
    list_url = []
    list_element = browser.find_elements_by_css_selector(
        "div.items.clearfix.items-results"
    )[0].find_elements_by_xpath("child::*")
    for element in list_element:
        list_url.append(
            element.find_elements_by_tag_name("a")[0].get_attribute("href")
        )
    last_page = (
        browser.find_element_by_id("freelancer-listing-pager")
        .find_elements_by_xpath("child::*")[-2]
        .find_elements_by_tag_name("a")[0]
        .get_attribute("data-page")
    )
    url_base = browser.current_url
    for i in range(2, int(last_page) + 1):
        browser.get(url_base + "&page=" + str(i))
        time.sleep(1)
        list_element = browser.find_elements_by_css_selector(
            "div.items.clearfix.items-results"
        )[0].find_elements_by_xpath("child::*")
        for element in list_element:
            list_url.append(
                element.find_elements_by_tag_name("a")[0].get_attribute("href")
            )

    ranking = 1
    list_workers = []
    for url in list_url:
        browser.get(url)
        time.sleep(1)
        worker = {
            "city": city,
            "rating": "",
            "language": [
                element.text
                for element in browser.find_element_by_css_selector(
                    "div.member-languages.clearfix"
                ).find_elements_by_tag_name("a")
            ],
            "rank": ranking,
            "number_of_project": "",
        }
        ranking += 1
        try:
            worker["rating"] = browser.find_element_by_class_name(
                "total-rating"
            ).text
        except NoSuchElementException:
            worker["rating"] = None
        list_workers.append(worker)
    print(list_workers)
    with open(
        output_path + "/" + slugify(city + "-" + task) + ".json", "w"
    ) as fout:
        json.dump(list_workers, fout)

    # Query finished close the browser
    browser.close()


def main():
    crawl_site(
        "Mumbai",
        "https://www.peopleperhour.com/hire-freelancers/designers/3d-artist",
        "/home/boubou/Stage/chromedriver",
        "task_name",
        "./datasets/peopleperhour/",
    )


main()
