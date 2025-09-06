import json
from pathlib import Path
from typing import List, Dict, Any

STORE_FILE = Path("feedback_store.json")

def load_store() -> List[Dict[str, Any]]:
    if not STORE_FILE.exists():
        return []
    try:
        with open(STORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_store(items: List[Dict[str, Any]]):
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
