import os
import glob
import json
import csv
import time

from slugify import slugify


path = "./results/*"
files = glob.glob(path)

workers = {}
with open("Final_Taskers.csv") as cf:
    csv_reader = csv.reader(cf, delimiter=",")
    for row in csv_reader:
        workers[row[3]] = {"id": row[3], "gender": row[0], "ethnicity": row[1]}

for filename in files:
    worker = []
    info = []
    rang = 1
    with open(filename) as r:
        query = json.load(r)
        for entry in query:
            if workers.get(entry["id"]) is not None:
                info.append(
                    {
                        "id": workers[entry["id"]]["id"],
                        "gender": workers[entry["id"]]["gender"],
                        "ethnicity": workers[entry["id"]]["ethnicity"],
                        "ranking": rang,
                    }
                )
                rang += 1
        with open("final_cities.json") as f2:
            cities = json.load(f2)
        for ville in cities:
            city = slugify(ville["city"])
            entree = entry["query"]
            if city in entree:
                city_final = ville["city"]
                break
        with open("allqueries.json") as f3:
            services = json.load(f3)
        for service in services:
            un_service = slugify(service["task_title"])
            le_service = entry["query"]
            if un_service in le_service:
                final_service = service["task_title"]
                break
        worker = {
            "city": city_final,
            "task": final_service,
            "partitions": info,
        }
        # print(worker)
    with open("./essai/" + filename.replace("./results/", ""), "w") as f:
        json.dump(worker, f)
