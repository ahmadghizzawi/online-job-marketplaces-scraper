import json


result = []

with open('queries.json') as f:
	queries = json.load(f)
	
with open('cities.json') as f:
	cities = json.load(f)

for entry in queries:
	for entry2 in cities:
		item = {}
		item['id'] = entry['id']
		item['task_title'] = entry['task_title']
		item['city'] = entry2['city']
		item['url'] = entry['url']
		result.append(item)

with open('final_queries.json', 'w') as nf:
	json.dump(result, nf)

