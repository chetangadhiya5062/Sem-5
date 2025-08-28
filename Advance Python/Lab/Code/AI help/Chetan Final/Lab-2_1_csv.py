import csv

dir = "files/program_1"


with open(f"{dir}/input.csv", "r", newline="") as input:
    reader = csv.DictReader(input)
    rows = []

    for row in reader:
        scores = [float(row[col]) for col in row if col != "Name"]
        avg = sum(scores) / len(scores)
        rows.append({"Name": row["Name"], "Average": avg})


with open(f"{dir}/output.csv", "w", newline="") as outfile:
    fieldnames = ["Name", "Average"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
