# ACADEMIC PROJECT REPORT

# FindBack — Campus Lost & Found Intelligence System
### MongoDB Course Continuous Assessment (CA-2)

---

## 1. Title of the Project
**FindBack — Campus Lost & Found Intelligence System**

---

## 2. Executive Summary / Abstract
FindBack is an academic lost-and-found management and analytical system engineered with MongoDB, Python, and PyMongo. The system streamlines reporting lost and found items on university campuses, prevents data corruption through strict MongoDB collection-level `$jsonSchema` validation, executes rapid multi-criteria CRUD queries, and generates actionable campus intelligence through multi-stage aggregation pipelines. The solution demonstrates document modeling, index optimization, query projections, and cross-collection joins (`$lookup`).

---

## 3. Problem Statement & Motivation
University campuses experience high daily volumes of misplaced items across libraries, laboratories, cafeterias, and auditoriums. Traditional manual logging on paper registers or unstructured social media groups suffers from poor searchability, record duplication, and an inability to track the resolution lifecycle. FindBack was developed to provide a centralized, structured, and queryable NoSQL database solution tailored to this operational challenge.

---

## 4. Project Objectives
1. Design a document-oriented database schema in MongoDB for campus lost-and-found records.
2. Implement and verify strict `$jsonSchema` collection validation rules and performance indexes.
3. Implement end-to-end CRUD operations in both native MongoDB Shell syntax and PyMongo.
4. Construct meaningful multi-stage aggregation pipelines for statistical insights (category ranking, location hotspots, resolution rates).
5. Develop dual user interfaces (Interactive Terminal CLI and Flask Web UI) for live demonstration.
6. Provide an automated test suite verifying all database operations.

---

## 5. Technology Stack

- **Database:** MongoDB Community Server (v8.0+)
- **Integration Driver:** PyMongo (v4.18+)
- **Programming Language:** Python 3.13+
- **Web Application Framework:** Flask 3.1+
- **Frontend / Styling:** Bootstrap 5, Bootstrap Icons
- **Terminal Formatting:** Tabulate, Colorama
- **Configuration:** Python-Dotenv

---

## 6. System Architecture

```
+-------------------------------------------------------------+
|                     PRESENTATION TIER                       |
|   Terminal CLI (app/cli.py)   |   Flask Web UI (web_app.py) |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                     APPLICATION LOGIC TIER                  |
|   Database Access (app/database.py)                         |
|   Schema Definitions (app/models.py)                        |
|   CRUD Operations Engine (app/crud.py)                      |
|   Aggregation Analytics Engine (app/analytics.py)           |
+-------------------------------------------------------------+
                              |
                              v (PyMongo Connection Pool)
+-------------------------------------------------------------+
|                     DATABASE TIER (MongoDB)                 |
|                     Database: campus_findback               |
|                                                             |
|   Collection: users (12 documents, $jsonSchema, indexes)    |
|   Collection: items (40 documents, $jsonSchema, indexes)    |
+-------------------------------------------------------------+
```

---

## 7. Database Design & Document Structures

### 7.1 Database: `campus_findback`

### 7.2 Collection: `users`
Stores campus community members.
```json
{
  "_id": "ObjectId(...)",
  "user_id": "USR-101",
  "name": "Aarav Sharma",
  "email": "aarav.sharma@campus.edu",
  "role": "student",
  "department": "Computer Science & Engineering",
  "phone": "+91-9876543210",
  "created_at": "ISODate(...)"
}
```

### 7.3 Collection: `items`
Stores lost and found property reports.
```json
{
  "_id": "ObjectId(...)",
  "item_id": "ITEM-2026-001",
  "item_name": "Dell Inspiron 15 Laptop (Silver)",
  "category": "Electronics",
  "type": "lost",
  "description": "Silver Dell Inspiron 15 with Linux sticker on top lid and black sleeve.",
  "location": "Central Library",
  "date_reported": "ISODate('2026-02-01T14:30:00Z')",
  "status": "open",
  "reported_by": "USR-101",
  "contact_email": "aarav.sharma@campus.edu",
  "contact_phone": "+91-9876543210",
  "reward": 500,
  "tags": ["laptop", "dell", "silver", "electronics"],
  "created_at": "ISODate('2026-02-01T14:35:00Z')",
  "updated_at": "ISODate('2026-02-01T14:35:00Z')"
}
```

---

## 8. Schema Validation Rules (`$jsonSchema`)

Implemented via `db.createCollection` with `validationLevel: 'strict'` and `validationAction: 'error'`.
- **Mandatory Fields:** `item_id`, `item_name`, `category`, `type`, `description`, `location`, `date_reported`, `status`, `reported_by`, `created_at`, `updated_at`.
- **Enums:**
  - `category`: `['Electronics', 'Books', 'Stationery', 'Clothing', 'Accessories', 'ID/Documents', 'Other']`
  - `type`: `['lost', 'found']`
  - `status`: `['open', 'matched', 'resolved', 'closed']`
- **Numeric Bounds:** `reward` >= 0.

---

## 9. CRUD Operations Implemented

| Operation | Method | Sample Command | Use Case |
|---|---|---|---|
| **Create** | `insertOne()` | `db.items.insertOne({...})` | Report individual item |
| **Create** | `insertMany()` | `db.items.insertMany([...])` | Batch seeding / multi-item log |
| **Read** | `find()` | `db.items.find({ category: "Electronics" })` | Category filter |
| **Read** | `findOne()` | `db.items.findOne({ item_id: "ITEM-2026-001" })` | Item lookup |
| **Update** | `updateOne()` | `db.items.updateOne({ item_id: "..." }, { $set: { status: "resolved" } })` | Status update |
| **Update** | `updateMany()` | `db.items.updateMany({ type: "found" }, { $addToSet: { tags: "unclaimed" } })` | Batch tag update |
| **Delete** | `deleteOne()` | `db.items.deleteOne({ item_id: "..." })` | Delete incorrect record |
| **Delete** | `deleteMany()` | `db.items.deleteMany({ status: "closed" })` | Archive cleanup |

---

## 10. Aggregation Pipelines

1. **Category Distribution:** Uses `$group` and `$sum` to compute total, lost, and found counts per category.
2. **Location Hotspot Analysis:** Identifies top 5 campus locations with highest reports using `$group`, `$sort`, and `$limit`.
3. **Resolution Rate Analytics:** Evaluates percentage of returned items using `$group`, `$project` with `$multiply`, `$divide`, and `$round`.
4. **Lifecycle Status Distribution:** Groups reports by `status` to monitor pending vs. closed cases.
5. **Open High-Value Electronics Analysis:** Combines `$match`, `$group`, and `$avg` to calculate average reward by location.
6. **Cross-Collection Join (`$lookup`):** Joins `items.reported_by` with `users.user_id` to link item reports with reporter department and role.

---

## 11. Results & Query Outputs

- Total Users Seeded: 12
- Total Items Seeded: 40
- Automated Tests: 14 passing out of 14 (100% pass rate).
- Native query execution verified in `mongosh` and through PyMongo.

---

## 12. Limitations & Future Scope

### Limitations
- Single-campus operational scope.
- Manual status resolution tracking.
- Text-based tags without binary image storage.

### Future Scope
- Image file storage using MongoDB GridFS.
- Automated match-scoring algorithm between lost and found items.
- Real-time automated email notifications on status changes.

---

## 13. Conclusion
The FindBack project comprehensively demonstrates core and advanced MongoDB capabilities, including document schema design, JSON Schema validation, indexed CRUD queries, and multi-stage aggregation pipelines integrated within a Python/PyMongo application. All CA-2 evaluation criteria are fulfilled.
