import os
import glob
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas

worker = []
path = "./results/*"
files = glob.glob(path)
workers = {}
count = 0
hist = {}
counted = []
for filename in files:
    with open(filename) as r:
        query = json.load(r)
    counter = {int(len(query))}
    for entry in query:
        worker.append({"id": entry["id"]})
        workers[entry["id"]] = 0
        last = {"number-of-worker": entry["rank"]}
        # hist[entry['rank']]= hist.get(entry['rank'], 0) + 1
# print(counted)
"""for k in sorted(counted):
   print('{0:5d} {1}'.format(k, '+' * counted[k]))
print(len(list(workers.keys())))
print(count)
average = (count / len(files))

print("The mean is:", average)
#with open('number_of_worker.json','w') as f:
    #json.dump(worker, f)
"""
with open("workers_id.json", "w") as f:
    json.dump(worker, f)
print(len(worker))
# print(len(list(workers.keys())))

"""
n , bins, patches = plt.hist(x=counted, bins=10, color='#0504aa',alpha=0.7, rwidth= 0.9)
plt.grid(axis='y', alpha=1)
plt.xlabel('Number of Taskers')
plt.ylabel('Number of Queries')
#maxfreq = n.max()
#plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
plt.show()
"""
