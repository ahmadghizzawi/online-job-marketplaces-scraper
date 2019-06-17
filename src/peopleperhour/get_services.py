import json
import time
import selenium
from selenium import webdriver


def get_services(url):
    browser = webdriver.Chrome("/home/boubou/Stage/chromedriver")

    # Load webpage
    browser.get(url)
    browser.implicitly_wait(1)
    # get jobs
    list_jobs = []
    time.sleep(2)
    browser.find_element_by_xpath("//a[@data-toggle='dropdown']").click()
    time.sleep(3)
    parent_categories = browser.find_element_by_css_selector(
        "ul.category-tree.sidebar-filter-options.tree-node.depth-0.last-level"
    )
    main_categories = parent_categories.find_elements_by_tag_name("li")
    time.sleep(3)
    i = 0
    for element in main_categories:
        if i > 0:
            element.find_elements_by_tag_name("a")[0].click()
            time.sleep(3)
            new_parent = browser.find_element_by_css_selector(
                "ul.tree-node.depth-1.last-level"
            )
            new_main = new_parent.find_elements_by_tag_name("li")
            for new_element in new_main:
                new_element.find_elements_by_tag_name("a")[0].click()
                time.sleep(2)
                print(browser.getCurrentUrl())
        i = 1

        time.sleep(3)
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
