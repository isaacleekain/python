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