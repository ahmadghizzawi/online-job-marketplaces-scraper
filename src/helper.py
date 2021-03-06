import argparse
import os
from datetime import datetime

from src.mistertemp_crawler import MistertempCrawler
from src.taskrabbit_crawler import TaskrabbitCrawler


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

    return res, pic, folder


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Online job marketplaces crawler"
    )
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


def get_url(platform, query):
    def get_url_mistertemp():
        return "https://www.mistertemp.com/espace-recruteur/"

    def get_url_taskrabbit(query):
        if query["city"].endswith("UK"):
            # UK cities, UK taskrabbit
            website = "https://www.taskrabbit.co.uk"
        elif query["city"] in ["Toronto, CA", "Vancouver, CA"]:
            # Canada cities, Canadien taskrabbit
            website = "https://www.taskrabbit.ca"
        else:
            # USA taskrabbit
            website = "https://www.taskrabbit.com"
        return website + query["url"]

    if platform == "mistertemp":
        return get_url_mistertemp()
    elif platform == "taskrabbit":
        return get_url_taskrabbit(query)


def get_crawler(platform):
    if platform == "mistertemp":
        return MistertempCrawler
    elif platform == "taskrabbit":
        return TaskrabbitCrawler
