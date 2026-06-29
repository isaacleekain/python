import os
import sys
import json
from src.configs.config import WORKSPACE_ROOT


def add_student(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
        input_name = input("Enter student name: ").strip()
        input_name = input_name[0].upper() + input_name[1:].lower()
        input_score = input("Enter student score: ")
        data.append(
            {
                "name": input_name,
                "score": int(input_score)
            }
        )
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)

def delete_student(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
        input_name = input("Enter student name: ").strip()
        input_name = input_name[0].upper() + input_name[1:].lower()
        data_del = [d for d in data if d["name"] == input_name]
        data = [d for d in data if d["name"] != input_name]
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)
        print(f"Deleted student: {data_del}")

def search_student(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
        input_name = input("Enter student name: ").strip()
        input_name = input_name[0].upper() + input_name[1:].lower()
        for d in data:
            if d["name"] == input_name:
                print(f"Found student: {d['name']}, score: {d['score']}")

def show_ranking(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
        data_sorted = sorted(data, key=lambda x: x["score"], reverse=True)
        count = 1
        for d in data_sorted:
            print(f"Rank {count}: {d['name']}, score: {d['score']}")
            count += 1
            

def show_statistics(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
        max_score = max(data, key=lambda x: x["score"])
        min_score = min(data, key=lambda x: x["score"])
        avg_score = int(round(sum(d["score"] for d in data) / len(data),0))
        passed_score = 60
        passed_count = len([d for d in data if d["score"] >= passed_score])
        print(f"Max score: {max_score['score']} (Student: {max_score['name']})")
        print(f"Min score: {min_score['score']} (Student: {min_score['name']})")
        print(f"Average score: {avg_score}")
        print(f"Number of students who passed: {passed_count} (passed score: {passed_score} or above)")

def show_all_students(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
        for d in data:
            print(f"Student: {d['name']}, score: {d['score']}")
            
def main():
    json_path = WORKSPACE_ROOT / "ai_dev_pre_lesson/d01/data/input/data.json"
    if not os.path.exists(json_path):
        print(f"Found data.json at {json_path}")
        with open(json_path, "w") as f:
            json.dump([], f, indent=4)
    while True:
        method = input("Enter method (add, del, search, rank, statis, show): ")
        if method == "add":
            add_student(json_path)
        elif method == "del":
            delete_student(json_path)
        elif method == "search":
            search_student(json_path)
        elif method == "rank":
            show_ranking(json_path)
        elif method == "statis":    
            show_statistics(json_path)
        elif method == "show":
            show_all_students(json_path)
        elif method == "exit":
            sys.exit()
    
if __name__ == "__main__":
    main()