"""
Database Seeding Script
Populates the 'campus_findback' database with realistic users and lost/found item documents.
"""

import sys
import os
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import get_db, test_connection
from scripts.setup_database import setup_database


def parse_date(date_val):
    """Converts ISO date string to datetime object if necessary."""
    if isinstance(date_val, str):
        # Handle trailing 'Z' in ISO format
        clean_str = date_val.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(clean_str)
        except ValueError:
            return datetime.utcnow()
    elif isinstance(date_val, datetime):
        return date_val
    return datetime.utcnow()


def seed_database() -> bool:
    """Reads sample_data.json and seeds the MongoDB database."""
    print("=" * 60)
    print("  FINDBACK DATABASE SEEDING PROCESS")
    print("=" * 60)

    if not test_connection():
        print("[X] ERROR: Could not connect to MongoDB server.")
        return False

    # Ensure collections and validation are initialized
    setup_database(drop_existing=True)

    db = get_db()
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mongodb", "sample_data.json"))

    if not os.path.exists(json_path):
        print(f"[X] ERROR: Sample data file not found at: {json_path}")
        return False

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    users_list = data.get("users", [])
    items_list = data.get("items", [])

    print(f"[*] Loaded {len(users_list)} users and {len(items_list)} items from sample_data.json")

    # Seed Users
    print(f"[+] Inserting {len(users_list)} users...")
    for user in users_list:
        user["created_at"] = parse_date(user.get("created_at"))
    
    if users_list:
        result_users = db.users.insert_many(users_list)
        print(f"[V] Successfully inserted {len(result_users.inserted_ids)} users.")

    # Seed Items
    print(f"[+] Inserting {len(items_list)} items...")
    for item in items_list:
        item["date_reported"] = parse_date(item.get("date_reported"))
        item["created_at"] = parse_date(item.get("created_at"))
        item["updated_at"] = parse_date(item.get("updated_at"))

    if items_list:
        result_items = db.items.insert_many(items_list)
        print(f"[V] Successfully inserted {len(result_items.inserted_ids)} items.")

    print("=" * 60)
    print(f"[V] DATABASE SEEDING COMPLETED SUCCESSFULLY!")
    print(f"    - Database Name: {db.name}")
    print(f"    - Total Users:   {db.users.count_documents({})}")
    print(f"    - Total Items:   {db.items.count_documents({})}")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = seed_database()
    sys.exit(0 if success else 1)
