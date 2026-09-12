# student_analyzer/utils/loaders.py
import json

from ..models.student import Student, InvalidScoreError

# q51
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
# q52
# type(data) 是list
# type(data[0]) 是dict

def load_students(path):
    json_data = load_json(path)


    # q54
    students = []
    for i in json_data:
        try:
            # q53
            student = Student(**i)
        except TypeError as e:
            # q56
            print(e)
            continue
        except InvalidScoreError as e:
            print(e)
            continue
        students.append(student)
    return students