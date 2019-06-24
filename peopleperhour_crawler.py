import argparse
import json
import os
import re
import subprocess
import time
import urllib.request
import concurrent.futures

from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify


def crawl_site(args, browser, browser_is_not_used, j):
    url, city, task, chromedriver_path, output_path, pics_path = args
    # Load webpage

    browser.get(url)
    browser.implicitly_wait(1)
    try:
        element = browser.find_element_by_css_selector(
            "div.pull-right.drop-filters-trigger"
        )
        element.find_elements_by_tag_name("a")[0].click()
    except NoSuchElementException:
        element = browser.find_element_by_css_selector("ul.filters__list")
        element.find_elements_by_tag_name("li")[3].find_elements_by_tag_name(
            "a"
        )[0].click()
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
            # "service": service,
            "language": [
                element.text
                for element in browser.find_element_by_css_selector(
                    "div.member-languages.clearfix"
                ).find_elements_by_tag_name("a")
            ],
            "rank": ranking,
            "number_of_project": "",
            "picture": browser.find_elements_by_xpath(
                '//div[@class="profile-pic"]/img'
            )[0].get_attribute("src"),
            "id": browser.find_element_by_class_name("action-buttons-inner")
            .find_elements_by_tag_name("a")[0]
            .get_attribute("href")
            .split("=")[1],
        }
        print(worker["id"])
        ranking += 1
        try:
            worker["rating"] = browser.find_element_by_class_name(
                "total-rating"
            ).text
        except NoSuchElementException:
            worker["rating"] = None
        list_workers.append(worker)
        urllib.request.urlretrieve(
            worker["picture"], pics_path + "/" + worker["id"] + ".jpg"
        )

    with open(
        output_path + "/" + slugify(city + "-" + task) + ".json", "w"
    ) as fout:
        json.dump(list_workers, fout)

    # Query finished close the browser


def main():
    parser = argparse.ArgumentParser(description="peopleperhour crawler")
    parser.add_argument(
        "-w",
        "--webdriver",
        type=str,
        metavar="",
        required=True,
        help="The PATH of the chromedriver",
    )
    parser.add_argument(
        "-q",
        "--queriesfile",
        type=str,
        metavar="",
        help=" The files containing the queries you wish to work with",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="",
        default="./datasets/peopleperhour/",
        help="The output directory containing the results, pics and the failed queries",
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        metavar="",
        default=1,
        help="The number of threads you want to use",
    )
    args = parser.parse_args()

    if args.queriesfile is None:
        print("No input file passed \nAutomatic crawl peopleperhour.com")
        """
        TODO
        """
        args.queriesfile = "queries.json"

    # Creation of the timeStamp folder
    now = datetime.now().isoformat().replace(":", "-")
    timestr = str(now)
    source1 = args.output
    folder = os.path.join(source1 + timestr)
    if not os.path.exists(folder):
        os.makedirs(folder)
        source = folder + "/"

    # Creation of the sub folder pics inside of the timeStamp folder
    pic = os.path.join(source + "pics")
    if not os.path.exists(pic):
        os.makedirs(pic)

    # Creation of the sub folder results inside of the timeStamp folder
    source2 = folder + "/"
    res = os.path.join(source2 + "results")
    if not os.path.exists(res):
        os.makedirs(res)

    with open("./data/peoplePerHour/" + args.queriesfile) as f:
        queries = json.load(f)

    crawl_args = [
        (entry["url"], entry["city"], entry["task"], args.webdriver, res, pic)
        for entry in queries
    ]

    browsers = []
    crawl_args.reverse()
    browser_is_not_used = [True for i in range(args.threads)]
    for j in range(args.threads):
        options = webdriver.ChromeOptions()
        # options.add_argument("headless")
        # Necessary for headless option otherwise the code raises an exception
        options.add_argument("--window-size=1920,1080")
        # Path to your chromedriver.exe directory
        browsers.append(
            webdriver.Chrome(args.webdriver, chrome_options=options)
        )

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=args.threads
    ) as executor:
        while len(crawl_args) > 0:
            for j in range(args.threads):
                if browser_is_not_used[j]:
                    browser_is_not_used[j] = False
                    executor.submit(
                        crawl_site,
                        crawl_args.pop(),
                        browsers[j],
                        browser_is_not_used,
                        j,
                    )


main()

# Star-b481b4de4ede69a041179a971f82eb0d
# Star-b481b4de4ede69a041179a971f82eb0d
# Star-dcfdd3ecaa5e46803528211ce1167dad
