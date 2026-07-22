from pathlib import Path
from datetime import timedelta, timezone

def find_root(start: Path, marker: str = "pyproject.toml") -> Path:
    current = start.resolve()

    for parent in [current, *current.parents]:
        if (parent / marker).exists():
            return parent

    raise FileNotFoundError(f"Cannot find {marker} from {start}")


WORKSPACE_ROOT = find_root(Path(__file__))
UTC_PLUS_8 = timezone(timedelta(hours=8))

JSON_PATH = {
    "local": WORKSPACE_ROOT / "ai_dev_pre_lesson/d01/data/local.json",
    "user": WORKSPACE_ROOT / "ai_dev_pre_lesson/d01/data/user.json",
    "role": WORKSPACE_ROOT / "ai_dev_pre_lesson/d01/data/role.json",
    "account": WORKSPACE_ROOT / "ai_dev_pre_lesson/d01/data/account.json",
    "category": WORKSPACE_ROOT / "ai_dev_pre_lesson/d01/data/category.json",
    "transaction": WORKSPACE_ROOT / "ai_dev_pre_lesson/d01/data/transaction.json",
    "direction": WORKSPACE_ROOT / "ai_dev_pre_lesson/d01/data/direction.json",
    "account_type": WORKSPACE_ROOT / "ai_dev_pre_lesson/d01/data/account_type.json",
}
JSON_INITIAL_DATA = {
    "user":[
        {
            "id": "019f3af6-2a54-78b1-9fda-96b19db927ab",
            "name": "admin",
            "password": "admin",
            "role_code": "019f4515-aebe-7710-b714-001d7a975f5e",
            "created_at": "2026-07-07 00:00:00",
            "updated_at": "2026-07-07 00:00:00",
            "created_by": "default",
            "updated_by": "default",
            "is_deleted": False
        }
    ],
    "account":[
        {
            "id": "019f3af6-72cc-7768-b53c-ad2538f4e0b6",
            "user_id": "019f3af6-2a54-78b1-9fda-96b19db927ab",
            "account_type_id": "019f3b60-6f1b-73cb-a147-c2462c9d7749",
            "name": "人民币",
            "balance": 0,
            "created_at": "2026-07-07 00:00:00",
            "updated_at": "2026-07-07 00:00:00",
            "created_by": "default",
            "updated_by": "default",
            "is_deleted": False,
            "is_default": True
        }
    ],
    "category":[
        {
            "id": "019f3af6-c9c0-72b5-b422-55ced6043cdf",
            "user_id": "019f3af6-2a54-78b1-9fda-96b19db927ab",
            "direction_code": "expense",
            "name": "饮食",
            "created_at": "2026-07-07 00:00:00",
            "updated_at": "2026-07-07 00:00:00",
            "created_by": "default",
            "updated_by": "default",
            "is_deleted": False,
            "is_default": True
        }
    ],
    "transaction":[],
    "account_type": [
        {
            "id": "019f3b60-6f1b-73cb-a147-c2462c9d7749",
            "name": "现金",
            "created_at": "2026-07-07 00:00:00",
            "updated_at": "2026-07-07 00:00:00",
            "created_by": "default",
            "updated_by": "default",
            "is_deleted": False
        }
    ],
    "direction":[
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
    ],
    "role":[
        {
            "code": "root",
            "name": "根管理员",
            "created_at": "2026-07-07 00:00:00",
            "updated_at": "2026-07-07 00:00:00",
            "created_by": "default",
            "updated_by": "default",
            "is_deleted": False
        },
        {
            "code": "admin",
            "name": "管理员",
            "created_at": "2026-07-07 00:00:00",
            "updated_at": "2026-07-07 00:00:00",
            "created_by": "default",
            "updated_by": "default",
            "is_deleted": False
        },
        {
            "code": "user",
            "name": "用户",
            "created_at": "2026-07-07 00:00:00",
            "updated_at": "2026-07-07 00:00:00",
            "created_by": "default",
            "updated_by": "default",
            "is_deleted": False
        },
        {
            "code": "guest",
            "name": "访客",
            "created_at": "2026-07-07 00:00:00",
            "updated_at": "2026-07-07 00:00:00",
            "created_by": "default",
            "updated_by": "default",
            "is_deleted": False
        }
    ]
}