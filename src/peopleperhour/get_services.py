import json
import time
import selenium

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def get_services(url):
    options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    options.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(
        "/home/boubou/Stage/chromedriver", options=options
    )
    # Load webpage
    browser.get(url)
    browser.implicitly_wait(1)
    # get jobs
    list_jobs = []
    time.sleep(2)
    browser.find_element_by_xpath("//a[@data-toggle='dropdown']").click()
    time.sleep(1)
    parent_categories = browser.find_element_by_css_selector(
        "ul.category-tree.sidebar-filter-options.tree-node.depth-0.last-level"
    )
    main_categories = parent_categories.find_elements_by_tag_name("li")
    list_url1 = []
    list_url2 = []
    for element in main_categories[1::]:
        list_url1.append(
            element.find_elements_by_tag_name("a")[0].get_attribute("href")
        )

    for urls in list_url1:
        browser.get(urls)
        new_parent = browser.find_element_by_css_selector(
            "ul.tree-node.depth-1.last-level"
        )
        new_main = new_parent.find_elements_by_tag_name("li")
        for new_element in new_main:
            list_url2.append(
                new_element.find_elements_by_tag_name("a")[0].get_attribute(
                    "href"
                )
            )
    for urls in list_url2:
        print(urls)
        browser.get(urls)
        try:
            new_parent = browser.find_element_by_css_selector(
                "ul.tree-node.depth-2.last-level"
            )
            new_main = new_parent.find_elements_by_tag_name("li")
            for new_element in new_main:
                list_jobs.append(
                    {
                        "url": new_element.find_elements_by_tag_name("a")[
                            0
                        ].get_attribute("href")
                    }
                )
        except NoSuchElementException:
            continue

    # put jobs list in json file
    with open("services.json", "w") as services:
        json.dump(list_jobs, services, ensure_ascii=False)
    browser.close()


def main():
    try:
        get_services("https://www.peopleperhour.com/hire-freelancers")
    except Exception as error:
        print("Error:", error)
    time.sleep(2)


main()
