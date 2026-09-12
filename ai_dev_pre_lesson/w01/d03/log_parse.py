import re
import json

def parse_logs(data):
    data_list = re.findall(r"\[(INFO|ERROR|WARN)\] user=(\w+) action=(\w+) duration=(\d+)", data)
    result = []
    for level, user, action, duration in data_list:
        result.append({
            "level": level,
            "user": user,
            "action": action,
            "duration": int(duration),
            })
    return result


def count_levels(data):
    result = {}
    for log in data:
        result[log["level"]] = result.get(log["level"], 0) + 1
    return result
        
   
def count_users(data):
    result = {}
    for log in data:
        result[log["user"]] = result.get(log["user"], 0) + 1
    return result
     
     
def get_duration_stats(data):
    result = {
        "total": 0,
        "average": None,
        "max": None,
        "min": None
    }
    count = 0
    if data:
        for log in data:
            if count == 0:
                result["total"] = log["duration"]
                result["max"] = log["duration"]
                result["min"] = log["duration"]
            else:
                result["total"] += log["duration"]
                result["max"] = log["duration"] if result["max"] < log["duration"] else result["max"]
                result["min"] = log["duration"] if result["min"] > log["duration"] else result["min"]
            count += 1
        result["average"] = result["total"] / count
    return result


def get_user_duration_stats(data):
    result = {}
    if data:
        for log in data:
            if log["user"] not in result:
                result[log["user"]] = {
                    "count": 0,
                    "total_duration": 0
                }
            result[log["user"]]["count"] = result[log["user"]]["count"] + 1
            result[log["user"]]["total_duration"] = result[log["user"]]["total_duration"] + log["duration"]
        for k,v in result.items():
            v["average_duration"] = v["total_duration"] / v["count"]
    return result


def get_slowest_log(data):
    if not data:
        return None
    result = data[0]
    for log in data:
        if result["duration"] < log["duration"]:
            result = log      
    return result


def filter_slow_logs(data, threshold=500):
    result = []
    for log in data:
        if log["duration"] >= threshold:
            result.append(log)
    return result


def filter_logs_by_level(data, level):
    target_level = level.lower()
    result = []
    for log in data:
        if log["level"].lower() == target_level:
            result.append(log)
    return result


def filter_logs_by_user(data, user):
    target_user = user.lower()
    result = []
    for log in data:
        if log["user"].lower() == target_user:
            result.append(log)
    return result


def filter_logs(data, **kwarg):
    result = data
    for filter_key, filter_value in kwarg.items():
        result = []
        if filter_key in ["user", "level"]:
            filter_value_target = filter_value.lower()
        for log in data:
            if filter_value is None:
                result.append(log)
            elif filter_key == "level":
                if log["level"].lower() == filter_value_target:
                    result.append(log)
            elif filter_key == "user":
                if log["user"].lower() == filter_value_target:
                    result.append(log)
            elif filter_key == "min_duration":
                if log["duration"] >= filter_value:
                    result.append(log)
        data = result
    return result


logs = """
[INFO] user=Tom action=login duration=120
[ERROR] user=Lucy action=query duration=850
[INFO] user=Tom action=query duration=230
[WARN] user=Jack action=upload duration=510
[ERROR] user=Tom action=download duration=920
[INFO] user=Lucy action=logout duration=80
"""

parse_logs_data = parse_logs(logs)
level_data = count_levels(parse_logs_data)
users_data = count_users(parse_logs_data)
duration_stats_data = get_duration_stats(parse_logs_data)
user_duration_stats_data = get_user_duration_stats(parse_logs_data)
slowest_log_data = get_slowest_log(parse_logs_data)
slow_logs_data = filter_slow_logs(parse_logs_data, 500)
logs_by_level_data = filter_logs_by_level(parse_logs_data, "info")
logs_by_user_data = filter_logs_by_user(parse_logs_data, "tom")
filter_logs_data = filter_logs(parse_logs_data, level="info", user="tom", min_duration=200)
# print(json.dumps(parse_logs_data, indent=2))
# print(json.dumps(level_data, indent=2))
# print(json.dumps(users_data, indent=2))
# print(json.dumps(duration_stats_data, indent=2))
# print(json.dumps(user_duration_stats_data, indent=2))
# print(json.dumps(slowest_log_data, indent=2))
# print(json.dumps(slow_logs_data, indent=2))
# print(json.dumps(logs_by_level_data, indent=2))
# print(json.dumps(logs_by_user_data, indent=2))
print(json.dumps(filter_logs_data, indent=2))
