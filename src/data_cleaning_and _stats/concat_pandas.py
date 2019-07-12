import csv
import glob
import pandas as pd

f = pd.read_csv("Taskers.csv")
f2 = pd.read_csv("essai.csv")

combined_csv = pd.concat([f, f2])

combined_csv.to_csv("Final_Taskers.csv", index=False)
"""
a = pd.read_csv("taskrabbit_users_labelled.csv")
b = pd.read_csv("taskrabbit_labelled.csv")
b = b.dropna(axis=1)

merged = a.merge(b, on='Gender')
merged.to_csv("output.csv", index=False)
"""
