import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

STORE_FILE = Path("feedback_store.json")

def load_store() -> List[Dict[str, Any]]:
    if not STORE_FILE.exists():
        return []
    try:
        with open(STORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def save_store(items: List[Dict[str, Any]]):
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False, default=datetime_serializer)
