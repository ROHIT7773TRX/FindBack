"""
CRUD Operations implementation using PyMongo.
Provides clean functions for Create, Read, Update, and Delete operations on MongoDB.
"""

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pymongo.errors import PyMongoError, DuplicateKeyError, WriteError
from app.database import get_items_collection, get_users_collection


# =============================================================================
# 1. CREATE (INSERT) OPERATIONS
# =============================================================================

def create_item(item_doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Inserts a single item document into the 'items' collection.
    MongoDB $jsonSchema validation will automatically check the document.
    """
    collection = get_items_collection()
    if "created_at" not in item_doc:
        item_doc["created_at"] = datetime.now(timezone.utc)
    if "updated_at" not in item_doc:
        item_doc["updated_at"] = datetime.now(timezone.utc)

    try:
        result = collection.insert_one(item_doc)
        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "item_id": item_doc.get("item_id"),
            "message": f"Item '{item_doc.get('item_name')}' created successfully."
        }
    except DuplicateKeyError as e:
        return {
            "success": False,
            "error": "DuplicateKeyError",
            "message": f"Item with ID '{item_doc.get('item_id')}' already exists."
        }
    except WriteError as e:
        return {
            "success": False,
            "error": "ValidationError",
            "message": f"MongoDB $jsonSchema validation rejected the document: {e.details.get('errmsg', str(e))}"
        }
    except PyMongoError as e:
        return {
            "success": False,
            "error": type(e).__name__,
            "message": f"Database error occurred: {str(e)}"
        }


def insert_multiple_items(items_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Inserts a batch of item documents using insert_many()."""
    collection = get_items_collection()
    now = datetime.now(timezone.utc)
    for doc in items_list:
        if "created_at" not in doc:
            doc["created_at"] = now
        if "updated_at" not in doc:
            doc["updated_at"] = now

    try:
        result = collection.insert_many(items_list, ordered=False)
        return {
            "success": True,
            "inserted_count": len(result.inserted_ids),
            "message": f"Successfully inserted {len(result.inserted_ids)} items."
        }
    except PyMongoError as e:
        return {
            "success": False,
            "error": type(e).__name__,
            "message": f"Error during batch insert: {str(e)}"
        }


# =============================================================================
# 2. READ (FIND & SEARCH) OPERATIONS
# =============================================================================

def get_items(
    filter_query: Optional[Dict[str, Any]] = None,
    limit: int = 50,
    skip: int = 0,
    sort_by: str = "date_reported",
    sort_order: int = -1
) -> List[Dict[str, Any]]:
    """
    Retrieves item documents matching the given filter query.
    Supports sorting, pagination (skip/limit), and exclusion of MongoDB internal _id.
    """
    collection = get_items_collection()
    query = filter_query or {}
    cursor = collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
    
    results = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])  # Make JSON serializable
        results.append(doc)
    return results


def get_item_by_id(item_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single item by its unique human-readable item_id."""
    collection = get_items_collection()
    doc = collection.find_one({"item_id": item_id})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


def search_items(
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    item_type: Optional[str] = None,
    location: Optional[str] = None,
    status: Optional[str] = None,
    min_reward: Optional[float] = None
) -> List[Dict[str, Any]]:
    """
    Constructs a compound MongoDB query filter based on user-provided criteria.
    Uses regex case-insensitive matching for keyword searching across names and descriptions.
    """
    query: Dict[str, Any] = {}

    if category and category != "All":
        query["category"] = category

    if item_type and item_type != "All":
        query["type"] = item_type.lower()

    if location and location != "All":
        query["location"] = location

    if status and status != "All":
        query["status"] = status.lower()

    if min_reward is not None and min_reward > 0:
        query["reward"] = {"$gte": float(min_reward)}

    if keyword and keyword.strip():
        term = keyword.strip()
        query["$or"] = [
            {"item_name": {"$regex": term, "$options": "i"}},
            {"description": {"$regex": term, "$options": "i"}},
            {"location": {"$regex": term, "$options": "i"}},
            {"tags": {"$regex": term, "$options": "i"}}
        ]

    return get_items(filter_query=query, limit=100)


def get_unresolved_items() -> List[Dict[str, Any]]:
    """Returns all items whose status is either 'open' or 'matched'."""
    query = {"status": {"$in": ["open", "matched"]}}
    return get_items(filter_query=query)


# =============================================================================
# 3. UPDATE OPERATIONS
# =============================================================================

def update_item_status(item_id: str, new_status: str) -> Dict[str, Any]:
    """
    Updates the lifecycle status ('open', 'matched', 'resolved', 'closed') of an item.
    Updates the updated_at timestamp automatically.
    """
    collection = get_items_collection()
    now = datetime.now(timezone.utc)
    try:
        result = collection.update_one(
            {"item_id": item_id},
            {
                "$set": {
                    "status": new_status.lower(),
                    "updated_at": now
                }
            }
        )
        if result.matched_count == 0:
            return {"success": False, "message": f"No item found with ID '{item_id}'."}
        return {
            "success": True,
            "modified_count": result.modified_count,
            "message": f"Item '{item_id}' status updated to '{new_status}'."
        }
    except WriteError as e:
        return {
            "success": False,
            "error": "ValidationError",
            "message": f"Validation failed on update: {e.details.get('errmsg', str(e))}"
        }
    except PyMongoError as e:
        return {"success": False, "error": type(e).__name__, "message": str(e)}


def update_item(item_id: str, update_fields: Dict[str, Any]) -> Dict[str, Any]:
    """Updates specified fields of an item document."""
    collection = get_items_collection()
    update_fields["updated_at"] = datetime.now(timezone.utc)
    # Remove immutable fields if present
    update_fields.pop("_id", None)
    update_fields.pop("item_id", None)
    update_fields.pop("created_at", None)

    try:
        result = collection.update_one(
            {"item_id": item_id},
            {"$set": update_fields}
        )
        if result.matched_count == 0:
            return {"success": False, "message": f"No item found with ID '{item_id}'."}
        return {
            "success": True,
            "modified_count": result.modified_count,
            "message": f"Item '{item_id}' updated successfully."
        }
    except WriteError as e:
        return {
            "success": False,
            "error": "ValidationError",
            "message": f"MongoDB validation error: {e.details.get('errmsg', str(e))}"
        }
    except PyMongoError as e:
        return {"success": False, "error": type(e).__name__, "message": str(e)}


# =============================================================================
# 4. DELETE OPERATIONS
# =============================================================================

def delete_item(item_id: str) -> Dict[str, Any]:
    """Deletes a single item document from the database using delete_one()."""
    collection = get_items_collection()
    try:
        result = collection.delete_one({"item_id": item_id})
        if result.deleted_count == 0:
            return {"success": False, "message": f"No item found with ID '{item_id}' to delete."}
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "message": f"Item '{item_id}' successfully deleted."
        }
    except PyMongoError as e:
        return {"success": False, "error": type(e).__name__, "message": str(e)}


def delete_items_by_query(query: Dict[str, Any]) -> Dict[str, Any]:
    """Deletes multiple documents matching a filter using delete_many()."""
    collection = get_items_collection()
    try:
        result = collection.delete_many(query)
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "message": f"Deleted {result.deleted_count} items."
        }
    except PyMongoError as e:
        return {"success": False, "error": type(e).__name__, "message": str(e)}


# =============================================================================
# 5. USER AND SUMMARY HELPERS
# =============================================================================

def get_dashboard_counts() -> Dict[str, int]:
    """Retrieves quick summary metric counts using count_documents()."""
    collection = get_items_collection()
    return {
        "total_reports": collection.count_documents({}),
        "lost_items": collection.count_documents({"type": "lost"}),
        "found_items": collection.count_documents({"type": "found"}),
        "open_reports": collection.count_documents({"status": "open"}),
        "matched_reports": collection.count_documents({"status": "matched"}),
        "resolved_reports": collection.count_documents({"status": "resolved"}),
        "closed_reports": collection.count_documents({"status": "closed"})
    }


def get_all_users() -> List[Dict[str, Any]]:
    """Fetches all registered users."""
    collection = get_users_collection()
    users = list(collection.find({}, {"_id": 0}))
    return users


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Fetches a specific user by user_id."""
    collection = get_users_collection()
    return collection.find_one({"user_id": user_id}, {"_id": 0})
