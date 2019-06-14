from selenium import webdriver
import json
import urllib.request
import time
import re
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify


def get_services(url):
    browser = webdriver.Chrome("/home/boubou/Stage/chromedriver")

    # Load webpage
    browser.get(url)
    browser.implicitly_wait(1)
    # get jobs
    list_jobs = []
    list_alphabet = [str(chr(97 + i)) for i in range(26)]
    time.sleep(2)
    for letter1 in list_alphabet:
        browser.find_element_by_class_name(
            "react-autosuggest__input"
        ).send_keys(letter1)
        for letter2 in list_alphabet:
            browser.find_element_by_class_name(
                "react-autosuggest__input"
            ).send_keys(letter2)
            try:
                for i in range(1, 40):
                    list_jobs.append(
                        browser.find_elements_by_xpath(
                            "//li[@data-suggestion-index='" + str(i) + "']"
                        )[0].text
                    )
            except IndexError:
                browser.find_element_by_class_name(
                    "react-autosuggest__input"
                ).send_keys("\u0008")
                continue
        browser.find_element_by_class_name(
            "react-autosuggest__input"
        ).send_keys("\u0008")
        browser.find_element_by_class_name(
            "react-autosuggest__input"
        ).send_keys("\u0008")

    # put jobs list in json file
    with open("services.json", "w") as services:
        json.dump(list_jobs, services, ensure_ascii=False)
    browser.close()


def main():
    try:
        get_services("https://www.mistertemp.com/espace-recruteur/")
    except Exception as error:
        print("Error:", error)
    time.sleep(2)


main()
