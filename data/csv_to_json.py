import csv
import json

# initially, categorize statements as
# * (I) can be law/important
# * (N) can't be law/not important
# * (L)eft
# * (R)ight
# * (C)enter

# select from 6 bins:

# IL, IR, L, R, IM, IM, M, M, any, any

probabilities = {
    "YL": 0.1,
    "YR": 0.1,
    "*L": 0.1,
    "*R": 0.1,
    "YM": 0.2,
    "*M": 0.2,
    "**": 0.2,
}

total = 0
for k, v in probabilities.items():
    total += v
if total != 1:
    raise Exception("Probabilities must add up to 1")

# Open the CSV file
with open('statements.csv', 'r') as csv_file:
    # Create a CSV reader object
    csv_reader = csv.reader(csv_file)

    # Iterate through the rows
    first = True
    data = []
    for row in csv_reader:
        if first:
            first = False
            headers = row
            continue
        # Each row is a list of values
        data.append(row)
        print(f"0: {row[0]}, 1: {row[1]}, 2: {row[2]}")

# Convert the data to a list of dictionaries
table_dict_data = [dict(zip(headers, row)) for row in data]

all_data = {
    "statements": table_dict_data,
    "probabilities": probabilities
}

# Convert the data to JSON
json_data = json.dumps(all_data, indent=2)  # Optional: 'indent' for pretty formatting

# Print the JSON data
print(json_data)

# Optionally, write the JSON data to a file
with open('statements.json', 'w') as json_file:
    json.dump(table_dict_data, json_file, indent=2)
