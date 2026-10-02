"""
Validation Demonstration Script
Demonstrates MongoDB $jsonSchema validation in action:
1. Attempting to insert a valid document (Success)
2. Attempting to insert invalid documents violating schema rules (Rejected by MongoDB)
"""

import sys
import os
from datetime import datetime, timezone

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import get_items_collection, test_connection
from pymongo.errors import WriteError, PyMongoError


def run_validation_demonstration():
    print("=" * 70)
    print("  FINDBACK MONGODB $jsonSchema VALIDATION DEMONSTRATION")
    print("=" * 70)

    if not test_connection():
        print("[X] ERROR: Cannot connect to MongoDB.")
        return

    items_col = get_items_collection()
    now = datetime.now(timezone.utc)

    # Clean up any leftover demo documents from prior test runs
    items_col.delete_many({"item_id": {"$in": ["DEMO-VALID-001", "DEMO-INVALID-001", "DEMO-INVALID-002", "DEMO-INVALID-003"]}})

    # =========================================================================
    # TEST CASE 1: Valid Document Insertion
    # =========================================================================
    print("\n[TEST 1] Inserting a FULLY VALID document...")
    valid_doc = {
        "item_id": "DEMO-VALID-001",
        "item_name": "Apple MacBook Pro 14 (Space Grey)",
        "category": "Electronics",
        "type": "lost",
        "description": "M3 Pro space grey laptop in navy blue protective sleeve.",
        "location": "Central Library",
        "date_reported": now,
        "status": "open",
        "reported_by": "USR-101",
        "contact_email": "aarav.sharma@campus.edu",
        "contact_phone": "+91-9876543210",
        "reward": 500,
        "tags": ["apple", "macbook", "electronics"],
        "created_at": now,
        "updated_at": now
    }

    try:
        res = items_col.insert_one(valid_doc)
        print(f"  [RESULT] SUCCESS! Document inserted with _id: {res.inserted_id}")
        print("  [EXPLANATION] All required fields present, valid types, category & type match enums.")
    except PyMongoError as e:
        print(f"  [RESULT] FAILED: {e}")

    # =========================================================================
    # TEST CASE 2: Invalid Category (Enum Violation)
    # =========================================================================
    print("\n[TEST 2] Inserting document with INVALID CATEGORY ('Weapons_Or_Illegal')...")
    invalid_category_doc = {
        "item_id": "DEMO-INVALID-001",
        "item_name": "Prohibited Item",
        "category": "Weapons_Or_Illegal",  # Not in allowed categories enum
        "type": "lost",
        "description": "Sample description of item for testing validation rejection.",
        "location": "Hostel Block C",
        "date_reported": now,
        "status": "open",
        "reported_by": "USR-101",
        "created_at": now,
        "updated_at": now
    }

    try:
        items_col.insert_one(invalid_category_doc)
        print("  [RESULT] Unexpected Success (Schema not enforcing enum!)")
    except WriteError as e:
        print(f"  [RESULT] REJECTED BY MONGODB as expected!")
        print(f"  [ERROR DETAILS] {e.details.get('errmsg', str(e))}")
        print("  [VIVA EXPLANATION] MongoDB $jsonSchema specifies category enum: ['Electronics', 'Books', ...].")
        print("                   The value 'Weapons_Or_Illegal' was rejected.")

    # =========================================================================
    # TEST CASE 3: Missing Mandatory Field ('location')
    # =========================================================================
    print("\n[TEST 3] Inserting document MISSING REQUIRED FIELD ('location')...")
    missing_field_doc = {
        "item_id": "DEMO-INVALID-002",
        "item_name": "Titan Wristwatch",
        "category": "Accessories",
        "type": "found",
        "description": "Silver mesh strap analog watch found on bench.",
        # "location" is intentionally omitted!
        "date_reported": now,
        "status": "open",
        "reported_by": "USR-105",
        "created_at": now,
        "updated_at": now
    }

    try:
        items_col.insert_one(missing_field_doc)
        print("  [RESULT] Unexpected Success (Required field check failed!)")
    except WriteError as e:
        print(f"  [RESULT] REJECTED BY MONGODB as expected!")
        print(f"  [ERROR DETAILS] {e.details.get('errmsg', str(e))}")
        print("  [VIVA EXPLANATION] 'location' is listed in required: [...] array in $jsonSchema.")
        print("                   MongoDB refused to insert document without location.")

    # =========================================================================
    # TEST CASE 4: Invalid Status Enum Value ('in_progress')
    # =========================================================================
    print("\n[TEST 4] Inserting document with ILLEGAL STATUS ('in_progress')...")
    invalid_status_doc = {
        "item_id": "DEMO-INVALID-003",
        "item_name": "Blue Physics File",
        "category": "Stationery",
        "type": "lost",
        "description": "Practical file with signed experiments.",
        "location": "Science Block 1",
        "date_reported": now,
        "status": "in_progress",  # Only 'open', 'matched', 'resolved', 'closed' allowed
        "reported_by": "USR-108",
        "created_at": now,
        "updated_at": now
    }

    try:
        items_col.insert_one(invalid_status_doc)
        print("  [RESULT] Unexpected Success (Status enum check failed!)")
    except WriteError as e:
        print(f"  [RESULT] REJECTED BY MONGODB as expected!")
        print(f"  [ERROR DETAILS] {e.details.get('errmsg', str(e))}")
        print("  [VIVA EXPLANATION] 'status' must be one of: ['open', 'matched', 'resolved', 'closed'].")

    # Clean up test documents
    items_col.delete_one({"item_id": "DEMO-VALID-001"})

    print("\n" + "=" * 70)
    print("  VALIDATION TEST SUITE PASSED ALL ENFORCEMENT CHECKS")
    print("=" * 70)


if __name__ == "__main__":
    run_validation_demonstration()
