
import json, os
from datetime import datetime

def load_json_file(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# helpers for app to access default file names
def get_default_files(base_dir):
    return {
        "USER_FILE": os.path.join(base_dir, "users.json"),
        "REPORT_FILE": os.path.join(base_dir, "reports.json"),
        "TOKENS_FILE": os.path.join(base_dir, "user_tokens.json"),
        "UPLOAD_DIR": os.path.join(base_dir, "uploads"),
        "GEOCACHE_FILE": os.path.join(base_dir, "geocache.json")
    }
