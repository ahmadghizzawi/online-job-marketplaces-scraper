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

from src.helper import (
    parse_arguments,
    create_output_folders,
    get_url,
    get_crawler,
)
from src.mistertemp_crawler import MistertempCrawler
from src.queries import get_queries
from src.crawler import Query, RankingItem, RankingItemEncoder, QueryEncoder
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify
from urllib.parse import urlparse


def main():

    args = parse_arguments()

    if args.queriesfile is None:
        args.queriesfile = get_queries(args)

    with open(args.queriesfile) as f:
        entries = json.load(f)

    res, pic, folder_path = create_output_folders(args.output)

    list_query = [
        Query(
            get_url(args.platform, args.queriesfile),
            entry["service"],
            entry["city"],
        )
        for entry in entries
    ]

    Crawler = get_crawler(args.platform)
    failed = []

    counter = 1
    for query in list_query:
        print("query " + str(counter))
        counter += 1
        crawler = Crawler(query, args.webdriver)
        try:
            list_result = crawler.crawl()
            with open(
                res + "/" + slugify(query.city + "-" + query.title) + ".json",
                "w",
            ) as fout:
                json.dump(list_result, fout, cls=RankingItemEncoder)
            for result in list_result:
                urllib.request.urlretrieve(
                    result.picture_url, pic + "/" + result.id + ".jpg"
                )
        except Exception as e:
            failed.append(query)
            print(e)
            crawler.exit()
    with open(folder_path + "/failed_queries.json", "w") as f:
        json.dump(failed, f, cls=QueryEncoder)


if __name__ == "__main__":
    main()
