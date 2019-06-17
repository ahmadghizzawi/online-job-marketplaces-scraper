import argparse
import json
import os
import subprocess
import time
import urllib.request
import concurrent.futures
from urllib.parse import urlparse

from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify


def crawl_site(args):
    url, city, task, chromedriver_path, output_path, pics_path = args
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    # Necessary for headless option otherwise the code raises an exception
    options.add_argument("--window-size=1920,1080")
    # Path to your chromedriver.exe directory
    browser = webdriver.Chrome(chromedriver_path, chrome_options=options)
    # Load webpage
    browser.get(url)
    browser.implicitly_wait(1)
    # Enter task and city
    browser.find_element_by_class_name("react-autosuggest__input").send_keys(
        task
    )
    browser.find_element_by_xpath("//input[@placeholder='Ville']").send_keys(
        city
    )
    time.sleep(1)
    browser.find_element_by_css_selector("button").click()

    time.sleep(1)
    browser.find_element_by_class_name("filter-checkbox-photo-video").click()
    time.sleep(1)
    list_workers = []
    iteration_number = 0
    try:
        # If there is only one page of result than there is no button to go to
        # the next page
        number_of_pages = int(
            browser.find_element_by_xpath(
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
                picture = browser.find_element_by_xpath(
                    '(//div[@class="avatar-container"]/img)['
                    + str(iteration_number)
                    + "]"
                ).get_attribute("src")
                o = urlparse(picture)
                name_img = o.path.split("/")[-1]

                worker_dict = {
                    "page": i,
                    "rank": iteration_number,
                    "rating": "",
                    "name_img": name_img,
                    "picture": picture,
                    "query": slugify(city + "_" + task),
                    "experience_time": browser.find_element_by_xpath(
                        '(//div[@class="xp"])[' + str(iteration_number) + "]"
                    ).text,
                }

                try:
                    worker_dict["rating"] = (
                        browser.find_element_by_xpath(
                            '(//div[@class="rating"])['
                            + str(iteration_number)
                            + "]"
                        ).text,
                    )
                except NoSuchElementException:
                    # No rating
                    worker_dict["rating"] = None

                list_workers.append(worker_dict)
                urllib.request.urlretrieve(
                    worker_dict["picture"], pics_path + "/" + name_img + ".jpg"
                )

        except NoSuchElementException:
            if number_of_pages != 1:
                browser.find_element_by_class_name("next").click()
            iteration_number += i
            time.sleep(3)

    # Write the list of workers found in a json file
    # Must create results folder in the directory of datasets
    with open(
        output_path + "/" + slugify(city + "-" + task) + ".json", "w"
    ) as fout:
        json.dump(list_workers, fout)

    browser.close()


def main():
    parser = argparse.ArgumentParser(description="mistertemp crawler")
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
        "--Queriesfile",
        type=str,
        metavar="",
        help=" The files containing the queries you wish to work with",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="",
        default="./datasets/mistertemp/",
        help="The output directory containing the results, pics and the failed queries",
    )
    parser.add_argument(
        "-t",
        "--workers",
        type=int,
        metavar="",
        default=1,
        help="The number of threads you want to use",
    )
    args = parser.parse_args()

    if args.Queriesfile is None:
        print("No input file passed \nAutomatic crawl mistertemp.com")
        subprocess.call(
            "scrapy crawl cities -o cities.json",
            shell=True,
            cwd="./src/mistertemp/mistertemp/",
        )
        subprocess.call(
            "python3 get_services.py -w " + args.webdriver,
            shell=True,
            cwd="./src/mistertemp/mistertemp/",
        )
        subprocess.call(
            "python3 final_services.py",
            shell=True,
            cwd="./src/mistertemp/mistertemp/",
        )
        subprocess.call(
            "mv ./mistertemp/cities.json cities.json",
            shell=True,
            cwd="./src/mistertemp/mistertemp/",
        )
        subprocess.call(
            "python3 make_queries.py",
            shell=True,
            cwd="./src/mistertemp/mistertemp/",
        )
        subprocess.call(
            "mv ./src/mistertemp/mistertemp/queries.json ./data/mistertemp/queries.json",
            shell=True,
            cwd=None,
        )
        subprocess.call(
            "rm *.json", shell=True, cwd="./src/mistertemp/mistertemp"
        )
        args.Queriesfile = "queries.json"

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

    with open("./data/mistertemp/" + args.Queriesfile) as f:
        queries = json.load(f)

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=args.workers
    ) as executor:
        crawl_args = [
            (
                "https://www.mistertemp.com/espace-recruteur/",
                entry["city"],
                entry["service"],
                args.webdriver,
                res,
                pic,
            )
            for entry in queries
        ]
        executor.map(crawl_site, crawl_args)


main()
