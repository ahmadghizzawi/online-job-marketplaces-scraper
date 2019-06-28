import argparse
import json
import os
import subprocess
import time
import urllib.request
import concurrent.futures
import sys
import asyncio
import threading

from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify
from urllib.parse import urlparse


def get_queries(args):

    if args.platform == "mistertemp":
        return get_queries_mistertemp(args)
    elif args.platform == "taskrabbit":
        return get_queries_taskrabbit(args)


def get_queries_mistertemp(args):
    print("No input file passed \nAutomatic crawl mistertemp.com")
    subprocess.call(
        "scrapy crawl cities -o cities.json",
        shell=True,
        cwd="./mistertemp/mistertemp/",
    )
    subprocess.call(
        "python3 get_services.py -w " + args.webdriver,
        shell=True,
        cwd="./mistertemp/mistertemp/",
    )
    subprocess.call(
        "python3 final_services.py", shell=True, cwd="./mistertemp/mistertemp/"
    )
    subprocess.call(
        "mv ./mistertemp/cities.json cities.json",
        shell=True,
        cwd="./mistertemp/mistertemp/",
    )
    subprocess.call(
        "python3 make_queries.py", shell=True, cwd="./mistertemp/mistertemp/"
    )
    subprocess.call(
        "mv ./mistertemp/mistertemp/queries.json ./data/mistertemp/queries.json",
        shell=True,
        cwd="..",
    )
    subprocess.call("rm *.json", shell=True, cwd="./mistertemp/mistertemp")
    args.queriesfile = "/data/mistertemp/queries.json"

    return args.queriesfile


def get_queries_taskrabbit(args):
    scrapy_project_path = "./src/Taskrabbit/spider/Taskrabbit/"
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
        "mv final.json ./../../final.json", shell=True, cwd=scrapy_project_path
    )
    # deleting the intermediate file allqueries
    subprocess.call("rm allqueries.json", shell=True, cwd=scrapy_project_path)
    # deleting duplicate on the query file
    subprocess.call("python3 helpers.py", shell=True, cwd="./src/Taskrabbit/")
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
    args.queriesfile = "./data/taskrabbit/final_queries.json"
    return args.queriesfile
