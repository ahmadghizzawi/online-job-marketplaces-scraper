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


def create_output_folders(output_path):
    def create_folder(name):
        if not os.path.exists(name):
            os.makedirs(name)

    # Creation of the timeStamp folder
    timestr = str(datetime.now().isoformat().replace(":", "-"))
    folder = os.path.join(output_path + timestr)
    create_folder(folder)

    # Creation of the sub folder pics inside of the timeStamp folder
    pic = os.path.join(folder + "/" + "pics")
    create_folder(pic)

    # Creation of the sub folder results inside of the timeStamp folder
    res = os.path.join(folder + "/" + "results")
    create_folder(res)

    return res, pic


def parse_arguments():
    parser = argparse.ArgumentParser(description="parser")
    parser.add_argument(
        "-p",
        "--platform",
        type=str,
        metavar="",
        required=True,
        choices=["mistertemp", "taskrabbit"],
        help="Platform to crawl",
    )
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
        "--queriesfile",
        type=str,
        metavar="",
        help=" The files containing the queries you wish to work with",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="",
        help="The output directory containing the results, pics and the failed queries",
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        metavar="",
        default=1,
        help="The number of threads you want to use",
    )
    args = parser.parse_args()
    if args.output is None:
        args.output = "./datasets/" + args.platform + "/"
    return args
