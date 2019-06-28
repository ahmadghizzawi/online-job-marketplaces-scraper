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

from src.crawler import OJMCrawler, RankingItem
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify
from urllib.parse import urlparse


class TaskrabbitCrawler(OJMCrawler):
    def crawl(self):
        print("TODO")

    def exit(self):
        self.browser.close()
