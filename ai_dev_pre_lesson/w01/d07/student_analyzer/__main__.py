# student_analyzer/__main__.py
from pathlib import Path
import sys
import json
# q60
# __main__
from .utils.loaders import load_students
from .services.analyzer import StudentAnalyzer

BASE_PATH = Path(__file__).parent

def main():
    try:
        students = load_students(BASE_PATH / "data/students.json")
    # q57
    # B，最上层决定
    except FileNotFoundError as e:
        print(e)
        sys.exit()
    # q58
    # KeyError
    except json.JSONDecodeError as e:
        print(e)
        sys.exit()
    student_analyzer = StudentAnalyzer(students)
    average_score = student_analyzer.get_average_score()
    print(f"average_score: {average_score}")
    top_student = student_analyzer.get_top_student()
    print(f"top_student: {top_student}")
    # q69
    passed_students = student_analyzer.get_passed_students()
    for passed_student in passed_students:
        print(f"{passed_student.name} - {passed_student.score} - {passed_student.get_grade()} ")
    print(f"passed_students: {passed_students}")
    student_by_name = student_analyzer.get_student_by_name("Tom")
    print(f"student_by_name: {student_by_name}")
    students_by_grade = student_analyzer.get_students_by_grade("A")
    print(f"students_by_grade: {students_by_grade}")
    

if __name__ == "__main__":
    main()