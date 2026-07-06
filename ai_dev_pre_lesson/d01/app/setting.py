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
    "user": WORKSPACE_ROOT / "ai_dev_pre_lesson/d01/data/user.json",
    "account": WORKSPACE_ROOT / "ai_dev_pre_lesson/d01/data/account.json",
    "category": WORKSPACE_ROOT / "ai_dev_pre_lesson/d01/data/category.json",
    "transaction": WORKSPACE_ROOT / "ai_dev_pre_lesson/d01/data/transaction.json",
}
JSON_INITIAL_DATA = {
    "user":[
        {
            "id": "c31d22c5-bbb8-42f5-aa1e-66fb096c93b7",
            "username": "admin",
            "password": "admin",
            "role": "admin",
            "created_at": "2026-07-07 00:00:00",
            "updated_at": "2026-07-07 00:00:00",
            "created_by": "system",
            "updated_by": "system",
            "deleted": False
        }
    ],
    "account":[
        {
            "id": "0ce63620-8dd7-445c-9c80-1df6bb3f2d21",
            "user_id": "c31d22c5-bbb8-42f5-aa1e-66fb096c93b7",
            "name": "Cash",
            "type": "cash",
            "balance": 0,
            "created_at": "2026-07-07 00:00:00",
            "updated_at": "2026-07-07 00:00:00",
            "created_by": "system",
            "updated_by": "system",
            "deleted": False
        }
    ],
    "category":[],
    "transaction":[]
}