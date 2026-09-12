import json
import csv
from pathlib import Path


BASE_PATH = Path("/workspace/ai_dev_pre_lesson/d04")

def load_students(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


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


def merge_data(students, bonus_data):
    data = []
    for student in students:
        # for bonus in bonus_data:
        #     if student["name"] == bonus["name"]:
        #         student["bonus"] = bonus["bonus"]
                student["bonus"] = bonus_data[student["name"]]
                student["final_score"] = student["bonus"] + student["score"]
                student["passed"] =  student["final_score"] >= 60
                data.append(student)
                continue
    return data

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        

def save_csv(data, path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0]))
        writer.writeheader()
        writer.writerows(data)
    
    
def main():
    students_path = BASE_PATH / "data/students.json"
    bonus_path = BASE_PATH / "data/bonus.csv"
    result_json_path = BASE_PATH / "output/result.json"
    result_csv_path = BASE_PATH / "output/result.csv"
    students = load_students(students_path)
    bonus = load_bonus(bonus_path)
    data = merge_data(students, bonus)
    save_json(data, result_json_path)
    save_csv(data, result_csv_path)

if __name__ == "__main__":
    main()