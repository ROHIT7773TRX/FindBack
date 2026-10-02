"""
Automated Test Suite for FindBack.
Tests MongoDB connection, $jsonSchema validation, CRUD operations, and Aggregation pipelines.
"""

import sys
import os
import unittest
from datetime import datetime, timezone

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import test_connection, get_db, get_items_collection, get_users_collection
from app.models import build_item_document
from app.crud import (
    create_item,
    get_items,
    get_item_by_id,
    search_items,
    update_item_status,
    update_item,
    delete_item,
    get_dashboard_counts
)
from app.analytics import (
    get_reports_by_category,
    get_reports_by_location,
    get_lost_vs_found_stats,
    get_status_distribution,
    get_open_electronics_by_location,
    get_items_with_reporter_details
)


class TestFindBackDatabase(unittest.TestCase):
    """Unit and Integration tests for MongoDB operations."""

    @classmethod
    def setUpClass(cls):
        """Verify database connectivity before running tests."""
        connected = test_connection()
        if not connected:
            raise unittest.SkipTest("MongoDB server is not reachable. Skipping database tests.")
        cls.items_col = get_items_collection()
        cls.users_col = get_users_collection()
        cls.test_item_id = "TEST-UNIT-999"

    def tearDown(self):
        """Clean up test records after each test."""
        self.items_col.delete_many({"item_id": {"$regex": "^TEST-UNIT-"}})

    # =========================================================================
    # 1. Connectivity Tests
    # =========================================================================
    def test_01_connection_ping(self):
        """Test MongoDB server ping."""
        self.assertTrue(test_connection(), "MongoDB ping should succeed.")

    # =========================================================================
    # 2. Validation Tests ($jsonSchema)
    # =========================================================================
    def test_02_validation_valid_insert(self):
        """Valid document must be accepted by MongoDB schema validator."""
        doc = build_item_document(
            item_id=self.test_item_id,
            item_name="Unit Test Laptop",
            category="Electronics",
            item_type="lost",
            description="Silver laptop testing unit insertion.",
            location="Central Library",
            reported_by="USR-101",
            reward=200
        )
        res = create_item(doc)
        self.assertTrue(res["success"], f"Valid item insertion failed: {res.get('message')}")
        self.assertIsNotNone(res.get("inserted_id"))

    def test_03_validation_invalid_category_rejected(self):
        """Document with illegal category enum must be rejected by MongoDB."""
        now = datetime.now(timezone.utc)
        invalid_doc = {
            "item_id": f"{self.test_item_id}-INV-CAT",
            "item_name": "Invalid Category Item",
            "category": "INVALID_CAT_123",  # Not in enum
            "type": "lost",
            "description": "Valid description length test.",
            "location": "Science Block 1",
            "date_reported": now,
            "status": "open",
            "reported_by": "USR-101",
            "created_at": now,
            "updated_at": now
        }
        res = create_item(invalid_doc)
        self.assertFalse(res["success"], "MongoDB should reject document with invalid category enum.")
        self.assertEqual(res.get("error"), "ValidationError")

    def test_04_validation_missing_location_rejected(self):
        """Document missing required field 'location' must be rejected."""
        now = datetime.now(timezone.utc)
        invalid_doc = {
            "item_id": f"{self.test_item_id}-MIS-LOC",
            "item_name": "Item Missing Location",
            "category": "Books",
            "type": "found",
            "description": "Valid description test.",
            # 'location' omitted intentionally
            "date_reported": now,
            "status": "open",
            "reported_by": "USR-101",
            "created_at": now,
            "updated_at": now
        }
        res = create_item(invalid_doc)
        self.assertFalse(res["success"], "MongoDB should reject document missing required field.")

    # =========================================================================
    # 3. CRUD Tests
    # =========================================================================
    def test_05_crud_create_read(self):
        """Test CREATE (insertOne) and READ (findOne)."""
        doc = build_item_document(
            item_id=self.test_item_id,
            item_name="Scientific Calculator Unit Test",
            category="Stationery",
            item_type="found",
            description="Black fx-991ms unit test calculator.",
            location="Computer Lab 3",
            reported_by="USR-102"
        )
        create_res = create_item(doc)
        self.assertTrue(create_res["success"])

        retrieved = get_item_by_id(self.test_item_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["item_name"], "Scientific Calculator Unit Test")
        self.assertEqual(retrieved["category"], "Stationery")

    def test_06_crud_search_and_filter(self):
        """Test search query filters."""
        doc = build_item_document(
            item_id=self.test_item_id,
            item_name="Rare Vintage Watch",
            category="Accessories",
            item_type="lost",
            description="Gold plated vintage collectible watch.",
            location="Main Auditorium",
            reported_by="USR-103",
            reward=500
        )
        create_item(doc)

        results = search_items(category="Accessories", keyword="Vintage")
        self.assertGreaterEqual(len(results), 1)
        self.assertTrue(any(i["item_id"] == self.test_item_id for i in results))

    def test_07_crud_update_status(self):
        """Test UPDATE (updateOne) status lifecycle change."""
        doc = build_item_document(
            item_id=self.test_item_id,
            item_name="Lab Coat White",
            category="Clothing",
            item_type="found",
            description="White cotton lab coat size M.",
            location="Science Block 1",
            reported_by="USR-104",
            status="open"
        )
        create_item(doc)

        up_res = update_item_status(self.test_item_id, "resolved")
        self.assertTrue(up_res["success"])
        self.assertEqual(up_res["modified_count"], 1)

        updated = get_item_by_id(self.test_item_id)
        self.assertEqual(updated["status"], "resolved")

    def test_08_crud_delete(self):
        """Test DELETE (deleteOne)."""
        doc = build_item_document(
            item_id=self.test_item_id,
            item_name="Temporary Item To Delete",
            category="Other",
            item_type="lost",
            description="Item created solely to test deleteOne.",
            location="Hostel Block C",
            reported_by="USR-101"
        )
        create_item(doc)

        del_res = delete_item(self.test_item_id)
        self.assertTrue(del_res["success"])
        self.assertEqual(del_res["deleted_count"], 1)

        # Verify no longer exists
        retrieved = get_item_by_id(self.test_item_id)
        self.assertIsNone(retrieved)

    # =========================================================================
    # 4. Aggregation Pipeline Tests
    # =========================================================================
    def test_09_aggregation_category(self):
        """Test Aggregation Pipeline 1: Group by Category."""
        stats = get_reports_by_category()
        self.assertIsInstance(stats, list)
        if len(stats) > 0:
            first = stats[0]
            self.assertIn("category", first)
            self.assertIn("total_reports", first)
            self.assertIn("lost_count", first)
            self.assertIn("found_count", first)

    def test_10_aggregation_location(self):
        """Test Aggregation Pipeline 2: Hotspots by Location."""
        hotspots = get_reports_by_location(limit=5)
        self.assertIsInstance(hotspots, list)
        self.assertLessEqual(len(hotspots), 5)
        if len(hotspots) > 0:
            first = hotspots[0]
            self.assertIn("location", first)
            self.assertIn("report_count", first)

    def test_11_aggregation_resolution_rate(self):
        """Test Aggregation Pipeline 3: Lost vs Found Breakdown."""
        res_stats = get_lost_vs_found_stats()
        self.assertIsInstance(res_stats, list)
        for entry in res_stats:
            self.assertIn(entry["report_type"], ["lost", "found"])
            self.assertIn("resolution_rate_percent", entry)

    def test_12_aggregation_status_distribution(self):
        """Test Aggregation Pipeline 4: Status Breakdown."""
        status_stats = get_status_distribution()
        self.assertIsInstance(status_stats, list)
        if len(status_stats) > 0:
            self.assertIn("status", status_stats[0])
            self.assertIn("count", status_stats[0])

    def test_13_aggregation_open_electronics(self):
        """Test Aggregation Pipeline 5: Open Electronics Hotspots."""
        open_elec = get_open_electronics_by_location()
        self.assertIsInstance(open_elec, list)
        if len(open_elec) > 0:
            self.assertIn("location", open_elec[0])
            self.assertIn("open_electronics_count", open_elec[0])

    def test_14_aggregation_cross_collection_lookup(self):
        """Test Aggregation Pipeline 6: Cross-Collection $lookup with Users."""
        lookups = get_items_with_reporter_details(limit=5)
        self.assertIsInstance(lookups, list)
        if len(lookups) > 0:
            self.assertIn("item_id", lookups[0])
            self.assertIn("item_name", lookups[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
