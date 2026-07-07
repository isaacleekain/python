import os
import sys
import json
import uuid6
from datetime import datetime
from app.setting import WORKSPACE_ROOT, JSON_PATH, JSON_INITIAL_DATA, UTC_PLUS_8





def initial_data_files():
    json_path = {}
    for json_file in list(JSON_INITIAL_DATA.keys()):
        if not os.path.exists(JSON_PATH[json_file]):
            print(f"Not Found {json_file}.json at {JSON_PATH[json_file]}")
            with open(JSON_PATH[json_file], "w") as f:
                json.dump(JSON_INITIAL_DATA[json_file], f, indent=4)
                print(f"Created {json_file}.json at {JSON_PATH[json_file]}")
        json_path[json_file] = JSON_PATH[json_file]
    return json_path


def initial_application_setup(user_path):
    user_input = input("输入管理员用户名: ")
    password_input = input("输入管理员密码: ")
    for i in range(3):
        if user_input == "admin" and password_input == "admin":
            print("管理员登录成功.")
            break
        else:
            print("管理员登录失败. 请检查用户名和密码.")
            if i < 2:
                user_input = input("输入管理员用户名: ")
                password_input = input("输入管理员密码: ")
            else:
                print("管理员登录失败. 请检查用户名和密码.")
                sys.exit()
    role = 0
    
    add_user(user_path, role)

def login():
    user_input = input("请输入用户名: ")
    with open(JSON_PATH["user"], "r") as f:
        users = json.load(f)
        user_dict = {user["username"]: user for user in users}
    while True:
        if user_input not in user_dict:
            user_input = input("用户名不存在，请重新输入.")
        else:
            break
    password_input = input("请输入密码: ")
    while True:
        if password_input != user_dict[user_input]["password"]:
            password_input = input("密码错误，请重新输入.")
        else:
            break
    print("登录成功. 登陆用户: ", user_input)
    user = user_dict[user_input]
    return user

def format_validation_user(user_input):
    while True:
        if not user_input:
            user_input = input("用户名不能为空. 请输入有效的用户名: ")
        elif len(user_input) < 3 or len(user_input) > 20:
            user_input = input("用户名必须在3-20个字符之间. 请输入有效的用户名: ")
        else:
            break
    return user_input


def format_validation_password(password_input):
    while True:
        if not password_input:
            password_input = input("密码不能为空: ")
        elif len(password_input) < 8 or len(password_input) > 16:
            password_input = input("密码必须在8-16个字符之间: ")
        else:
            break
    return password_input


def format_validation_category(category_input):
    while True:
        if not category_input:
            category_input = input("分类名不能为空. 请输入有效的分类名: ")
        elif len(category_input) < 1 or len(category_input) > 20:
            category_input = input("分类名必须在1-20个字符之间. 请输入有效的分类名: ")
        else:
            break
    return category_input


def format_validation_role():
    while True:
        role_input = input("请输入用户角色 (0=管理员, 1=普通用户): ")
        if role_input not in ["0", "1"]:
            print("无效的角色. 请输入有效的角色 (0=管理员, 1=普通用户).")
        else:
            break
    return int(role_input)


def format_validation_type():
    type_dict = {}
    with open(JSON_PATH["account_type"], "r") as f:
        account_types = json.load(f)
        for i, account_type in enumerate(account_types, start=1):
            type_dict[str(i)] = account_type
            print(f"{i}. {account_type['name']}")
    type_input = input("请输入账户类型: ")
    while True:
        if type_input not in type_dict:
            type_input = input("无效的账户类型. 请输入有效的账户类型: ")
        else:
            break
    return type_dict[type_input]


def format_vali


def existing_validation_user(user_input, users_names):
    while True:
        if user_input in users_names:
            print("用户名已存在，请输入其他用户名.")
            user_input = input("请输入用户名: ")
        else:
            break
    return user_input
        
        
def existing_validation_category(category_input, categories_names):
    while True:
        if category_input in categories_names:
            print("分类名已存在，请输入其他分类名.")
            category_input = input("请输入分类名: ")
        else:
            break
    return category_input
        
        
def add_user(user_path, user_login):
    if user_login["role"] != 0:
        print("只有管理员可以添加用户.")
        return
    with open(user_path, "r") as f:
        users = json.load(f)
        users_names = [user["username"] for user in users]
        user_add = input("输入用户名: ")
        user = format_validation_user(user_add)
        user = existing_validation_user(user, users_names)
        password_add = input("输入密码: ")
        password = format_validation_password(password_add)
        role = format_validation_role()
        users.append(
            {
                "id": str(uuid6.uuid7()),
                "username": user,
                "password": password,
                "role": role,
                "created_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
                "created_by": user_login["username"],
                "updated_by": user_login["username"],
                "is_deleted": False
            }
        )
    save_add(user_path, users, "用户")


def add_category(category_path, user_login):
    with open(category_path, "r") as f:
        categories = json.load(f)
        category_add = input("输入分类名: ")
        category = format_validation_category(category_add)
        categories_names = [category["name"] for category in categories]
        category = existing_validation_category(category, categories_names)
        categories.append(
            {
                "id": str(uuid6.uuid7()),
                "user_id": user_login["id"],
                "name": category,
                "type": "支出",
                "created_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
                "created_by": user_login["username"],
                "updated_by": user_login["username"],
                "is_deleted": False,
                "is_default": False
            }
        )
    save_add(category_path, categories, "分类")


def add_account(account_path, user_login):
    with open(account_path, "r") as f:
        accounts = json.load(f)
        account_add = input("输入账户名: ")
        account = format_validation_account(account_add)
        accounts_names = [account["name"] for account in accounts]
        account = existing_validation_account(account, accounts_names)
        type_input = format_validation_type()
        accounts.append(
            {
                "id": str(uuid6.uuid7()),
                "user_id": user_login["id"],
                "name": account,
                "account_type_id": type_input,
                "created_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
                "created_by": user_login["username"],
                "updated_by": user_login["username"],
                "is_deleted": False,
                "is_default": False
            }
        )
    save_add(account_path, accounts, "账户")


def add_account_type(account_type_path, user_login):
    with open(account_type_path, "r") as f:
        account_types = json.load(f)
        type_add = input("输入账户类型名: ")
        type_name = format_validation_account_type(type_add)
        types_names = [account_type["name"] for account_type in account_types]
        type_name = existing_validation_account_type(type_name, types_names)
        account_types.append(
            {
                "id": str(uuid6.uuid7()),
                "user_id": user_login["id"],
                "name": type_name,
                "created_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S"),
                "created_by": user_login["username"],
                "updated_by": user_login["username"],
                "is_deleted": False,
                "is_default": False
            }
        )
    save_add(account_type_path, account_types, "账户类型")


def date_validation(date_input):
    while True:
        try:
            if not date_input:
                date = datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d")
                print(f"Transaction date: {date}")
                return str(date)
            else:
                date = datetime.strptime(date_input, "%Y-%m-%d")
                print(f"Transaction date: {date_input}")
                return date_input
        except ValueError:
            print(f"Invalid date format: {date_input}. Please use YYYY-MM-DD.")
            date_input = input("Enter transaction datetime(seperate by '-', default today): ")


def time_validation(time_input):
    while True:
        try:
            if not time_input:
                time = datetime.now(UTC_PLUS_8).strftime("%H:%M:%S")
                print(f"Transaction time: {time}")
                return str(time)
            else:
                time = datetime.strptime(time_input, "%H:%M:%S")
                print(f"Transaction time: {time_input}")
                return time_input
        except ValueError:
            print(f"Invalid time format: {time_input}. Please use HH:MM:SS.")
            time_input = input("Enter transaction time(seperate by ':', default now): ")


def amount_validation(expense_amount_input):
    while True:
        try:
            expense_amount = float(expense_amount_input)
            if expense_amount < 0:
                raise ValueError("Amount cannot be negative.")
            print(f"Transaction amount: {expense_amount}")
            return expense_amount
        except ValueError as e:
            print(f"Invalid amount: {e}. Please enter a valid number.")
            expense_amount_input = input("Enter transaction amount: ")


def account_validation(payment_account_input):
    payment_account_input = payment_account_input[0].upper() + payment_account_input[1:].lower()
    while True:
        if payment_account_input in ACCOUNT:
            print(f"Transaction account: {payment_account_input}")
            return payment_account_input
        else:
            print(f"Invalid account: {payment_account_input}. Please choose from: {', '.join(ACCOUNT)}")
            payment_account_input = input("Enter transaction account: ")


def category_validation(expense_category_input):
    expense_category_input = expense_category_input[0].upper() + expense_category_input[1:].lower()
    while True:
        if expense_category_input in CATEGORY:
            print(f"Transaction category: {expense_category_input}")
            return expense_category_input
        else:
            print(f"Invalid category: {expense_category_input}. Please choose from: {', '.join(CATEGORY)}")
            expense_category_input = input("Enter transaction category: ")


def save_add(json_path, data, data_type):
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"{data_type} 保存成功.")


def add_transaction(json_path, user):
    with open(json_path, "r") as f:
        transactions = json.load(f)
        transaction_id = str(uuid.uuid4())
        date_input = input("Enter transaction datetime(seperate by '-', default today): ")
        date = date_validation(date_input)
        time_input = input("Enter transaction time(seperate by ':', default now): ")
        time = time_validation(time_input)
        expense_amount_input = input("Enter transaction amount: ")
        expense_amount = amount_validation(expense_amount_input)
        print(f"Available accounts: {', '.join(ACCOUNT)}")
        payment_account_input = input("Enter transaction account: ")
        payment_account = account_validation(payment_account_input)
        print(f"Available categories: {', '.join(CATEGORY)}")
        expense_category_input = input("Enter transaction category: ")
        expense_category = category_validation(expense_category_input)
        note = input("Enter transaction Note: ").strip()
        created_at = datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S")
        created_by = user
        transactions.append(
            {
                "id": transaction_id,
                "date": date,
                "time": time,
                "expense_amount": expense_amount,
                "payment_account": payment_account,
                "expense_category": expense_category,
                "note": note,
                "created_at": created_at,
                "created_by": created_by
            }
        )
    save_add(json_path, transactions)


def delete_transaction(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
        input_name = input("Enter transaction name: ").strip()
        input_name = input_name[0].upper() + input_name[1:].lower()
        data_del = [d for d in data if d["name"] == input_name]
        data = [d for d in data if d["name"] != input_name]
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)
        print(f"Deleted transaction: {data_del}")


def search_transaction(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
        input_name = input("Enter transaction name: ").strip()
        input_name = input_name[0].upper() + input_name[1:].lower()
        for d in data:
            if d["name"] == input_name:
                print(f"Found transaction: {d['name']}, score: {d['score']}")


def show_ranking(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
        data_sorted = sorted(data, key=lambda x: x["score"], reverse=True)
        count = 1
        for d in data_sorted:
            print(f"Rank {count}: {d['name']}, score: {d['score']}")
            count += 1
            

def show_statistics(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
        max_score = max(data, key=lambda x: x["score"])
        min_score = min(data, key=lambda x: x["score"])
        avg_score = int(round(sum(d["score"] for d in data) / len(data),0))
        passed_score = 60
        passed_count = len([d for d in data if d["score"] >= passed_score])
        print(f"Max score: {max_score['score']} (transaction: {max_score['name']})")
        print(f"Min score: {min_score['score']} (transaction: {min_score['name']})")
        print(f"Average score: {avg_score}")
        print(f"Number of transactions who passed: {passed_count} (passed score: {passed_score} or above)")


def show_all_transactions(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
        for d in data:
            print(d)
            
            
def main():
    json_path = initial_data_files()
    with open(JSON_PATH["user"], "r") as f:
        users = json.load(f)
        if len(users) == 1 and users[0]["username"] == "admin":
            initial_application_setup(json_path["user"])
            print("非管理员用户已创建，请重新运行程序以登录.")
            sys.exit()
    user_login = login()
    while True:
        method = input("请输入要做什么 (1=添加, 2=删除, 3=搜索, 4=排名, 5=统计, 6=显示): ")
        if method == "1":
            method_2nd = input("请输入要添加什么 (1=用户, 2=分类, 3=账户, 4=账户类型, 5=交易): ")
            if method_2nd == "1":
                add_user(json_path["user"], user_login)
            elif method_2nd == "2":
                add_category(json_path["category"], user_login)
            elif method_2nd == "3":
                add_account(json_path["account"], json_path["account_type"], user_login)
            elif method_2nd == "4":
                add_account_type(json_path["account_type"], user_login)
            elif method_2nd == "5":
                add_transaction(json_path["transaction"], user_login)
        elif method == "2":
            delete_transaction(json_path["transaction"])
        elif method == "3":
            search_transaction(json_path["transaction"])
        elif method == "4":
            show_ranking(json_path["transaction"])
        elif method == "5":
            show_statistics(json_path["transaction"])
        elif method == "6":
            show_all_transactions(json_path["transaction"])
        elif method == "exit":
            sys.exit()
    
if __name__ == "__main__":
    main()