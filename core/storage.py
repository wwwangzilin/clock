import json
import os
from datetime import date

DATA_FILE = "tomato_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tomato():
    today = date.today().isoformat()
    data = load_data()
    data[today] = data.get(today, 0) + 1
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_today_count():
    today = date.today().isoformat()
    return load_data().get(today, 0)