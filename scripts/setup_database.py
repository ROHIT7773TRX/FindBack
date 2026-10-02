"""
Database Setup Script
Initializes MongoDB collections with strict $jsonSchema validation rules and performance indexes.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pymongo.errors import PyMongoError, CollectionInvalid
from app.database import get_db, test_connection
from app.models import ITEMS_VALIDATION_SCHEMA, USERS_VALIDATION_SCHEMA


def setup_database(drop_existing: bool = False) -> bool:
    """Configures the 'campus_findback' database with validation schemas and indexes."""
    print("=" * 60)
    print("  FINDBACK DATABASE SETUP & SCHEMA VALIDATION INITIALIZER")
    print("=" * 60)

    if not test_connection():
        print("[X] ERROR: Could not connect to MongoDB server. Ensure MongoDB is running.")
        return False

    db = get_db()
    existing_collections = db.list_collection_names()
    print(f"[*] Target Database: {db.name}")
    print(f"[*] Existing Collections: {existing_collections}")

    # Setup 'users' collection
    if drop_existing and "users" in existing_collections:
        print("[-] Dropping existing 'users' collection...")
        db.drop_collection("users")

    if "users" not in db.list_collection_names():
        print("[+] Creating 'users' collection with $jsonSchema validation...")
        try:
            db.create_collection(
                "users",
                validator=USERS_VALIDATION_SCHEMA,
                validationLevel="strict",
                validationAction="error"
            )
        except CollectionInvalid:
            pass
    else:
        print("[*] Updating 'users' collection validation rules...")
        db.command({
            "collMod": "users",
            "validator": USERS_VALIDATION_SCHEMA,
            "validationLevel": "strict",
            "validationAction": "error"
        })

    # Users Indexes
    print("[+] Creating indexes for 'users'...")
    db.users.create_index("user_id", unique=True)
    db.users.create_index("email", unique=True)

    # Setup 'items' collection
    if drop_existing and "items" in existing_collections:
        print("[-] Dropping existing 'items' collection...")
        db.drop_collection("items")

    if "items" not in db.list_collection_names():
        print("[+] Creating 'items' collection with $jsonSchema validation...")
        try:
            db.create_collection(
                "items",
                validator=ITEMS_VALIDATION_SCHEMA,
                validationLevel="strict",
                validationAction="error"
            )
        except CollectionInvalid:
            pass
    else:
        print("[*] Updating 'items' collection validation rules...")
        db.command({
            "collMod": "items",
            "validator": ITEMS_VALIDATION_SCHEMA,
            "validationLevel": "strict",
            "validationAction": "error"
        })

    # Items Indexes
    print("[+] Creating indexes for 'items'...")
    db.items.create_index("item_id", unique=True)
    db.items.create_index("category")
    db.items.create_index("type")
    db.items.create_index("status")
    db.items.create_index("location")
    db.items.create_index([
        ("item_name", "text"),
        ("description", "text"),
        ("location", "text")
    ])

    print("[V] Database collections, $jsonSchema rules, and indexes set up successfully!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    drop_flag = "--drop" in sys.argv or "-d" in sys.argv
    success = setup_database(drop_existing=drop_flag)
    sys.exit(0 if success else 1)
