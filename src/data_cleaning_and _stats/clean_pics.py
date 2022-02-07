import csv
import os


with open("taskrabbit_users_labelled.csv") as f:
    csv_reader = csv.reader(f, delimiter=",")
    for row in csv_reader:
        file_path = "./pics/" + row[3] + ".jpg"
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print("Can not delete the file does not exist")
