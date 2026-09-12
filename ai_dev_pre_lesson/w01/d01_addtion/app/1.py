a = [
    {
        "code": "transfer",
        "name": "转账",
        "created_at": "2026-07-07 00:00:00",
        "updated_at": "2026-07-07 00:00:00",
        "created_by": "default",
        "updated_by": "default",
        "is_deleted": False
    },
    {
        "code": "expense",
        "name": "支出",
        "created_at": "2026-07-07 00:00:00",
        "updated_at": "2026-07-07 00:00:00",
        "created_by": "default",
        "updated_by": "default",
        "is_deleted": False
    },
    {
        "code": "income",
        "name": "收入",
        "created_at": "2026-07-07 00:00:00",
        "updated_at": "2026-07-07 00:00:00",
        "created_by": "default",
        "updated_by": "default",
        "is_deleted": False
    }
]

b = {i['code']:i['name'] for i in a}

print(b)