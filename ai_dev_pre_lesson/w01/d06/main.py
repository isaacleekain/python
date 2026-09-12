import json
import csv

from pathlib import Path

from ai_dev_pre_lesson.w01.d06.student_analyzer.utils.result_writer import save_csv, save_json
from ai_dev_pre_lesson.w01.d06.student_analyzer.utils.validators import process_students
from ai_dev_pre_lesson.w01.d06.student_analyzer.loaders.bonus_loader import load_bonus
from ai_dev_pre_lesson.w01.d06.student_analyzer.loaders.student_loader import load_students
from ai_dev_pre_lesson.w01.d06.student_analyzer.services.student_service import merge_data


BASE_PATH = Path("/workspace/ai_dev_pre_lesson/d06")

    
def main():
    students_path = BASE_PATH / "data/students.json"
    bonus_path = BASE_PATH / "data/bonus.csv"
    result_json_path = BASE_PATH / "output/result.json"
    result_csv_path = BASE_PATH / "output/result.csv"
    students = load_students(students_path)
    bonus = load_bonus(bonus_path)
    process_students_data = process_students(students)
    data = merge_data(process_students_data, bonus)
    save_json(data, result_json_path)
    save_csv(data, result_csv_path)

if __name__ == "__main__":
    main()