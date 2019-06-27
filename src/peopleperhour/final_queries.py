import json


result = []

with open("final_services.json") as f:
    queries = json.load(f)

with open("peopleperhour_cities.json") as f:
    cities = json.load(f)

for entry in cities:
    for entry2 in queries:
        for i in range(1, 6):
            item = {}
            item["task"] = entry2["task"]
            item["country"] = entry["country"]
            item["city"] = entry[str(i)]
            item["url"] = entry2["url"]
            result.append(item)

with open("final_queries.json", "w") as nf:
    json.dump(result, nf, ensure_ascii=False)
