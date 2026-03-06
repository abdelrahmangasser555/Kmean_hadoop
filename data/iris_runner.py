import csv
input_file = "data/iris_raw.csv"
output_file = "data/iris.csv"

with open(input_file) as f, open(output_file,"w") as out:

    reader = csv.reader(f)

    for row in reader:

        if len(row) == 0:
            continue

        x = row[0]
        y = row[2]

        out.write(f"{x},{y}\n")