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


from src.helper import parse_arguments, create_output_folders
from src.mistertemp_crawler import MistertempCrawler
from src.get_queries import get_queries
from src.crawler import Query, RankingItem, RankingItemEncoder
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify
from urllib.parse import urlparse


def main():

    args = parse_arguments()

    if args.queriesfile is None:
        args.queriesfile = get_queries(args)

    with open("./data/" + args.platform + "/" + args.queriesfile) as f:
        entries = json.load(f)

    res, pic = create_output_folders(args.output)

    list_query = [
        Query(
            "https://www.mistertemp.com/espace-recruteur/",
            entry["service"],
            entry["city"],
        )
        for entry in entries
    ]

    for query in list_query:
        crawler = MistertempCrawler(query, args.webdriver)
        list_result = crawler.crawl()
        with open(
            res + "/" + slugify(query.city + "-" + query.title) + ".json", "w"
        ) as fout:
            json.dump(list_result, fout, cls=RankingItemEncoder)
        for result in list_result:
            urllib.request.urlretrieve(
                result.picture_url, pic + "/" + result.id + ".jpg"
            )


main()
