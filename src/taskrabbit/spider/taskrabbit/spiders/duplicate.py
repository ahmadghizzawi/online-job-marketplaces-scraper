from urllib.parse import urlparse , parse_qs
from urllib.request import urlopen
import json

url = []
parse = []
parsed = []
unique = []
result = []
with open('final.json') as f:
	urls = json.load(f)

for entry in urls:
	url = (entry['url'])
	parse = (urlparse(str(url)))
	parsed = parse_qs(parse.query)
	if not parsed['task_template_id'] in unique:
		unique.append(parsed['task_template_id'])
		result.append(entry)
with open('new_file.json', 'w') as nf:
	json.dump(result, nf)

