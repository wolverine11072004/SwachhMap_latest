
import hashlib
from data_store import load_json_file, save_json_file, get_default_files
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users(base_dir):
    paths = get_default_files(base_dir)
    u = load_json_file(paths['USER_FILE'], {})
    normalized = {}
    for k, v in u.items():
        if isinstance(v, dict) and 'password' in v:
            normalized[k] = v
        else:
            normalized[k] = {'password': v, 'tokens': 0}
    return normalized

def save_users(users_dict, base_dir):
    paths = get_default_files(base_dir)
    save_json_file(paths['USER_FILE'], users_dict)

def save_user(username, password, base_dir):
    users = load_users(base_dir)
    if username in users:
        return False
    users[username] = {'password': hash_password(password), 'tokens': 0}
    save_users(users, base_dir)
    return True

def authenticate_user(username, password, base_dir):
    users = load_users(base_dir)
    entry = users.get(username)
    if not entry:
        return False
    return entry.get('password') == hash_password(password)

# Token management
def load_tokens(base_dir):
    paths = get_default_files(base_dir)
    tokens = load_json_file(paths['TOKENS_FILE'], {})
    return tokens

def save_tokens(tokens, base_dir):
    paths = get_default_files(base_dir)
    save_json_file(paths['TOKENS_FILE'], tokens)

def add_tokens(username, amount, base_dir):
    if not username:
        return
    tokens = load_tokens(base_dir)
    tokens[username] = tokens.get(username, 0) + amount
    save_tokens(tokens, base_dir)
    users = load_users(base_dir)
    if username in users:
        users[username]['tokens'] = tokens[username]
        save_users(users, base_dir)

def get_user_tokens(username, base_dir):
    tokens = load_tokens(base_dir)
    if username in tokens:
        return tokens[username]
    users = load_users(base_dir)
    return users.get(username, {}).get('tokens', 0)
