from urllib.parse import urlparse , parse_qs
from urllib.request import urlopen
import json

city = []
unique = ["\n"]
result = []
with open('cities.json') as f:
	cities = json.load(f)

for entry in cities:
	city = (entry['city'])
	if not city in unique:
		unique.append(city)
		result.append(entry)
with open('final_cities.json', 'w') as nf:
	json.dump(result, nf)

