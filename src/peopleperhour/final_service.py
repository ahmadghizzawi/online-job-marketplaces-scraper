import json


result = []

with open("services.json") as f:
    services = json.load(f)

for task in services:
    url_split = task["url"].split("/")
    result.append(
        {
            "task": url_split[-3] + "-" + url_split[-2] + "-" + url_split[-1],
            "url": task["url"],
        }
    )

with open("final_services.json", "w") as final_services:
    json.dump(result, final_services, ensure_ascii=False)
