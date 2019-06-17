import argparse
import json
import urllib.request
import time
import re
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify
from selenium import webdriver


def get_services(url, chromedriver_path):

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    # Necessary for headless option otherwise the code raises an exception
    options.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(chromedriver_path, chrome_options=options)

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
    parser = argparse.ArgumentParser(description="mistertemp services crawler")
    parser.add_argument(
        "-w",
        "--webdriver",
        type=str,
        metavar="",
        required=True,
        help="The PATH of the chromedriver",
    )
    args = parser.parse_args()

    try:
        get_services(
            "https://www.mistertemp.com/espace-recruteur/", args.webdriver
        )
    except Exception as error:
        print("Error:", error)
    time.sleep(2)


main()
