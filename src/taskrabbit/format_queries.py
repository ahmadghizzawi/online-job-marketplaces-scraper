# flake8: noqa

import os
import sys
import json
import inspect

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()))
)
parentdir = os.path.dirname(currentdir)
sys.path.insert(1, parentdir)

from crawler import Query, QueryEncoder

result = []

with open("final_queries.json") as f:
    queries = json.load(f)

for query in queries:
    result.append(
        Query(
            query["url"], query["task_title"], query["city"], None, query["id"]
        )
    )

with open("final_queries2.json", "w") as nf:
    json.dump(result, nf, cls=QueryEncoder)
