import csv
import os


with open("taskrabbit.csv", mode="w") as f:
    fieldnames = ["ID", "image_url"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    for filename in os.listdir("./pics"):
        writer.writerow(
            {
                "ID": str(filename).replace(".jpg", ""),
                "image_url": "http://ahmadghizzawi.me/new-pics/"
                + str(filename),
            }
        )
