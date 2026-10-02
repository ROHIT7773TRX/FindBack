"""
Data definitions, categories, enum constants, and $jsonSchema validation rules.
Provides clean constants and helper dictionaries for MongoDB collection validation.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List

CATEGORIES: List[str] = [
    "Electronics",
    "Books",
    "Stationery",
    "Clothing",
    "Accessories",
    "ID/Documents",
    "Other"
]

ITEM_TYPES: List[str] = ["lost", "found"]

STATUSES: List[str] = ["open", "matched", "resolved", "closed"]

USER_ROLES: List[str] = ["student", "faculty", "staff", "admin"]

CAMPUS_LOCATIONS: List[str] = [
    "Central Library",
    "Computer Lab 3",
    "Cafeteria Block B",
    "Sports Complex",
    "Main Auditorium",
    "Science Block 1",
    "Hostel Block C",
    "Admin Building",
    "Bus Terminal",
    "Student Center"
]

# MongoDB $jsonSchema validation dictionary for 'items' collection
ITEMS_VALIDATION_SCHEMA: Dict[str, Any] = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "item_id",
            "item_name",
            "category",
            "type",
            "description",
            "location",
            "date_reported",
            "status",
            "reported_by",
            "created_at",
            "updated_at"
        ],
        "properties": {
            "item_id": {
                "bsonType": "string",
                "description": "Unique item reference ID (e.g. ITEM-2026-001) - required"
            },
            "item_name": {
                "bsonType": "string",
                "minLength": 2,
                "maxLength": 100,
                "description": "Descriptive title of item - required string (2-100 chars)"
            },
            "category": {
                "enum": CATEGORIES,
                "description": "Must match one of the recognized categories"
            },
            "type": {
                "enum": ITEM_TYPES,
                "description": "Report type - must be 'lost' or 'found'"
            },
            "description": {
                "bsonType": "string",
                "minLength": 5,
                "description": "Detailed description - required string (min 5 chars)"
            },
            "location": {
                "bsonType": "string",
                "description": "Campus location - required string"
            },
            "date_reported": {
                "bsonType": ["date", "string"],
                "description": "Date of incident/report - required"
            },
            "status": {
                "enum": STATUSES,
                "description": "Lifecycle status - open, matched, resolved, closed"
            },
            "reported_by": {
                "bsonType": "string",
                "description": "User ID or reporter reference - required string"
            },
            "contact_email": {
                "bsonType": "string",
                "description": "Contact email - optional string"
            },
            "contact_phone": {
                "bsonType": "string",
                "description": "Contact phone - optional string"
            },
            "reward": {
                "bsonType": ["int", "double", "long", "decimal"],
                "minimum": 0,
                "description": "Monetary reward - optional number >= 0"
            },
            "tags": {
                "bsonType": "array",
                "items": {"bsonType": "string"},
                "description": "Array of keyword tags"
            },
            "created_at": {
                "bsonType": "date",
                "description": "Creation timestamp"
            },
            "updated_at": {
                "bsonType": "date",
                "description": "Last update timestamp"
            }
        }
    }
}

# MongoDB $jsonSchema validation dictionary for 'users' collection
USERS_VALIDATION_SCHEMA: Dict[str, Any] = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id", "name", "email", "role", "department", "created_at"],
        "properties": {
            "user_id": {
                "bsonType": "string",
                "description": "Unique user ID - required string"
            },
            "name": {
                "bsonType": "string",
                "minLength": 2,
                "description": "Full name - required string"
            },
            "email": {
                "bsonType": "string",
                "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                "description": "Valid email address - required string"
            },
            "role": {
                "enum": USER_ROLES,
                "description": "Campus role - student, faculty, staff, admin"
            },
            "department": {
                "bsonType": "string",
                "description": "Department - required string"
            },
            "phone": {
                "bsonType": "string",
                "description": "Phone number - optional string"
            },
            "created_at": {
                "bsonType": "date",
                "description": "Registration date - required date"
            }
        }
    }
}


def build_item_document(
    item_id: str,
    item_name: str,
    category: str,
    item_type: str,
    description: str,
    location: str,
    reported_by: str,
    contact_email: str = "",
    contact_phone: str = "",
    reward: float = 0.0,
    tags: List[str] = None,
    status: str = "open"
) -> Dict[str, Any]:
    """Helper to construct a properly structured and timestamped item document."""
    now = datetime.now(timezone.utc)
    return {
        "item_id": item_id,
        "item_name": item_name.strip(),
        "category": category,
        "type": item_type.lower(),
        "description": description.strip(),
        "location": location.strip(),
        "date_reported": now,
        "status": status.lower(),
        "reported_by": reported_by.strip(),
        "contact_email": contact_email.strip(),
        "contact_phone": contact_phone.strip(),
        "reward": float(reward) if reward else 0.0,
        "tags": tags if tags is not None else [],
        "created_at": now,
        "updated_at": now
    }
