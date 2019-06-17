import json

result = []

with open("final_services.json") as f:
    services = json.load(f)

with open("final_cities.json") as f:
    cities = json.load(f)

for service in services:
    for city in cities:
        item = {}
        item["city"] = city["city"]
        item["service"] = service["service"]
        result.append(item)

with open("queries.json", "w") as nf:
    json.dump(result, nf)
