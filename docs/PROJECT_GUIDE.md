# FindBack — Campus Lost & Found Intelligence System
## Complete Project Understanding & Viva Master Guide

---

# 1. Project Introduction

### What are we building?
We are building **FindBack**, a specialized, database-driven lost-and-found management and intelligence system designed for university campuses. It allows students, faculty, and administrative staff to report lost items, register found items, search and filter through reports, update report statuses (e.g., from `open` to `matched` and `resolved`), and run meaningful analytical aggregations.

### Why did we select this problem?
On a typical college campus, hundreds of items (smartphones, calculators, notebooks, ID cards, keys, water bottles) are misplaced daily. Traditional paper logbooks at security desks or disorganized WhatsApp/Telegram groups suffer from:
1. No centralized search capabilities.
2. High duplication of records.
3. Zero analytical insight into where and why items are lost.
4. Inability to track whether an item was successfully returned to its owner.

### Who would use it?
- **Students & Faculty:** To quickly report missing possessions or log items found in classrooms and labs.
- **Campus Security & Helpdesk Staff:** To verify ownership, match claims, and close cases.
- **Campus Administration:** To analyze loss hotspots (e.g., Central Library, Cafeteria, Sports Complex) and allocate security or storage lockers accordingly.

---

# 2. Problem Statement

> *"Campus communities lack a centralized, structured, and queryable system to manage lost and found property. Existing manual registries lack data integrity, real-time status tracking, and analytical capabilities. FindBack addresses this by implementing a document-oriented database architecture in MongoDB, providing strict schema validation, rapid multi-criteria querying, and multi-stage aggregation analytics for campus lost-and-found intelligence."*

---

# 3. Proposed Solution

FindBack provides an end-to-end, lightweight solution consisting of:
1. **MongoDB Database (`campus_findback`):** Flexible, high-performance document store with strict `$jsonSchema` validation rules.
2. **PyMongo Integration Layer:** Python-to-MongoDB driver executing validated CRUD operations and aggregation pipelines.
3. **Interactive Demonstration Interfaces:**
   - **Terminal CLI (`app/cli.py`):** Fast, menu-driven command line tool for live query demonstrations during viva.
   - **Web UI (`app/web_app.py`):** Clean Flask-based dashboard, reporting forms, search filters, and analytics dashboard.

---

# 4. Why MongoDB?

During your viva, you will likely be asked: **"Why did you choose MongoDB over a relational database like MySQL?"**

| Criteria | Relational Database (SQL/MySQL) | MongoDB (Document Database) | Why FindBack Chose MongoDB |
| :--- | :--- | :--- | :--- |
| **Data Format** | Rigid tables, rows, fixed columns | Flexible JSON/BSON documents | Lost/found items have varied attributes (electronics have serials, books have editions, keys have tags). Documents accommodate diverse fields naturally. |
| **Schema Evolution** | Requires disruptive `ALTER TABLE` migrations | Dynamic schema with optional `$jsonSchema` | Easy to add new fields (e.g., `reward`, `tags`, image URLs) without altering entire tables. |
| **Complex Attributes** | Requires separate lookup tables and `JOIN`s for arrays (e.g., `tags`) | Native support for nested arrays and embedded sub-documents | Search tags (`["laptop", "dell", "silver"]`) are stored directly inside the document. |
| **Aggregation Framework** | Complex nested SQL queries and `GROUP BY` | Native multi-stage aggregation pipelines (`$group`, `$match`, `$sort`, `$project`) | Clean, intuitive data processing pipelines for campus hotspot analysis. |

---

# 5. Why PyMongo?

**PyMongo** is the official, idiomatic Python distribution for MongoDB.
1. **Direct Translation:** Python dictionaries (`dict`) and lists (`list`) map 1-to-1 with MongoDB BSON documents and arrays.
2. **Native Driver Performance:** Handles connection pooling, socket management, and failover automatically through `MongoClient`.
3. **Query Transparency:** PyMongo queries look almost identical to native `mongosh` commands, making it easy to explain both in Python and in MongoDB Shell.

---

# 6. System Architecture

```
+-------------------------------------------------------------+
|                        USER INTERFACE                       |
|   Terminal Interactive CLI (cli.py) / Web UI (Flask)        |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                   PYTHON APPLICATION LAYER                  |
|    app/models.py  |  app/crud.py  |  app/analytics.py       |
+-------------------------------------------------------------+
                              |
                              v (PyMongo Driver: MongoClient)
+-------------------------------------------------------------+
|                    MONGODB DATABASE ENGINE                  |
|                    Database: campus_findback                |
|                                                             |
|   +--------------------------+  +------------------------+  |
|   |   Collection: users      |  |   Collection: items    |  |
|   |   - $jsonSchema validator|  |   - $jsonSchema rules  |  |
|   |   - Unique Index user_id |  |   - Compound text idx  |  |
|   +--------------------------+  +------------------------+  |
+-------------------------------------------------------------+
```

---

# 7. Database Design & Collections

The database is named **`campus_findback`**. It contains two collections:

### 1. Collection: `users`
Represents registered students, faculty, and campus staff who report or claim items.

| Field Name | BSON Type | Required | Description / Purpose |
| :--- | :--- | :---: | :--- |
| `_id` | `ObjectId` | Yes (Auto) | Unique internal MongoDB primary key. |
| `user_id` | `string` | Yes | Unique human-readable user ID (e.g., `USR-101`). |
| `name` | `string` | Yes | Full name of the campus member (min length: 2). |
| `email` | `string` | Yes | Campus email address validated with regex pattern. |
| `role` | `string` | Yes | Enum: `student`, `faculty`, `staff`, `admin`. |
| `department` | `string` | Yes | Academic or administrative department. |
| `phone` | `string` | No | Contact phone number. |
| `created_at` | `date` | Yes | Timestamp of account registration. |

### 2. Collection: `items`
Represents every lost or found item report on campus.

| Field Name | BSON Type | Required | Description / Purpose |
| :--- | :--- | :---: | :--- |
| `_id` | `ObjectId` | Yes (Auto) | Unique internal MongoDB primary key. |
| `item_id` | `string` | Yes | Unique reference identifier (e.g., `ITEM-2026-001`). |
| `item_name` | `string` | Yes | Title/name of the item (e.g., `Dell Inspiron 15`). |
| `category` | `string` | Yes | Enum: `Electronics`, `Books`, `Stationery`, `Clothing`, `Accessories`, `ID/Documents`, `Other`. |
| `type` | `string` | Yes | Enum: `lost` or `found`. |
| `description`| `string` | Yes | Physical description, color, distinguishing marks (min length: 5). |
| `location` | `string` | Yes | Campus location where item was lost or found. |
| `date_reported` | `date` | Yes | Timestamp when the incident occurred or was logged. |
| `status` | `string` | Yes | Lifecycle status enum: `open`, `matched`, `resolved`, `closed`. |
| `reported_by`| `string` | Yes | Reference to reporter's `user_id` (e.g., `USR-101`). |
| `contact_email` | `string`| No | Direct email for notification updates. |
| `contact_phone` | `string`| No | Phone number for rapid claiming. |
| `reward` | `number` | No | Optional monetary reward offered (>= 0). |
| `tags` | `array` | No | Array of keyword tags for flexible search (`["blue", "laptop"]`). |
| `created_at` | `date` | Yes | Document creation timestamp. |
| `updated_at` | `date` | Yes | Last modification timestamp. |

---

# 8. Why Document-Based Design?

1. **Self-Contained Records:** An item document contains all necessary attributes (tags, category, status, reward, reporter ID) in one place. No complex joins are needed for daily operations.
2. **Array Handling:** Fields like `tags: ["apple", "macbook", "silver"]` are first-class citizens in MongoDB, searchable via simple queries (`tags: "apple"`).
3. **Audit Trail Support:** Storing `created_at` and `updated_at` alongside status transitions allows simple tracking of report lifecycles.

---

# 9. MongoDB Validation (`$jsonSchema`)

### What is collection validation?
Collection validation allows MongoDB to enforce data quality and structural rules directly inside the database engine. Even if an application bug attempts to insert bad data, MongoDB rejects it.

### How `$jsonSchema` works in FindBack:
1. **Required Fields Check:** Ensures mandatory fields like `item_id`, `item_name`, `category`, `type`, `location`, `status`, and `reported_by` are never omitted.
2. **Data Type Enforcement:** `item_name` must be a string, `created_at` must be a date, `reward` must be a number >= 0.
3. **Enum Whitelisting:**
   - `type` must strictly be either `'lost'` or `'found'`.
   - `status` must strictly be one of: `'open'`, `'matched'`, `'resolved'`, `'closed'`.
   - `category` must strictly match one of the 7 predefined categories.

### Live Demonstration Example:
When you run `python scripts/demo_validation.py`:
- A document with `category: "Weapons_Or_Illegal"` is rejected with `Document failed validation`.
- A document missing the `location` field is rejected immediately by the database.

---

# 10. CRUD Operations Explained

### 1. CREATE (Insert)
- **Single Insert:** `db.items.insertOne(document)`
- **Batch Insert:** `db.items.insertMany([doc1, doc2])`
- **Purpose:** Registers new lost or found property.

### 2. READ (Find & Query)
- **Find All with Projection:** `db.items.find({ type: "lost" }, { item_name: 1, location: 1, _id: 0 })`
- **Exact Match:** `db.items.findOne({ item_id: "ITEM-2026-001" })`
- **Comparison & Logical Query:** `db.items.find({ location: "Central Library", reward: { $gte: 200 } })`
- **Text / Regex Search:** `db.items.find({ item_name: { $regex: "calculator", $options: "i" } })`

### 3. UPDATE (Modify)
- **Single Update:** `db.items.updateOne({ item_id: "ITEM-2026-001" }, { $set: { status: "resolved", updated_at: new Date() } })`
- **Batch Tagging:** `db.items.updateMany({ type: "found", status: "open" }, { $addToSet: { tags: "unclaimed" } })`

### 4. DELETE (Remove)
- **Single Deletion:** `db.items.deleteOne({ item_id: "ITEM-2026-041" })`
- **Batch Cleanup:** `db.items.deleteMany({ status: "closed", created_at: { $lt: oneYearAgo } })`

---

# 11. Aggregation Pipelines Explained (All 6 Pipelines)

Aggregation in MongoDB is a multi-stage pipeline where documents enter stage 1, are filtered/transformed, and pass to subsequent stages.

### Pipeline 1: Reports Grouped by Item Category
- **Question:** Which categories of items are reported most frequently?
- **Pipeline Stages:**
  1. `$group`: Groups by `category`, counts total records using `$sum: 1`, and uses conditional `$cond` to count lost vs found.
  2. `$project`: Formats fields and drops internal `_id`.
  3. `$sort`: Orders by `total_reports: -1` (descending).

### Pipeline 2: Top Campus Location Hotspots
- **Question:** Which locations on campus have the highest loss/found activity and open items?
- **Pipeline Stages:**
  1. `$group`: Groups by `location`, sums total reports and counts open/matched items.
  2. `$project`: Renames output fields.
  3. `$sort`: Highest report count first.
  4. `$limit`: Returns top 5 hotspot areas.

### Pipeline 3: Lost vs Found Resolution Rate
- **Question:** What percentage of lost items and found items get successfully returned to owners?
- **Pipeline Stages:**
  1. `$group`: Groups by `type` (`lost` vs `found`), sums total and resolved counts.
  2. `$project`: Calculates percentage using `$multiply`, `$divide`, and rounds to 1 decimal place with `$round`.
  3. `$sort`: Orders by `total_items` descending.

### Pipeline 4: Lifecycle Status Distribution
- **Question:** How many reports are currently `open`, `matched`, `resolved`, or `closed`?
- **Pipeline Stages:**
  1. `$group`: Groups by `status` and counts occurrences.
  2. `$sort`: Sorts in descending order of count.

### Pipeline 5: Open High-Value Electronics Hotspots
- **Question:** Where are high-value unclaimed Electronics located and what is the average reward offered?
- **Pipeline Stages:**
  1. `$match`: Filters only documents where `category == "Electronics"` AND `status == "open"`.
  2. `$group`: Groups by `location`, counts open electronics, and computes `$avg: "$reward"`.
  3. `$sort`: Orders by count descending.

### Pipeline 6: Cross-Collection Join (`$lookup`)
- **Question:** Who reported open lost items? (Combine item details with student/faculty department).
- **Pipeline Stages:**
  1. `$match`: Filters for open lost items.
  2. `$lookup`: Joins with `users` collection matching `items.reported_by` == `users.user_id`.
  3. `$unwind`: Deconstructs the joined array into a single user object.
  4. `$project`: Extracts reporter's name, department, and role.
  5. `$limit`: Shows top results.

---

# 12. PyMongo Implementation Summary

```python
from pymongo import MongoClient

# 1. Connect
client = MongoClient("mongodb://localhost:27017/")
db = client["campus_findback"]
items = db["items"]

# 2. Insert
result = items.insert_one({"item_id": "ITEM-101", "item_name": "Calculator", ...})

# 3. Read
doc = items.find_one({"item_id": "ITEM-101"})

# 4. Update
items.update_one({"item_id": "ITEM-101"}, {"$set": {"status": "resolved"}})

# 5. Delete
items.delete_one({"item_id": "ITEM-101"})

# 6. Aggregate
pipeline = [{"$group": {"_id": "$category", "total": {"$sum": 1}}}]
results = list(items.aggregate(pipeline))
```

---

# 13. Complete Application Flow

1. **User files a report:** The user submits a form on the web UI or CLI.
2. **Python prepares document:** Adds UTC timestamps (`created_at`, `updated_at`), formats data.
3. **PyMongo sends to MongoDB:** PyMongo executes `insert_one(document)`.
4. **MongoDB engine validates:** MongoDB checks `$jsonSchema` rules (types, required fields, enums).
5. **Database commits:** Document is stored on disk with a unique `_id` and indexed in B-trees.
6. **Analytics generation:** Dashboard triggers `aggregate(pipeline)` which processes collections in memory and returns aggregated metric summaries.

---

# 14. Important Code Files Overview

- [app/database.py](file:///d:/ca-2%20mongodb/app/database.py): Manages `MongoClient`, database connections, and server ping checks.
- [app/models.py](file:///d:/ca-2%20mongodb/app/models.py): Defines `$jsonSchema` validator dictionaries, category enums, and document constructors.
- [app/crud.py](file:///d:/ca-2%20mongodb/app/crud.py): Contains clean CRUD functions (`create_item`, `get_items`, `search_items`, `update_item_status`, `delete_item`).
- [app/analytics.py](file:///d:/ca-2%20mongodb/app/analytics.py): Executes the 6 PyMongo aggregation pipelines.
- [app/cli.py](file:///d:/ca-2%20mongodb/app/cli.py): Terminal interface for live viva demonstration.
- [app/web_app.py](file:///d:/ca-2%20mongodb/app/web_app.py): Flask web server with dashboard, forms, and analytics.
- [mongodb/validation.js](file:///d:/ca-2%20mongodb/mongodb/validation.js): Native mongosh schema validation script.
- [mongodb/crud_queries.js](file:///d:/ca-2%20mongodb/mongodb/crud_queries.js): Native mongosh CRUD query examples.
- [mongodb/aggregation_queries.js](file:///d:/ca-2%20mongodb/mongodb/aggregation_queries.js): Native mongosh aggregation pipelines.
- [scripts/seed_data.py](file:///d:/ca-2%20mongodb/scripts/seed_data.py): Seeds 40 items and 12 users into MongoDB.
- [tests/test_database.py](file:///d:/ca-2%20mongodb/tests/test_database.py): 14 unit and integration tests.

---

# 15. Why We Chose This Database Structure

- **Two Collections (`users` and `items`):** Separates campus member identity from individual property reports, avoiding duplication of user profile details.
- **Embedded Arrays (`tags`):** Enables multi-keyword search without creating separate mapping tables.
- **Reference Linking (`reported_by` -> `user_id`):** Keeps item documents lightweight while allowing cross-collection joins (`$lookup`) when reporter details are required.

---

# 16. Testing Methodology

1. **Automated Unit & Integration Tests:** 14 automated test cases in `tests/test_database.py` verifying ping, valid insertion, validation rejection, CRUD, and all 6 aggregation pipelines.
2. **Schema Rejection Verification:** Dedicated script `scripts/demo_validation.py` explicitly tests invalid enums and missing required fields.
3. **Native Shell Testing:** Verified scripts run inside `mongosh` independently of Python.

---

# 17. Common Troubleshooting Scenarios

- **Error: `ServerSelectionTimeoutError: No replica set members match selector`**
  - *Cause:* MongoDB service is stopped.
  - *Fix:* Start MongoDB service via Windows Services or run `mongod` in a terminal.
- **Error: `WriteError: Document failed validation`**
  - *Cause:* An inserted document is missing a required field or has an illegal enum value.
  - *Fix:* Ensure document contains all required fields (`item_id`, `item_name`, `category`, `type`, `location`, `status`, `reported_by`) and values match allowed enums.

---

# 18. Project Limitations

1. **Campus-Scoped:** Designed for single university campus environments.
2. **Manual Status Transition:** Requires staff/students to manually mark items as `matched` or `resolved`.
3. **No Image Uploads:** Uses descriptive text and search tags instead of binary image storage (GridFS) to keep the project clean and academic.

---

# 19. Future Scope

1. **Image Storage with GridFS:** Store item photos directly in MongoDB GridFS.
2. **Automated Match Scoring:** Implement weighted matching queries comparing tags, categories, and date ranges between lost and found items.
3. **Email/SMS Push Notifications:** Notify reporters automatically when a matching item is registered.

---

# 20. Summary Checklist for Viva

- [x] Database: `campus_findback` created and running.
- [x] Collections: `items` (40 docs) and `users` (12 docs).
- [x] Schema Validation: `$jsonSchema` enforcing required fields and enums.
- [x] CRUD Operations: `insertOne`, `insertMany`, `find`, `findOne`, `updateOne`, `updateMany`, `deleteOne`, `deleteMany`.
- [x] Aggregation: 6 multi-stage pipelines (`$group`, `$sort`, `$project`, `$match`, `$limit`, `$lookup`, `$avg`, `$sum`, `$cond`).
- [x] PyMongo: Fully integrated in Python application.
- [x] Interfaces: Both Terminal CLI and Flask Web UI available for demonstration.
