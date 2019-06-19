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


failed_queries = []
counter = 1


def cookies(element):
    if element.is_displayed():
        element.click()
    else:
        print("cookie banner hidden")


def assembly(boxes, browser):
    if len(boxes) == 5:
        print("found 5 boxes")
        assembly = browser.find_elements_by_css_selector(
            ".build-input-list li:last-of-type > input[type='radio']"
        )
        for element in assembly:
            element.click()
        browser.find_element_by_css_selector(".btn.btn-primary").click()
    time.sleep(3)


def task_option(elements, browser):
    for element in elements:
        element.click()

    browser.find_element_by_css_selector(".btn.btn-primary").click()
    time.sleep(1)


def reviews_retiever(browser, worker_dict, next_page):
    while True:
        # Retrieve reviews
        reviews = browser.find_elements_by_css_selector(".tasker-review")
        if len(reviews) > 0:
            for review in reviews:
                worker_dict["reviews"].append(
                    {
                        "text": review.find_element_by_css_selector(
                            ".exterior__bottom--sm"
                        ).text,
                        "date": review.find_element_by_css_selector(
                            ".review-author"
                        ).text.split(",", 1)[1],
                    }
                )
        if len(next_page) > 0:
            next_page[0].click()
            next_page = browser.find_elements_by_xpath(
                "//span[@class='current']/following-sibling::a"
            )
            time.sleep(0.5)
        if len(next_page) == 0:
            break


def crawl_site(args):
    url, city, task, driver_path, output_path, pics_path, entry, total = args
    # Path to your chromedriver.exe directory
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    browser = webdriver.Chrome(driver_path, options=options)
    # Load webpage
    browser.get(url)
    browser.implicitly_wait(1)

    # dismiss cookie if it is displayed
    element = browser.find_element_by_css_selector(
        ".js__cookie-banner-dismiss"
    )
    cookies(element)

    # # Click on the first task type
    # browser.find_element_by_css_selector('#metro-templates
    # .btn.btn-secondary.btn-small.js__formEntry').click()

    # TASK INTEREST
    # Task interest selected (i'm just browsing)
    browser.find_element_by_id("intent_level_low").click()

    browser.find_element_by_css_selector(".btn.btn-primary").click()

    # TASK LOCATION / START ADDRESS
    # Location selected from the query
    browser.find_element_by_css_selector(
        "input[name='location.freeform']"
    ).send_keys(city)
    # Unit or Apt optional, we selected number 5
    browser.find_element_by_id("address2").send_keys("5")
    time.sleep(1)
    browser.find_element_by_css_selector(".btn.btn-primary").click()
    time.sleep(1)

    # TASK END ADDRESS (HELP MOVING CASE)
    # Condition for the case where we have 5 boxes (assembly task)
    boxes = browser.find_elements_by_css_selector(".build-group")
    assembly(boxes, browser)

    # TASK OPTIONS
    # Loop to select the first option in each elements of the task options
    elements = browser.find_elements_by_css_selector(
        ".build-input-list li:first-of-type > input[type='radio']"
    )
    task_option(elements, browser)

    # TASK DETAILS
    # we fill the task details with one letter in order to be able to select
    # the primary button
    browser.find_element_by_css_selector(
        "textarea[name='description']"
    ).send_keys("t")
    time.sleep(1)

    browser.find_element_by_css_selector(".btn.btn-primary").click()
    time.sleep(1)

    # WORKERS LIST
    # Task date selected to within a week
    browser.find_element_by_id(
        "recommendations__schedule-option-next_week"
    ).click()

    # sleep time in order to load the whole page correctly
    time.sleep(3)

    workers = browser.find_elements_by_css_selector(
        ".recommendations__result_wrapper"
    )

    # Loop to build the list of workers
    list_workers = []
    iteration_number = 1
    for worker in workers:
        # worker build
        worker_dict = {
            "id": worker.find_element_by_css_selector(
                ".recommendations__result.recommendations__result--tasker"
            ).get_attribute("data-user-id"),
            "rank": iteration_number,
            "picture": worker.find_element_by_css_selector(
                ".recommendations__avatar__circular"
            ).get_attribute("src"),
            "positive_rating": worker.find_elements_by_xpath(
                "//i[@class='ss-lnr-star']/following-sibling::span"
            )[iteration_number - 1].text,
            "number_of_relevant_tasks": worker.find_elements_by_xpath(
                "//i[@class='ss-lnr-check-circle']/following-sibling::span"
            )[iteration_number - 1].text,
            "great_value_badge": "",
            "elite_tasker": "",
            "new_tasker": "",
            "how_can_help": worker.find_element_by_css_selector(
                ".recommendations__blurb"
            ).text,
            "right_person": "",
            "when_tasking": "",
            "number_of_reviews_received": "",
            "number_of_relevant_reviews_received": "",
            # Return the string of per_hour_rate
            "per_hour_rate": float(
                re.findall(
                    r"[-+]?\d*\.\d+|\d+",
                    worker.find_element_by_css_selector("strong").text,
                )[0]
            ),
            # City and the task separated by '_'
            "query": slugify(city + "_" + task),
            "reviews": [],
        }

        # positive rating
        try:
            # Return the float of the percentage of Positve rating
            worker_dict["positive_rating"] = float(
                int(
                    re.findall(
                        r"[-+]?\d*\.\d+|\d+", worker_dict["positive_rating"]
                    )[0]
                )
                / 100
            )
        except IndexError:
            # Case of positive rating not found
            worker_dict["positive_rating"] = None

        # number of relevant tasks

        try:
            # Return the number of relevant tasks
            worker_dict["number_of_relevant_tasks"] = int(
                re.findall(
                    r"[-+]?\d*\.\d+|\d+",
                    worker_dict["number_of_relevant_tasks"],
                )[0]
            )
        except IndexError:
            # Case of relevant tasks not found
            worker_dict["number_of_relevant_tasks"] = None

        # worker has great value badge?
        try:
            # Boolean for value_badge
            worker.find_element_by_css_selector(
                ".recommendations__great-value-badge"
            )
            worker_dict["great_value_badge"] = True
        except NoSuchElementException:
            # Case of value_badge not found
            worker_dict["great_value_badge"] = False

        # worker is an elite tasker?
        try:
            # Boolean for elite_tasker
            worker.find_element_by_css_selector(".ss-medal-star")
            worker_dict["elite_tasker"] = True
        except NoSuchElementException:
            # Case of elite_tasker not found
            worker_dict["elite_tasker"] = False

        # worker is a new tasker?
        try:
            # Boolean for new_tasker
            worker.find_element_by_css_selector(".ss-happy-lined")
            worker_dict["new_tasker"] = True
        except NoSuchElementException:
            # Case of new_tasker not found (ss-happy-lined)
            worker_dict["new_tasker"] = False

        # open user popup (Profile & reviews)
        worker.find_element_by_css_selector(
            ".recommendations__result-name"
        ).click()

        # retrieve the first free text
        try:
            worker_dict[
                "right_person"
            ] = browser.find_elements_by_css_selector(
                ".tasker--bio-responses"
            )[
                0
            ].text
        except Exception:
            print("no right person")

        # retrieve the second free text
        try:
            worker_dict[
                "when_tasking"
            ] = browser.find_elements_by_css_selector(
                ".tasker--bio-responses"
            )[
                1
            ].text
        except Exception:
            print("no when tasking")

        # retrieve number of reviews
        reviews_dropdown = browser.find_elements_by_css_selector(
            ".reviews__filter--select option"
        )
        if len(reviews_dropdown) > 0:
            worker_dict["number_of_reviews_received"] = int(
                re.findall(r"[-+]?\d*\.\d+|\d+", reviews_dropdown[-1].text)[0]
            )
            worker_dict["number_of_relevant_reviews_received"] = int(
                re.findall(r"[-+]?\d*\.\d+|\d+", reviews_dropdown[0].text)[0]
            )

            # select all reviews
            reviews_dropdown[-1].click()
        else:
            # If worker have no review
            worker_dict["number_of_reviews_received"] = 0
            worker_dict["number_of_relevant_reviews_received"] = 0

        # while clicking on right arrow is permissible, retrieve the next page
        # of reviews
        next_page = browser.find_elements_by_xpath(
            "//span[@class='current']/following-sibling::a"
        )
        reviews_retiever(browser, worker_dict, next_page)

        # close popup of the worker profile & reviews
        browser.find_element_by_css_selector(".lightbox--dismiss").click()

        # Add the worker to the list of workers
        list_workers.append(worker_dict)
        # Save users pictures
        # Must create pics folder in your directory

        urllib.request.urlretrieve(
            worker_dict["picture"],
            pics_path + "/" + str(worker_dict["id"]) + ".jpg",
        )
        iteration_number += 1

        time.sleep(0.5)

    # Write the list of workers found in a json file
    # Must create results folder in the directory of datasets
    with open(
        output_path + "/" + slugify(city + "-" + task) + ".json", "w"
    ) as fout:
        json.dump(list_workers, fout)

    # Query finished close the browser
    browser.close()


def crawl_site_aux(args):
    global failed_queries
    global counter
    url, city, task, driver_path, output_path, pics_path, entry, total = args
    try:
        print("Running query #", counter, "out of", total, "queries")
        counter_failed = counter
        counter += 1
        crawl_site(args)
    except Exception as error:
        print("query #", counter_failed, "failed.")
        print("Error:", error)
        failed_queries.append(entry)


def main():
    parser = argparse.ArgumentParser(description="taskrabbit crawler")
    parser.add_argument(
        "-w",
        "--web",
        type=str,
        metavar="",
        required=True,
        help=" The path to your chrome web driver",
    )
    parser.add_argument(
        "-q",
        "--queries",
        type=str,
        metavar="",
        help=" The path to the file containing the queries you wish to work with",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="",
        default="./datasets/taskrabbit/",
        help="The output directory containing the results, pics and the failed queries",
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        metavar="",
        default=1,
        help="The number of threads you want to work with",
    )

    args = parser.parse_args()

    scrapy_project_path = "./src/Taskrabbit/spider/Taskrabbit/"

    if args.queries is None:
        print("No input file passed \nAutomatic crawl Taskrabbit.com")
        # crawling of the taskrabbit cities from the scrapy path
        subprocess.call(
            "scrapy crawl cities -o cities.json",
            shell=True,
            cwd=scrapy_project_path,
        )
        # moving the cities file to the correct folder for the next step
        subprocess.call(
            "mv cities.json ./../../cities.json",
            shell=True,
            cwd=scrapy_project_path,
        )
        # cleaning and removing duplicate from cities.json
        subprocess.call(
            "python3 clean_cities.py", shell=True, cwd="./src/Taskrabbit/"
        )
        # copying the final and clean city file to the data folder
        subprocess.call(
            "cp final_cities.json ./../../data/taskrabbit/final_cities.json",
            shell=True,
            cwd="./src/Taskrabbit/",
        )
        # crawling the list of all the task available
        subprocess.call(
            "scrapy crawl allqueries -o allqueries.json",
            shell=True,
            cwd=scrapy_project_path,
        )
        # crawling the last url of each task
        subprocess.call(
            "scrapy crawl task_urls -o final.json",
            shell=True,
            cwd=scrapy_project_path,
        )
        # moving the query file to the correct for the next step
        subprocess.call(
            "mv final.json ./../../final.json",
            shell=True,
            cwd=scrapy_project_path,
        )
        # deleting the intermediate file allqueries
        subprocess.call(
            "rm allqueries.json", shell=True, cwd=scrapy_project_path
        )
        # deleting duplicate on the query file
        subprocess.call(
            "python3 helpers.py", shell=True, cwd="./src/Taskrabbit/"
        )
        # merging the city and query file together
        subprocess.call(
            "python3 final_queries.py", shell=True, cwd="./src/Taskrabbit/"
        )
        # copying the final query file to the data folder
        subprocess.call(
            "cp final_queries.json ./../../data/taskrabbit/final_queries.json",
            shell=True,
            cwd="./src/Taskrabbit/",
        )
        # removing all of the json file left in src folder
        subprocess.call("rm *.json", shell=True, cwd="./src/Taskrabbit/")
        args.queries = "./data/taskrabbit/final_queries.json"

    # Creation of the timeStamp folder
    now = datetime.now().isoformat().replace(":", "-")
    timestr = str(now)
    source1 = args.output
    folder = os.path.join(source1 + timestr)
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Creation of the sub folder pics inside of the timeStamp folder
    source = folder + "/"
    pic = os.path.join(source + "pics")
    if not os.path.exists(pic):
        os.makedirs(pic)

    # Creation of the sub folder results inside of the timeStamp folder
    source2 = folder + "/"
    res = os.path.join(source2 + "results")
    if not os.path.exists(res):
        os.makedirs(res)

    with open(args.queries) as f:
        entries = json.load(f)

    # Counter used to know the number of query
    global failed_queries
    list_args = []
    for entry in entries:
        if entry["city"].endswith("UK"):
            # UK cities, UK taskrabbit
            website = "https://www.taskrabbit.co.uk"
        elif entry["city"] in ["Toronto, CA", "Vancouver, CA"]:
            # Canada cities, Canadien taskrabbit
            website = "https://www.taskrabbit.ca"
        else:
            # USA taskrabbit
            website = "https://www.taskrabbit.com"
        # List of attrbute for crawl_site fonction
        list_args.append(
            (
                website + entry["url"],
                entry["city"],
                entry["task_title"],
                args.web,
                res,
                pic,
                entry,
                len(entries),
            )
        )
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=args.threads
    ) as executor:
        executor.map(crawl_site_aux, list_args)
    with open(folder + "/failed_queries.json", "w") as f:
        json.dump(failed_queries, f)


if __name__ == "__main__":
    main()
