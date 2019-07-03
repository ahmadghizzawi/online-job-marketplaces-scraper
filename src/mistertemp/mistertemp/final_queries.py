# flake8: noqa

import os
import sys
import json
import inspect

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()))
)
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(1, parentdir)

from crawler import Query, QueryEncoder

result = []

with open("queries.json") as f:
    queries = json.load(f)

for query in queries:
    result.append(Query("", query["service"], query["city"]))

with open("final_queries.json", "w") as nf:
    json.dump(result, nf, cls=QueryEncoder)
