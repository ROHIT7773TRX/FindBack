"""
Database connection manager using PyMongo.
Connects to MongoDB using standard connection string and provides database access.
"""

import os
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "campus_findback")

_client: Optional[MongoClient] = None


def get_client() -> MongoClient:
    """Returns a singleton PyMongo MongoClient instance."""
    global _client
    if _client is None:
        _client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000
        )
    return _client


def get_db(db_name: Optional[str] = None) -> Database:
    """Returns the MongoDB database instance."""
    client = get_client()
    target_name = db_name or DATABASE_NAME
    return client[target_name]


def get_items_collection() -> Collection:
    """Convenience helper to get the 'items' collection."""
    return get_db()["items"]


def get_users_collection() -> Collection:
    """Convenience helper to get the 'users' collection."""
    return get_db()["users"]


def test_connection() -> bool:
    """
    Sends a 'ping' command to MongoDB to verify server connectivity.
    Returns True if connected successfully, False otherwise.
    """
    try:
        client = get_client()
        client.admin.command('ping')
        return True
    except Exception as err:
        print(f"[!] MongoDB connection error: {err}")
        return False


def close_connection() -> None:
    """Closes the MongoDB connection pool cleanly."""
    global _client
    if _client is not None:
        _client.close()
        _client = None
