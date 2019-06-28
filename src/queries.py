import argparse
import json
import os
import subprocess
import time
import urllib.request
import concurrent.futures
import psutil
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
    args.queriesfile = "queries.json"

    return args.queriesfile


def get_queries_taskrabbit(args):
    print("TO DO")
