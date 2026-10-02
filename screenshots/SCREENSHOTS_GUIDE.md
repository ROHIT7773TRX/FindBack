# FindBack — Screenshots & Output Demonstration Guide

This guide details the exact screenshots, terminal outputs, and web interface views to capture for your CA-2 submission and presentation.

---

## Recommended Screenshots Checklist

| # | Suggested Filename | Screen / Interface to Capture | Expected Content |
|---|--------------------|--------------------------------|-------------------|
| 01 | `01_database_compass.png` | MongoDB Compass / mongosh | `campus_findback` database with `items` (40 docs) and `users` (12 docs) collections. |
| 02 | `02_schema_validation.png` | MongoDB Compass / `scripts/setup_database.py` | Collection validation tab in Compass or terminal output showing `$jsonSchema` rules. |
| 03 | `03_valid_insert.png` | Terminal / Web UI (`/validation-demo`) | Successful insertion of a compliant item document. |
| 04 | `04_invalid_insert_rejected.png` | Terminal / Web UI (`/validation-demo`) | MongoDB rejecting an illegal document (e.g., invalid category or missing location) with `Document failed validation`. |
| 05 | `05_crud_create.png` | Web UI (`/report`) or CLI Option 3 | Item creation form submitted and confirmed in MongoDB. |
| 06 | `06_crud_read_browse.png` | Web UI (`/browse`) or CLI Option 2 | Table view of filtered items matching category/location. |
| 07 | `07_crud_update.png` | Web UI (`/browse`) or mongosh | Changing status from `open` to `matched` or `resolved`. |
| 08 | `08_crud_delete.png` | Web UI (`/browse`) or CLI Option 5 | Deletion confirmation message of a test item. |
| 09 | `09_aggregation_category.png` | Web UI (`/analytics`) or mongosh | Pipeline 1: Group by category output table. |
| 10 | `10_aggregation_hotspots.png` | Web UI (`/analytics`) or mongosh | Pipeline 2: Top campus location hotspots table. |
| 11 | `11_aggregation_resolution.png` | Web UI (`/analytics`) or mongosh | Pipeline 3: Lost vs Found resolution rate percentage. |
| 12 | `12_application_dashboard.png` | Web UI (`http://127.0.0.1:5000/`) | Full dashboard view with metric cards and recent items. |
| 13 | `13_automated_tests.png` | Terminal: `python tests/test_database.py` | 14 test cases running and printing `OK`. |

---

## Actual Terminal Output Examples (Verifiable Reference)

### 1. Database Seeding Output (`python scripts/seed_data.py`)

```text
============================================================
  FINDBACK DATABASE SEEDING PROCESS
============================================================
============================================================
  FINDBACK DATABASE SETUP & SCHEMA VALIDATION INITIALIZER
============================================================
[*] Target Database: campus_findback
[*] Existing Collections: []
[+] Creating 'users' collection with $jsonSchema validation...
[+] Creating indexes for 'users'...
[+] Creating 'items' collection with $jsonSchema validation...
[+] Creating indexes for 'items'...
[V] Database collections, $jsonSchema rules, and indexes set up successfully!
============================================================
[*] Loaded 12 users and 40 items from sample_data.json
[+] Inserting 12 users...
[V] Successfully inserted 12 users.
[+] Inserting 40 items...
[V] Successfully inserted 40 items.
============================================================
[V] DATABASE SEEDING COMPLETED SUCCESSFULLY!
    - Database Name: campus_findback
    - Total Users:   12
    - Total Items:   40
============================================================
```

---

### 2. Validation Demonstration Output (`python scripts/demo_validation.py`)

```text
======================================================================
  FINDBACK MONGODB $jsonSchema VALIDATION DEMONSTRATION
======================================================================

[TEST 1] Inserting a FULLY VALID document...
  [RESULT] SUCCESS! Document inserted with _id: 6abf8d0558d28d5dafef9159
  [EXPLANATION] All required fields present, valid types, category & type match enums.

[TEST 2] Inserting document with INVALID CATEGORY ('Weapons_Or_Illegal')...
  [RESULT] REJECTED BY MONGODB as expected!
  [ERROR DETAILS] Document failed validation
  [VIVA EXPLANATION] MongoDB $jsonSchema specifies category enum: ['Electronics', 'Books', ...].
                   The value 'Weapons_Or_Illegal' was rejected.

[TEST 3] Inserting document MISSING REQUIRED FIELD ('location')...
  [RESULT] REJECTED BY MONGODB as expected!
  [ERROR DETAILS] Document failed validation
  [VIVA EXPLANATION] 'location' is listed in required: [...] array in $jsonSchema.
                   MongoDB refused to insert document without location.

[TEST 4] Inserting document with ILLEGAL STATUS ('in_progress')...
  [RESULT] REJECTED BY MONGODB as expected!
  [ERROR DETAILS] Document failed validation
  [VIVA EXPLANATION] 'status' must be one of: ['open', 'matched', 'resolved', 'closed'].

======================================================================
  VALIDATION TEST SUITE PASSED ALL ENFORCEMENT CHECKS
======================================================================
```

---

### 3. Automated Test Execution Output (`python tests/test_database.py`)

```text
test_01_connection_ping (__main__.TestFindBackDatabase.test_01_connection_ping)
Test MongoDB server ping. ... ok
test_02_validation_valid_insert (__main__.TestFindBackDatabase.test_02_validation_valid_insert)
Valid document must be accepted by MongoDB schema validator. ... ok
test_03_validation_invalid_category_rejected (__main__.TestFindBackDatabase.test_03_validation_invalid_category_rejected)
Document with illegal category enum must be rejected by MongoDB. ... ok
test_04_validation_missing_location_rejected (__main__.TestFindBackDatabase.test_04_validation_missing_location_rejected)
Document missing required field 'location' must be rejected. ... ok
test_05_crud_create_read (__main__.TestFindBackDatabase.test_05_crud_create_read)
Test CREATE (insertOne) and READ (findOne). ... ok
test_06_crud_search_and_filter (__main__.TestFindBackDatabase.test_06_crud_search_and_filter)
Test search query filters. ... ok
test_07_crud_update_status (__main__.TestFindBackDatabase.test_07_crud_update_status)
Test UPDATE (updateOne) status lifecycle change. ... ok
test_08_crud_delete (__main__.TestFindBackDatabase.test_08_crud_delete)
Test DELETE (deleteOne). ... ok
test_09_aggregation_category (__main__.TestFindBackDatabase.test_09_aggregation_category)
Test Aggregation Pipeline 1: Group by Category. ... ok
test_10_aggregation_location (__main__.TestFindBackDatabase.test_10_aggregation_location)
Test Aggregation Pipeline 2: Hotspots by Location. ... ok
test_11_aggregation_resolution_rate (__main__.TestFindBackDatabase.test_11_aggregation_resolution_rate)
Test Aggregation Pipeline 3: Lost vs Found Breakdown. ... ok
test_12_aggregation_status_distribution (__main__.TestFindBackDatabase.test_12_aggregation_status_distribution)
Test Aggregation Pipeline 4: Status Breakdown. ... ok
test_13_aggregation_open_electronics (__main__.TestFindBackDatabase.test_13_aggregation_open_electronics)
Test Aggregation Pipeline 5: Open Electronics Hotspots. ... ok
test_14_aggregation_cross_collection_lookup (__main__.TestFindBackDatabase.test_14_aggregation_cross_collection_lookup)
Test Aggregation Pipeline 6: Cross-Collection $lookup with Users. ... ok

----------------------------------------------------------------------
Ran 14 tests in 0.228s

OK
```
