# FindBack — Presentation Guide & Live Demo Flow

This guide provides a structured 10-slide presentation blueprint, word-for-word talking points, and a 5–7 minute live demonstration script tailored for your MongoDB CA-2 evaluation.

---

# 10-Slide Presentation Structure

```
Slide 1: Project Title & Team
Slide 2: Problem Statement & Motivation
Slide 3: Proposed Solution — FindBack
Slide 4: Technology Stack & System Architecture
Slide 5: MongoDB Document & Collection Design
Slide 6: Collection Validation ($jsonSchema)
Slide 7: CRUD Operations Implementation
Slide 8: MongoDB Aggregation Pipelines
Slide 9: PyMongo Integration & Application Demo
Slide 10: Conclusion, Limitations & Future Scope
```

---

## Slide 1: Project Title & Overview
- **Visual:** Project title ("FindBack — Campus Lost & Found Intelligence System"), your name, roll number, course ("MongoDB CA-2"), and university details.
- **What to Say:**
  > *"Good morning respected faculty and examiner. Today, I am presenting FindBack — a campus lost and found intelligence system built from scratch using MongoDB, Python, and PyMongo."*
- **Key Points:** Real-world problem, MongoDB-first design, strict data integrity.

---

## Slide 2: Problem Statement & Motivation
- **Visual:** Comparison diagram between traditional manual logbooks/chat groups vs. centralized database.
- **What to Say:**
  > *"On any college campus, hundreds of personal possessions are misplaced every month. Traditional physical registers lack searchability, have no status tracking, and provide zero analytical insight into campus loss hotspots. FindBack solves this by providing a queryable, validated, and analytical platform."*
- **Key Points:** Data loss, duplication, lack of analytics.

---

## Slide 3: Proposed Solution — FindBack
- **Visual:** Feature matrix: Report Lost/Found, Multi-criteria Search, Status Lifecycle, Aggregation Analytics.
- **What to Say:**
  > *"FindBack allows students and security staff to file reports, filter by category and location, transition statuses from open to resolved, and automatically compute loss hotspots and recovery rates using MongoDB aggregation pipelines."*

---

## Slide 4: Technology Stack & System Architecture
- **Visual:** Architecture diagram showing: `User Interface -> Python / PyMongo -> MongoDB Engine (campus_findback)`.
- **What to Say:**
  > *"Our architecture is clean and robust. The presentation layer connects via PyMongo to MongoDB running on port 27017. We utilize two collections: users and items, protected by native JSON Schema validation rules."*

---

## Slide 5: MongoDB Document Design
- **Visual:** JSON snippet of an item document (`item_id`, `item_name`, `category`, `type`, `location`, `status`, `reward`, `tags`, `timestamps`).
- **What to Say:**
  > *"We chose MongoDB's document model because lost and found items possess varied attributes like keyword tags and optional rewards. A document model stores these self-contained records without requiring complex multiple-table joins."*

---

## Slide 6: Collection Validation (`$jsonSchema`)
- **Visual:** Code snippet of `$jsonSchema` validator showing `required` fields and `enum` arrays for `category`, `type`, and `status`.
- **What to Say:**
  > *"To ensure data integrity, we implemented MongoDB $jsonSchema validation with strict error actions. If an insertion lacks a required field like location or uses an invalid category, MongoDB rejects it at the database engine level."*

---

## Slide 7: CRUD Operations Implementation
- **Visual:** Table mapping CRUD operations to MongoDB commands (`insertOne`, `find`, `updateOne`, `deleteOne`).
- **What to Say:**
  > *"We implemented all core CRUD operations: insertOne for single reports, compound find queries with regex for search, updateOne with $set to update statuses, and deleteOne to remove incorrect entries."*

---

## Slide 8: MongoDB Aggregation Pipelines
- **Visual:** Diagram of the 6 aggregation pipelines (`$group`, `$sort`, `$match`, `$project`, `$limit`, `$lookup`).
- **What to Say:**
  > *"Aggregation is the analytical core of FindBack. We built 6 multi-stage pipelines that run in-database to calculate category distributions, campus location hotspots, and resolution rate percentages."*

---

## Slide 9: PyMongo Integration & Live Demo
- **Visual:** Screenshots of Terminal CLI and Flask Web UI.
- **What to Say:**
  > *"Through PyMongo, Python handles user input and executes these MongoDB commands directly. Let us now move to the live demonstration of the system."*

---

## Slide 10: Conclusion & Future Scope
- **Visual:** Summary bullet points: Complete CA-2 requirements met, 14 automated tests passed, future integration with GridFS for photo uploads.
- **What to Say:**
  > *"In conclusion, FindBack demonstrates full document modeling, schema validation, CRUD operations, and multi-stage aggregation pipelines. Thank you, and I am now ready for questions."*

---

# 5–7 Minute Live Demo Script

Follow this step-by-step sequence during your evaluation:

### Step 1: Show MongoDB Database & Collections (1 min)
1. Open MongoDB Compass or `mongosh`.
2. Run `use campus_findback; db.items.countDocuments();` (Shows 40 seeded documents).
3. Explain the collection structure and fields.

### Step 2: Demonstrate Validation Enforcement (1 min)
1. Run `python scripts/demo_validation.py` (or open Web UI `/validation-demo`).
2. Show Test 1 passing (valid document).
3. Show Test 2 & 3 failing (invalid category / missing location rejected by MongoDB).

### Step 3: Demonstrate CRUD Operations (2 min)
1. **Create:** Add a new lost item via Web UI (`/report`) or CLI (Option 3).
2. **Read:** Search for the item in `/browse` using a keyword or category filter.
3. **Update:** Change the item status from `open` to `matched` or `resolved`.
4. **Delete:** Delete a temporary test item and show the deletion confirmation.

### Step 4: Demonstrate Aggregation Pipelines (1.5 min)
1. Open Web UI (`/analytics`) or CLI (Option 6).
2. Point out **Pipeline 1** (Category Distribution: Electronics is #1).
3. Point out **Pipeline 2** (Location Hotspots: Sports Complex & Central Library have the highest reports).
4. Point out **Pipeline 3** (Resolution rate percentage for Lost vs. Found).

### Step 5: Run Automated Tests (30 sec)
1. Run `python tests/test_database.py`.
2. Show all 14 tests passing (`OK`).
