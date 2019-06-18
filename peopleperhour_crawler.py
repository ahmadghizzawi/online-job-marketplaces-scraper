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


def crawl_site(url, city, task, driver_path):
    # Path to your chromedriver.exe directory
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(driver_path, options=options)
    # Load webpage
    browser.get(url)
    browser.implicitly_wait(1)

    browser.close()


def main():
    crawl_site(
        "https://www.peopleperhour.com/hire-freelancers?ref=hp-v3", "london"
    )
