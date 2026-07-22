import os


def get_name_dict(data):
    return data.get("name")


def get_name_list_dict(data):
    return [i.get('name') for i in data]


def create_user(name, age=18):
    return {
        "name": name,
        "age": age
    }
    


def main():
    stu = [
        {'name': 'tom', 'age': 12},
        {'name': 'tom2', 'age': 14},
        {'name': 'tom3', 'age': 13},
    ]
    
    stu_name = get_name_list_dict(stu)
    print(stu_name)
    
    
    
if __name__ == "__main__":
    main()