import json
import csv
from pathlib import Path
import sys

BASE_PATH = Path(__file__).parent


def load_students(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def validate_score(score):
    score = int(score)

    if score < 0 or score > 100:
        raise ValueError("score must be between 0 and 100")

    return score


def process_students(students):
    data = []

    for student in students:
        try:
            score = validate_score(student["score"])

        except KeyError as e:
            print(f"缺少字段 score: {e}")
            continue

        except ValueError as e:
            print(f"score 数据错误: {e}")
            continue

        else:
            student["score"] = score
            data.append(student)

    if not data:
        raise ValueError("没有正常数据")

    return data
    

def main():
    students_path = BASE_PATH / "data/students.json"
    print(students_path)
    try:
        students_data = load_students(students_path)
    except FileNotFoundError:
        print(f"students.json not found: {students_path}")
        sys.exit()
    except json.JSONDecodeError as e:
        print(e)
        sys.exit()
    try:
        desposed_students_data = process_students(students_data)
    except IndexError as e:
        print(e)
        sys.exit()
    except ValueError as e:
        print(e)
        sys.exit()
    print(desposed_students_data)
    

if __name__ == "__main__":
    main()