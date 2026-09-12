def get_names(students):
    return [i["name"] for i in students]

def filter_students(students, min_score=60):
    return [i for i in students if i["score"] >= min_score]

def get_top_student(students):
    return max(students, key=lambda x: x["score"])

def get_average_score(students):
    return sum(i["score"] for i in students) / len(students)