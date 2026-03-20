# Import libs
import pandas as pd
import matplotlib.pyplot as plt
import re


df = pd.read_csv('hr_project.csv')
df.sample(2)
# Remove spaces and turn every row to lower case for ease of access.
for cols in df.select_dtypes(include=["object", 'string']):
    df[cols] = df[cols].astype(str).str.strip().str.lower()
# add _ to the column names for better readability, then make lower case for ease of selection
df.columns = df.columns.str.replace(
    r'(?<!^)(?=[A-Z])', '_', regex=True).str.lower()
# drop duplicates
df = df.drop_duplicates()
