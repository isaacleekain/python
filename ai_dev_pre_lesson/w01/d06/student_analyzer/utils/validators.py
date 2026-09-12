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
    