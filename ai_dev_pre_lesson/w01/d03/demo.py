q1
re.fullmatch(r"[A-Z]{2}-\d{8}", code)

q2
match = re.fullmatch(r"([A-Z]+)-(\d{8})-(\d{4})", text)
prefix, date, number = match.groups()

q3
match = re.findall(r"([A-Za-Z]+)=(\d+)", text)

q4
def filter_user(data, user):
    user = user.lower()
    result = []

    for log in data:
        if log["user"].lower() == user:
            result.append(log)

    return result