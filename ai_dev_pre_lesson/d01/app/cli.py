import os
import sys
import json
import uuid6
import yaml
from datetime import datetime
from app.setting import WORKSPACE_ROOT, JSON_PATH, JSON_INITIAL_DATA, UTC_PLUS_8


def yaml_load(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

    
FORMAT_VALIDATION_YAML = yaml_load(WORKSPACE_ROOT / "ai_dev_pre_lesson/d01/configs/validation.yaml")["format"]
NAME_MAPPING = {
    "user_name": "用户名",
    "password": "密码",
    "role": "角色",
    "category": "分类",
    "category_name": "分类名",
    "account": "账户",
    "account_name": "账户名",
    "account_type": "账户类型",
    "account_type_name": "账户类型名",
    "direction": "交易类型",
    "amount": "金额",
    "transaction_account": "交易账户"
}

ERROR_RANGE_MAPPING = {
    "role": "无效的角色, 输入角色(0=管理员,1=辅助管理员,2=用户): ",
    "category_type": "无效的分类类型, 输入分类类型(0=支出,1=收入): ",
    "amount": "金额不能小于0, 输入金额: "
}


def initial_data_files():
    for json_file in list(JSON_INITIAL_DATA.keys()):
        if not os.path.exists(JSON_PATH[json_file]):
            print(f"Not Found {json_file}.json at {JSON_PATH[json_file]}")
            with open(JSON_PATH[json_file], "w") as f:
                json.dump(JSON_INITIAL_DATA[json_file], f, indent=4, ensure_ascii=False)
                print(f"Created {json_file}.json at {JSON_PATH[json_file]}")


def initial_application_setup():
    user_path = JSON_PATH["user"]
    with open(user_path, "r") as f:
        admin_user_contents = json.load(f)[0]
        admin_user = admin_user_contents["name"]
        admin_password = admin_user_contents["password"]
    user_input = input("输入管理员用户名: ")
    password_input = input("输入管理员密码: ")
    for i in range(3):
        if user_input == admin_user and password_input == admin_password:
            print("管理员登录成功.")
            break
        else:
            print("管理员登录失败, 请检查用户名和密码。")
            if i < 2:
                user_input = input("输入管理员用户名: ")
                password_input = input("输入管理员密码: ")
            else:
                print("管理员登录失败, 请检查用户名和密码：")
                sys.exit()
    add_user(admin_user_contents)

def login():
    user_input = input("请输入用户名: ")
    with open(JSON_PATH["user"], "r") as f:
        users = json.load(f)
        user_dict = {user["name"]: user for user in users}
    while True:
        if user_input not in user_dict:
            user_input = input("用户名不存在, 请重新输入: ")
        else:
            break
    password_input = input("请输入密码: ")
    while True:
        if password_input != user_dict[user_input]["password"]:
            password_input = input("密码错误, 请重新输入: ")
        else:
            break
    print("登录成功. 登陆用户: ", user_input)
    user = user_dict[user_input]
    # save_cache = input("是否保存登陆状态(0=保存, 1=不保存)")
    # if save_cache =="0":
    #     data = {
    #         "user": user,
    #         "local": True
    #     }
    #     with open(JSON_PATH["user"], "w") as f:
    #         json.dump(data, f, indent=4, ensure_ascii=False)
    
    return user


def format_validation(input_content, table, content):
    validation_contents = FORMAT_VALIDATION_YAML[table][content]
    if validation_contents["required"]:
        input_content = required_format_validation(input_content, content)
    if "digits" in validation_contents:
        input_content = digits_format_validation(input_content, content, validation_contents["digits"])
    if "range" in validation_contents:
        input_content = range_format_validation(input_content, content, validation_contents["range"])
    return input_content

def required_format_validation(input_content, content):
    while True:
        if not input_content:
            input_content = input(f"{NAME_MAPPING[content]}不能为空, 请输入有效的{NAME_MAPPING[content]}: ")
        else:
            return input_content
            
def digits_format_validation(input_content, content, validation_contents_digits):
    while True:
        if len(input_content) < validation_contents_digits[0] or len(input_content) > validation_contents_digits[1]:
            input_content = input(f"{NAME_MAPPING[content]}必须在{validation_contents_digits[0]}-{validation_contents_digits[1]}之间, 请输入有效的{NAME_MAPPING[content]}: ")
        else:
            return input_content
        
def range_format_validation(input_content, content, validation_contents_range):
    if "select" in validation_contents_range:
        while True:
            if input_content not in validation_contents_range["select"]:
                input_content = input(ERROR_RANGE_MAPPING[content])
            else:
                break
    if "min" in validation_contents_range:
        while True:
            if float(input_content) < validation_contents_range["min"]:
                input_content = input(ERROR_RANGE_MAPPING[content])
            else:
                break
    return input_content

     
def connect_range_validation(input_content, exist_list, content, error_msg):
    while True:
        if input_content not in exist_list:
            input_content = input(f"不存在该{NAME_MAPPING[content]}, 重新输入({error_msg}): ")
        else:
            break
    return input_content
        
        
def existing_validation(input_content, exist_contents, content):
    while True:
        if input_content in exist_contents:
            print(f"{NAME_MAPPING[content]}已存在, 请输入其他{NAME_MAPPING[content]}.")
            input_content = input(f"请输入{NAME_MAPPING[content]}: ")
        else:
            break
    return input_content


def connect_validation(exist_connect, content):
    if content == "role":
        exist_msg = {str(i):v for i,v in enumerate(exist_connect) if i > 0}
    else:    
        exist_msg = {str(i+1):v for i,v in enumerate(exist_connect)}
    print_msg = "".join([f"{i}.{v['name']}" for i,v in exist_msg.items()])
    print(print_msg)
    input_content = input(f"输入{NAME_MAPPING[content]}: ")
    input_content = connect_range_validation(input_content, list(exist_msg.keys()), content, print_msg)
    return exist_msg[input_content]["code"] if content in ["role", "direction"] else exist_msg[input_content]["id"]
    
      
def add_user(user_login):
    add_type = "user"
    if user_login["role_code"] in ["user", "guest"]:
        print(f"只有管理员可以添加用户. 当前登录用户: {user_login['role_code']}")
        return
    users = json_load(JSON_PATH["user"])
    roles = json_load(JSON_PATH["role"])
    users_names = [user["name"] for user in users]
    user_name_add = input("输入用户名: ")
    user_name = format_validation(user_name_add, add_type, "user_name")
    user_name = existing_validation(user_name, users_names, "user_name")
    password_add = input("输入密码: ")
    password = format_validation(password_add, add_type, "password")
    role_add = connect_validation(roles, "role")
    users.append(
        {
            "id": str(uuid6.uuid7()),
            "name": user_name,
            "password": password,
            "role_code": role_add,
            "created_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
            "created_by": user_login["id"],
            "updated_by": user_login["id"],
            "is_deleted": False
        }
    )
    save_add(JSON_PATH["user"], users, "用户")


def add_category(user_login):
    add_type = "category"
    
    directions = json_load(JSON_PATH["direction"])
    categories = json_load(JSON_PATH["category"])
    
    category_name_add = input("输入分类名: ")
    category_name = format_validation(category_name_add, add_type, "category_name")
    category_names = [category["name"] for category in categories]
    category_name = existing_validation(category_name, category_names, "category_name")
    direction_add = connect_validation(directions, "direction")
    categories.append(
        {
            "id": str(uuid6.uuid7()),
            "user_id": user_login["id"],
            "name": category_name,
            "direction_code": direction_add,
            "created_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
            "created_by": user_login["id"],
            "updated_by": user_login["id"],
            "is_deleted": False,
            "is_default": False
        }
    )
    save_add(JSON_PATH["category"], categories, "分类")


def add_account_type(user_login):
    add_type = "account_type"
    
    account_types = json_load(JSON_PATH["account_type"])
    
    account_type_name_add = input("输入账户类型名: ")
    account_type_name = format_validation(account_type_name_add, add_type, "account_type_name")
    account_type_names = [account_type["name"] for account_type in account_types]
    account_type_name = existing_validation(account_type_name, account_type_names, "account_type_name")
    account_types.append(
        {
            "id": str(uuid6.uuid7()),
            "user_id": user_login["id"],
            "name": account_type_name,
            "created_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
            "created_by": user_login["id"],
            "updated_by": user_login["id"],
            "is_deleted": False,
            "is_default": False
        }
    )
    save_add(JSON_PATH["account_type"], account_types, "账户类型")


def add_account(user_login):
    add_type = "account"
    
    account_types = json_load(JSON_PATH["account_type"])
    accounts = json_load(JSON_PATH["account"])
    
    account_add = input("输入账户名: ")
    account = format_validation(account_add, add_type, "account_name")
    accounts_names = [account["name"] for account in accounts]
    account = existing_validation(account, accounts_names, "account_name")
    account_type_add = connect_validation(account_types, "account_type")
    accounts.append(
        {
            "id": str(uuid6.uuid7()),
            "user_id": user_login["id"],
            "name": account,
            "account_type_id": account_type_add,
            "created_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
            "created_by": user_login["id"],
            "updated_by": user_login["id"],
            "is_deleted": False,
            "is_default": False
        }
    )
    save_add(JSON_PATH["account"], accounts, "账户")


def add_transaction(user_login):
    add_type = "transaction"
    
    accounts = json_load(JSON_PATH["account"])
    directions = json_load(JSON_PATH["direction"])
    categories = json_load(JSON_PATH["category"])
    transactions = json_load(JSON_PATH["transaction"])
    
    transaction_id = str(uuid6.uuid7())
    date_input = input("输入交易日期(用'-'间隔年月日, 直接回车默认今天): ")
    date = date_validation(date_input)
    time_input = input("输入交易时间(用':'间隔时分秒, 直接回车默认现在): ")
    time = time_validation(time_input)
    amount_input = input("输入交易金额: ")
    amount = format_validation(amount_input, add_type, "amount")
    account_add = connect_validation(accounts, "account")
    direction_add = connect_validation(directions, "direction")
    category_add = connect_validation(categories, "category")
    note = input("输入备注: ").strip()
    transactions.append(
        {
            "id": transaction_id,
            "date": date,
            "time": time,
            "amount": amount,
            "direction_code": direction_add,
            "account_id": account_add,
            "category_id": category_add,
            "note": note,
            "created_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
            "created_by": user_login["id"],
            "updated_by": user_login["id"],
            "is_deleted": False,
            "is_default": False
        }
    )
    save_add(JSON_PATH["transaction"], transactions, "交易")


def json_load(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data


def date_validation(date_input):
    while True:
        try:
            if not date_input:
                date = datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d")
                print(f"交易日期: {date}")
                return str(date)
            else:
                date = datetime.strptime(date_input, "%Y-%m-%d")
                print(f"交易日期: {date_input}")
                return date_input
        except ValueError:
            print(f"无效日期格式: {date_input}. 日期格式: 2000-01-01")
            date_input = input("输入交易日期(用'-'间隔年月日, 直接回车默认今天): ")


def time_validation(time_input):
    while True:
        try:
            if not time_input:
                time = datetime.now(UTC_PLUS_8).strftime("%H:%M:%S")
                print(f"交易时间: {time}")
                return str(time)
            else:
                time = datetime.strptime(time_input, "%H:%M:%S")
                print(f"交易时间: {time_input}")
                return time_input
        except ValueError:
            print(f"无效时间格式: {time_input}. 日期格式: 12:01:01")
            time_input = input("输入交易时间(用':'间隔时分秒, 直接回车默认现在): ")


def save_add(save_path, data, data_type):
    with open(save_path, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"{data_type} 保存成功.")


def delete_transaction(user_login):
    directions_map, categories_map, accounts_map = map_create()
    result = search_transaction(user_login)
    if not result:
        return False
    idx_map, data_sorted_filter = result
    input_idx = input("输入交易编号(0=返回上一级): ").strip()
    if input_idx == "0":
        return False
    data_del = [d for d in data_sorted_filter if d["id"] == idx_map[int(input_idx)]]
    data_save = [d for d in data_sorted_filter if d["id"] != idx_map[int(input_idx)]]
    save_add(JSON_PATH["transaction"], data_save, "删除交易")
    idx_map, data_sorted = data_print(idx_map, data_del, directions_map, categories_map)


def search_transaction(user_login):
    directions_map, categories_map, accounts_map = map_create()
    idx_map, data_sorted = show_all_transactions(user_login) 
    key_input = input("输入日期(0000=返回上一级)")
    if key_input == "0000":
        return False
    data_sorted_filter = [i for i in data_sorted if str(key_input) in f"{i['date'].split('-', 2)[0]} {i['date'].split('-', 2)[1]} {i['date'].split('-', 2)[2]}"]
    
    idx_map, data_sorted = data_print(idx_map, data_sorted_filter, directions_map, categories_map)
    return idx_map, data_sorted_filter


def map_create():
    directions = json_load(JSON_PATH["direction"])
    directions_map = {k["code"]:k["name"] for k in directions}
    categories = json_load(JSON_PATH["category"])
    categories_map = {k["id"]:k["name"] for k in categories}
    accounts = json_load(JSON_PATH["account"])
    accounts_map = {k["id"]:k["name"] for k in accounts}
    return directions_map, categories_map, accounts_map


def show_ranking(user_login):
    directions_map, categories_map, accounts_map = map_create()
    idx_map, data_sorted = show_all_transactions(user_login)
    
    sorted_key = input("输入排序项目(0=返回上一级, 1=日期时间, 2=金额, 3=创建时间)")
    if sorted_key == "0":
        return False
    if sorted_key == "1":
        idx_map, data_sorted = data_print(idx_map, data_sorted, directions_map, categories_map)
        return True
    elif sorted_key == "2":
        data_sorted = sorted(data_sorted, key=lambda x: x["amount"], reverse=True)
        idx_map, data_sorted = data_print(idx_map, data_sorted, directions_map, categories_map)
        return True
    elif sorted_key == "3":
        data_sorted = sorted(data_sorted, key=lambda x: x["created_at"], reverse=True)
        idx_map, data_sorted = data_print(idx_map, data_sorted, directions_map, categories_map)
        return True
            

def show_statistics(user_login):
    directions_map, categories_map, accounts_map = map_create()
    idx_map, data_sorted = show_all_transactions(user_login)
    max_money = max(data_sorted, key=lambda x: x["amount"])
    min_money = min(data_sorted, key=lambda x: x["amount"])
    avg_money = int(round(sum(int(d["amount"]) for d in data_sorted) / len(data_sorted),0))
    over_money = 1000
    over_sorted = [d for d in data_sorted if int(d["amount"]) >= over_money]
    print(f"最大交易金额: {max_money['amount']}")
    max_money_sorted = [i for i in data_sorted if i['amount'] == max_money['amount']]
    data_print(idx_map, max_money_sorted, directions_map, categories_map)
    print(f"最小交易金额: {min_money['amount']}")
    min_money_sorted = [i for i in data_sorted if i['amount'] == min_money['amount']]
    data_print(idx_map, min_money_sorted, directions_map, categories_map)
    print(f"平均交易金额: {avg_money}")
    print(f"超过{over_money}金额计数: {len(over_sorted)}笔")
    data_print(idx_map, over_sorted, directions_map, categories_map)


def show_all_transactions(user_login):
    transactions = json_load(JSON_PATH["transaction"])
    data_filter = [i for i in transactions if i["created_by"] == user_login["id"]]
    data_sorted = sorted(
        data_filter,
        key=lambda x: datetime.strptime(
            f"{x['date']} {x['time']}", 
            "%Y-%m-%d %H:%M:%S"
        )
    )
    idx_map = {}
    for idx, i in enumerate(data_sorted):
        idx_map[idx+1] = i['id']
    return idx_map, data_sorted
            
            
def show_all_transactions_print(user_login):
    directions_map, categories_map, accounts_map = map_create()
    transactions = json_load(JSON_PATH["transaction"])
    data_filter = [i for i in transactions if i["created_by"] == user_login["id"]]
    data_sorted = sorted(
        data_filter,
        key=lambda x: datetime.strptime(
            f"{x['date']} {x['time']}", 
            "%Y-%m-%d %H:%M:%S"
        )
    )
    idx_map = {}
    idx_map, data_sorted = data_print(idx_map, data_sorted, directions_map, categories_map)
    return idx_map, data_sorted


def data_print(idx_map, data_sorted, directions_map, categories_map):
    for idx, i in enumerate(data_sorted):
        idx_map[idx+1] = i['id']
        print(f"{idx+1}. 交易日期:{i['date']} 交易时间:{i['time']} 交易类型:{directions_map[i['direction_code']]} 交易分类:{categories_map[i['category_id']]} 交易金额:{i['amount']} 创建时间:{i['created_at']}")
    return idx_map, data_sorted

def main():
    initial_data_files()
    with open(JSON_PATH["user"], "r") as f:
        users = json.load(f)
        if len(users) == 1 and users[0]["name"] == "admin":
            initial_application_setup()
            print("非管理员用户已创建, 请重新运行程序以登录.")
            sys.exit()
    user_login = login()
    while True:
        method = input("请输入要做什么 (1=添加, 2=删除, 3=搜索, 4=排名, 5=统计, 6=显示): ")
        if method == "1":
            method_1_flag = True
            while method_1_flag:
                method_2nd = input("请输入要添加什么 (1=用户, 2=分类, 3=账户, 4=账户类型, 5=交易, 0=返回): ")
                if method_2nd == "1":
                    add_user(user_login)
                elif method_2nd == "2":
                    add_category(user_login)
                elif method_2nd == "3":
                    add_account(user_login)
                elif method_2nd == "4":
                    add_account_type(user_login)
                elif method_2nd == "5":
                    add_transaction(user_login)
                elif method_2nd == "0":
                    break
        elif method == "2":
            method_2_flag = True
            while method_2_flag:
                method_2_flag = delete_transaction(user_login)
                if not method_2_flag:
                    break
        elif method == "3":
            method_3_flag = True
            while method_3_flag:
                method_3_flag = search_transaction(user_login)
                if not method_3_flag:
                    break
        elif method == "4":
            method_4_flag = True
            while method_4_flag:
                method_4_flag = show_ranking(user_login)
                if not method_4_flag:
                    break
        elif method == "5":
            method_5_flag = True
            while method_5_flag:
                method_5_flag = show_statistics(user_login)
                if not method_5_flag:
                    break
        elif method == "6":
            show_all_transactions_print(user_login)
        elif method == "exit":
            sys.exit()
    
if __name__ == "__main__":
    main()