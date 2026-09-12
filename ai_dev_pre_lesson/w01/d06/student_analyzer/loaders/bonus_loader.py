import csv


def load_bonus(path):
    # data = []
    data = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # row["bonus"] = int(row["bonus"])
            # data.append(row)
            data[row["name"]] = int(row["bonus"])
            
    return data