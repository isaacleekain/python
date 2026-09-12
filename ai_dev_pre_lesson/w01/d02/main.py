import ai_dev_pre_lesson.w01.d02.student_util as su

students = [
    {"name": "Tom", "score": 88},
    {"name": "Lucy", "score": 95},
    {"name": "Jack", "score": 58},
    {"name": "Bob", "score": 76},
]

def main():
    print(su.get_names(students))
    print(su.filter_students(students))
    print(su.get_top_student(students))
    print(su.get_average_score(students))


if __name__ == "__main__":
    main()