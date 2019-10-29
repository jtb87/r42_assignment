from datetime import datetime
from uuid import uuid4
import json

data_format = {
    "id": str(uuid4()),
    "emails": [
        {"email": "alice@gmail.com", "name": "Alice"},
        {"email": "bob@gmail.com", "name": "Bob"},
    ],
    "order_ids": [
        {"id": str(uuid4()), "quantity": 1, "item_id": str(uuid4())},
        {"id": str(uuid4()), "quantity": 3, "item_id": str(uuid4())},
    ],
    "account_status": "open",
    "location": "Amsterdam",
    "creation_date": f"{datetime.now().isoformat()}",
}


def generate_data():
    filename = f'data_{str(datetime.now().time()).split(".")[0].replace(":", "")}.json'
    create_file(filename=filename, data=data_format)


def create_file(filename: str, data):
    full_path = f"./{filename}"
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    generate_data()
