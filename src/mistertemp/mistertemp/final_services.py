import json


def final_services():  # merge json file
    with open("services.json") as f:
        entries = json.load(f)
    list_jobs = quicksort(entries)
    list_jobs_final = [{"service": list_jobs[0]}]
    for i in range(1, len(list_jobs)):
        if list_jobs[i] != list_jobs[i - 1]:
            list_jobs_final.append({"city": list_jobs[i]})
    with open("services_final.json", "w") as services:
        json.dump(list_jobs_final, services, ensure_ascii=False)


def quicksort(t):
    if t == []:
        return []
    else:
        pivot = t[0]
        t1 = []
        t2 = []
        for x in t[1:]:
            if x < pivot:
                t1.append(x)
            else:
                t2.append(x)
        return quicksort(t1) + [pivot] + quicksort(t2)


final_services()
