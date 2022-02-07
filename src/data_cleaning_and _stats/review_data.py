import pandas as pd
import csv

pd.set_option("display.expand_frame_repr", False)
df = pd.read_csv("./Batch_3689328_batch_results.csv")

items = df[
    [
        "Input.image_url",
        "Answer.asian.on",
        "Answer.black.on",
        "Answer.white.on",
        "Answer.female.on",
        "Answer.male.on",
    ]
]

aggregation_functions = {
    "Answer.asian.on": "sum",
    "Answer.black.on": "sum",
    "Answer.white.on": "sum",
    "Answer.female.on": "sum",
    "Answer.male.on": "sum",
}
items = items.groupby(df["Input.image_url"]).aggregate(aggregation_functions)

cols = ["Answer.asian.on", "Answer.black.on", "Answer.white.on"]
items = items[
    (items["Answer.asian.on"] >= 2)
    | (items["Answer.black.on"] >= 2)
    | (items["Answer.white.on"] >= 2)
]

list_dict = []

for x in items.itertuples():
    dict = {}
    dict["Image_URL"] = x[0]
    sub = str(x[0]).replace("http://ahmadghizzawi.me/new-pics/", "")
    ID = sub.replace(".jpg", "")
    dict["ID"] = ID
    if x[1] >= 2:
        dict["Ethnicity"] = "asian"
    elif x[2] >= 2:
        dict["Ethnicity"] = "black"
    else:
        dict["Ethnicity"] = "white"
    if x[4] >= 2:
        dict["Gender"] = "female"
    else:
        dict["Gender"] = "male"
    list_dict.append(dict)

with open("taskrabbit_labelled.csv", "w") as f:
    fieldnames = ["Gender", "Ethnicity", "Image_URL", "ID"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for dict in list_dict:
        writer.writerow(
            {
                "Gender": dict["Gender"],
                "Ethnicity": dict["Ethnicity"],
                "Image_URL": dict["Image_URL"],
                "ID": dict["ID"],
            }
        )
