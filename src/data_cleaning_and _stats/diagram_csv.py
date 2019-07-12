import csv
import json
import statistics

total = 0
worker = []
with open("diagram.csv", mode="w") as f:
    fieldnames = ["number"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    with open("number_of_worker.json") as r:
        queries = json.load(r)
    for query in queries:
        total = total + int(query["number of worker"])
        writer.writerow({"number": query["number of worker"]})
        worker.append(query["number of worker"])

x = statistics.mean(worker)
print("Total worker:", total)
