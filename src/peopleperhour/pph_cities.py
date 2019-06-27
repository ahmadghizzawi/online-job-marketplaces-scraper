from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify
import json
import time


def get_cities(url):
    browser = webdriver.Chrome(
        "/home/boubou/Github/online-job-marketplaces-scraper/chromedriver"
    )
    browser.get(url)
    browser.implicitly_wait(1)
    list_cities = []
    list_url = []
    service = browser.find_elements_by_css_selector(
        "body > p:nth-child(2) > table:nth-child(1) > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr"
    )[0]
    list_object = service.find_elements_by_tag_name("a")
    for object in list_object:
        list_url.append(object.get_attribute("href"))
    print(list_url)
    for url2 in list_url:
        browser.get(url2)
        time.sleep(1)
        try:
            list_stuff = browser.find_element_by_css_selector(".datatable")
            dict = {
                "country": url2.split("/")[-1],
                "1": list_stuff.find_elements_by_tag_name("span")[0].text,
                "2": list_stuff.find_elements_by_tag_name("span")[1].text,
                "3": list_stuff.find_elements_by_tag_name("span")[2].text,
                "4": list_stuff.find_elements_by_tag_name("span")[3].text,
                "5": list_stuff.find_elements_by_tag_name("span")[4].text,
            }
            print(dict)
            list_cities.append(dict)
        except Exception:
            print("not enough cities")
            continue

    with open("peopleperhour_cities.json", "w") as f:
        json.dump(list_cities, f, ensure_ascii=False)

    browser.close()


def main():
    try:
        get_cities("https://data.mongabay.com/igapo/largest_cities.htm")
    except Exception as error:
        print("Error:", error)
    time.sleep(2)


main()
