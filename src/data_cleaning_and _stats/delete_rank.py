import os
import glob
import json
import csv
import time

from slugify import slugify


worker = []
path = "./last/*"
files = glob.glob(path)
info = []
# next line added to pass the flake8, remove it when executing (line 15)
partitions = []

for filename in files:
    with open(filename) as r:
        query = json.load(r)
        for entry in query:
            info.append(
                {"id": entry[partitions[0]]}
            )  # ,"gender": entry['gender'],"ethnicity": entry['ethnicity'], "ranking": entry['rank']})
        worker = {
            "city": entry["city"],
            "task": entry["task"],
            "partitions": info,
        }
        print(worker)
    with open("./final_last/" + filename.replace("./last/", ""), "w") as f:
        json.dump(worker, f)
    info = []
    worker = []
