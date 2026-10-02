"""
MongoDB Aggregation Pipelines executed via PyMongo.
Provides analytical intelligence on campus loss and recovery patterns.
"""

from typing import List, Dict, Any
from app.database import get_items_collection


# =============================================================================
# PIPELINE 1: Reports Grouped by Item Category
# =============================================================================
def get_reports_by_category() -> List[Dict[str, Any]]:
    """
    Aggregation 1: Counts total, lost, and found reports per category.
    Stages: $group -> $project -> $sort
    """
    collection = get_items_collection()
    pipeline = [
        {
            "$group": {
                "_id": "$category",
                "total_reports": {"$sum": 1},
                "lost_count": {
                    "$sum": {"$cond": [{"$eq": ["$type", "lost"]}, 1, 0]}
                },
                "found_count": {
                    "$sum": {"$cond": [{"$eq": ["$type", "found"]}, 1, 0]}
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "category": "$_id",
                "total_reports": 1,
                "lost_count": 1,
                "found_count": 1
            }
        },
        {
            "$sort": {"total_reports": -1}
        }
    ]
    return list(collection.aggregate(pipeline))


# =============================================================================
# PIPELINE 2: Top Campus Location Hotspots
# =============================================================================
def get_reports_by_location(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Aggregation 2: Identifies campus hotspots with the most lost/found activity.
    Stages: $group -> $project -> $sort -> $limit
    """
    collection = get_items_collection()
    pipeline = [
        {
            "$group": {
                "_id": "$location",
                "report_count": {"$sum": 1},
                "unresolved_count": {
                    "$sum": {"$cond": [{"$in": ["$status", ["open", "matched"]]}, 1, 0]}
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "location": "$_id",
                "report_count": 1,
                "unresolved_count": 1
            }
        },
        {
            "$sort": {"report_count": -1}
        },
        {
            "$limit": limit
        }
    ]
    return list(collection.aggregate(pipeline))


# =============================================================================
# PIPELINE 3: Lost vs Found Distribution & Resolution Percentage
# =============================================================================
def get_lost_vs_found_stats() -> List[Dict[str, Any]]:
    """
    Aggregation 3: Computes lost vs found breakdown with resolution rate calculation.
    Stages: $group -> $project ($multiply, $divide, $round) -> $sort
    """
    collection = get_items_collection()
    pipeline = [
        {
            "$group": {
                "_id": "$type",
                "total_items": {"$sum": 1},
                "resolved_items": {
                    "$sum": {"$cond": [{"$eq": ["$status", "resolved"]}, 1, 0]}
                },
                "open_items": {
                    "$sum": {"$cond": [{"$eq": ["$status", "open"]}, 1, 0]}
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "report_type": "$_id",
                "total_items": 1,
                "resolved_items": 1,
                "open_items": 1,
                "resolution_rate_percent": {
                    "$round": [
                        {"$multiply": [{"$divide": ["$resolved_items", "$total_items"]}, 100]},
                        1
                    ]
                }
            }
        },
        {
            "$sort": {"total_items": -1}
        }
    ]
    return list(collection.aggregate(pipeline))


# =============================================================================
# PIPELINE 4: Lifecycle Status Distribution
# =============================================================================
def get_status_distribution() -> List[Dict[str, Any]]:
    """
    Aggregation 4: Evaluates lifecycle health across open, matched, resolved, and closed.
    Stages: $group -> $project -> $sort
    """
    collection = get_items_collection()
    pipeline = [
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "status": "$_id",
                "count": 1
            }
        },
        {
            "$sort": {"count": -1}
        }
    ]
    return list(collection.aggregate(pipeline))


# =============================================================================
# PIPELINE 5: Open Electronics Hotspot & Reward Analysis
# =============================================================================
def get_open_electronics_by_location() -> List[Dict[str, Any]]:
    """
    Aggregation 5: Multi-stage pipeline filtering open Electronics and calculating average rewards.
    Stages: $match -> $group -> $project -> $sort
    """
    collection = get_items_collection()
    pipeline = [
        {
            "$match": {
                "category": "Electronics",
                "status": "open"
            }
        },
        {
            "$group": {
                "_id": "$location",
                "open_electronics_count": {"$sum": 1},
                "average_reward": {"$avg": "$reward"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "location": "$_id",
                "open_electronics_count": 1,
                "average_reward": {"$round": ["$average_reward", 2]}
            }
        },
        {
            "$sort": {"open_electronics_count": -1}
        }
    ]
    return list(collection.aggregate(pipeline))


# =============================================================================
# PIPELINE 6: Cross-Collection Join ($lookup) with Users
# =============================================================================
def get_items_with_reporter_details(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Aggregation 6: Joins items with users collection to enrich reports with student/faculty info.
    Stages: $match -> $lookup -> $unwind -> $project -> $limit
    """
    collection = get_items_collection()
    pipeline = [
        {
            "$match": {"type": "lost", "status": "open"}
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "reported_by",
                "foreignField": "user_id",
                "as": "reporter_info"
            }
        },
        {
            "$unwind": {
                "path": "$reporter_info",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "_id": 0,
                "item_id": 1,
                "item_name": 1,
                "category": 1,
                "location": 1,
                "reward": 1,
                "reporter_name": "$reporter_info.name",
                "department": "$reporter_info.department",
                "reporter_role": "$reporter_info.role"
            }
        },
        {
            "$limit": limit
        }
    ]
    return list(collection.aggregate(pipeline))
