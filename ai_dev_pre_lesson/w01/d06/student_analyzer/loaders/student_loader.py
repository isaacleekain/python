import json


def load_students(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data