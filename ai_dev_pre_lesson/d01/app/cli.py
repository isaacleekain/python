import os
import sys
import json
import uuid
from datetime import datetime
from setting import WORKSPACE_ROOT, JSON_PATH, JSON_INITIAL_DATA, UTC_PLUS_8





def user_validation(user_input):
    while True:
        if user_input in VALIDATION_USER:
            print(f"Username: {user_input}")
            return user_input
        else:
            print("Invalid username. Please enter a valid username.")
            user_input = input("Enter your username: ")
            

def password_validation(user_input, password_input):
    while True:
        if password_input == VALIDATION_USER[user_input]["password"]:
            print("Password validated successfully.")
            return
        else:
            print("Invalid password. Please try again.")
            password_input = input("Enter your password: ")


def date_validation(date_input):
    while True:
        try:
            if not date_input:
                date = datetime.now(UTC_PLUS_9).strftime("%Y-%m-%d")
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
                time = datetime.now(UTC_PLUS_9).strftime("%H:%M:%S")
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


def save_transaction(json_path, transaction):
    with open(json_path, "w") as f:
        json.dump(transaction, f, indent=4, ensure_ascii=False)
    print("Transaction saved successfully.")


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
        created_at = datetime.now(UTC_PLUS_9).strftime("%Y-%m-%d %H:%M:%S")
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
    save_transaction(json_path, transactions)


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
    for json_file in list(JSON_INITIAL_DATA.keys()):
        if not os.path.exists(JSON_PATH[json_file]):
            print(f"Not Found {json_file}.json at {JSON_PATH[json_file]}")
            with open(JSON_PATH[json_file], "w") as f:
                json.dump(JSON_INITIAL_DATA[json_file], f, indent=4)
                print(f"Created {json_file}.json at {JSON_PATH[json_file]}")
    user_input = input("Enter your username: ")
    user = user_validation(user_input)
    password_input = input("Enter your password: ")
    password_validation(user, password_input)
    while True:
        method = input("Enter method (add, del, search, rank, statis, show): ")
        if method == "add":
            add_transaction(transactions_json_path, user)
        elif method == "del":
            delete_transaction(transactions_json_path)
        elif method == "search":
            search_transaction(transactions_json_path)
        elif method == "rank":
            show_ranking(transactions_json_path)
        elif method == "statis":    
            show_statistics(transactions_json_path)
        elif method == "show":
            show_all_transactions(transactions_json_path)
        elif method == "exit":
            sys.exit()
    
if __name__ == "__main__":
    main()