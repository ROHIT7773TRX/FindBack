# FindBack — Comprehensive Viva Preparation Guide
## 50+ Viva Questions & Answers + 20 Live Query Practice Tasks

---

# PART 1: 50+ VIVA QUESTIONS & ANSWERS

## A. Basic Project Questions

### Q1: What is your project and what problem does it solve?
**Answer:** My project is **FindBack — Campus Lost & Found Intelligence System**. It solves the problem of scattered, manual, and disorganized lost-and-found tracking on college campuses by providing a centralized MongoDB database where lost and found items can be reported, searched, updated, and analyzed using aggregation pipelines.

### Q2: Who are the primary users of FindBack?
**Answer:** Students, faculty members, campus security officers, library staff, and administrative management.

### Q3: Why did you choose this problem for your CA-2?
**Answer:** It is an authentic real-world problem that naturally fits MongoDB's document model—items have diverse attributes (tags, categories, locations, rewards), and campus management requires analytical reporting (hotspots, resolution rates) that showcase MongoDB aggregation pipelines.

### Q4: What are the main components of your project?
**Answer:**
1. A MongoDB database (`campus_findback`) with schema validation (`$jsonSchema`).
2. Two collections: `users` and `items`.
3. A Python backend utilizing PyMongo for database connectivity and CRUD/aggregation execution.
4. An interactive Terminal CLI and a clean Flask Web UI for demonstration.

---

## B. Core MongoDB Questions

### Q5: What is MongoDB?
**Answer:** MongoDB is a source-available, cross-platform, document-oriented NoSQL database system that stores data in flexible, JSON-like documents called BSON (Binary JSON).

### Q6: What is a MongoDB Document?
**Answer:** A document is a basic unit of data in MongoDB, composed of field-and-value pairs (similar to a JSON object or Python dictionary).

### Q7: What is a Collection?
**Answer:** A collection is a grouping of MongoDB documents, analogous to a table in a relational database, but without requiring all documents to share identical schemas.

### Q8: What is BSON?
**Answer:** BSON stands for *Binary JSON*. It is the binary-encoded serialization format used by MongoDB to store documents on disk and over the network. It extends JSON with additional data types like `Date`, `ObjectId`, `Decimal128`, and raw binary data.

### Q9: What is `_id` in a MongoDB document?
**Answer:** `_id` is the primary key required in every MongoDB document. If not explicitly provided during insertion, MongoDB automatically generates a 12-byte `ObjectId` consisting of a 4-byte timestamp, 5-byte random value, and 3-byte incrementing counter.

### Q10: How does MongoDB differ from Relational Databases (SQL)?
**Answer:**
- SQL stores structured data in fixed rows and columns across tables with strict foreign keys.
- MongoDB stores semi-structured or polymorphic data in dynamic BSON documents. It allows embedded arrays/sub-documents and scales horizontally through sharding.

### Q11: What is schema flexibility in MongoDB?
**Answer:** Schema flexibility means documents within the same collection do not need to possess identical fields or types. However, schema validation (`$jsonSchema`) can be enforced when data consistency is required.

---

## C. MongoDB Validation Questions (`$jsonSchema`)

### Q12: What is MongoDB collection validation?
**Answer:** It is a server-side mechanism that evaluates documents against validation rules whenever an insert or update operation is executed, preventing invalid data from entering the database.

### Q13: Why did you use `$jsonSchema`?
**Answer:** `$jsonSchema` uses the standardized JSON Schema specification to validate document structure, data types, required fields, string length, regex patterns, and enum values directly at the database engine layer.

### Q14: What fields are required in your `items` collection?
**Answer:** `item_id`, `item_name`, `category`, `type`, `description`, `location`, `date_reported`, `status`, `reported_by`, `created_at`, and `updated_at`.

### Q15: What is an enum in MongoDB schema validation?
**Answer:** An `enum` (enumeration) restricts a field's value to a fixed list of allowed strings. For example, `type` must be either `['lost', 'found']` and `status` must be `['open', 'matched', 'resolved', 'closed']`.

### Q16: What happens when an invalid document is inserted?
**Answer:** MongoDB throws a `WriteError` with the message `Document failed validation` and refuses to write the document to disk.

### Q17: What are `validationLevel` and `validationAction`?
**Answer:**
- `validationLevel`: Controls which documents are checked (`strict` checks all inserts and updates; `moderate` only checks existing valid documents).
- `validationAction`: Controls what happens on violation (`error` rejects the write; `warn` logs a warning but allows the write). We used `strict` and `error`.

---

## D. CRUD Operations Questions

### Q18: What is CRUD?
**Answer:** CRUD stands for Create, Read, Update, and Delete—the four foundational operations for persistent data storage.

### Q19: What is the difference between `insertOne()` and `insertMany()`?
**Answer:**
- `insertOne()` inserts a single document and returns `insertedId`.
- `insertMany()` takes an array of documents and inserts them in a single network batch, returning `insertedIds`.

### Q20: What is the difference between `find()` and `findOne()`?
**Answer:**
- `find()` returns a cursor pointing to all matching documents.
- `findOne()` returns the single first matching document or `None` if no match is found.

### Q21: What is a projection in MongoDB queries?
**Answer:** A projection specifies which fields should be included (`1`) or excluded (`0`) in the query result. For example: `db.items.find({}, { item_name: 1, location: 1, _id: 0 })`.

### Q22: What is the difference between `updateOne()` and `updateMany()`?
**Answer:**
- `updateOne()` modifies only the first document that satisfies the query filter.
- `updateMany()` modifies all documents that satisfy the query filter.

### Q23: Why do we use the `$set` operator in updates?
**Answer:** `$set` replaces only the specified fields without overwriting or replacing the entire document.

### Q24: How do you delete documents in MongoDB?
**Answer:**
- `deleteOne({ filter })` deletes the first matching document.
- `deleteMany({ filter })` deletes all matching documents.

### Q25: What is an index in MongoDB and why did you use it?
**Answer:** An index is a special data structure (B-tree) that stores a small portion of the collection's data to allow MongoDB to locate documents rapidly without scanning every document (collection scan / `COLLSCAN`). We indexed `item_id` (unique), `category`, `type`, `status`, `location`, and a text index for full-text search.

---

## E. Aggregation Framework Questions

### Q26: What is MongoDB Aggregation?
**Answer:** Aggregation is a framework for data processing where documents pass through a multi-stage pipeline that transforms, filters, groups, and computes metrics on the documents.

### Q27: Why use Aggregation instead of fetching all documents and computing in Python?
**Answer:** Aggregation runs natively inside the database engine in C++, which is significantly faster, utilizes database indexes, and transfers only the aggregated summary across the network rather than millions of raw documents.

### Q28: What does `$match` do?
**Answer:** `$match` filters documents to allow only those matching the specified criteria to pass to the next stage in the pipeline (analogous to SQL `WHERE`).

### Q29: What does `$group` do?
**Answer:** `$group` separates documents into groups according to a specified group key (`_id`) and applies accumulator expressions (`$sum`, `$avg`, `$max`) to calculate summary statistics for each group (analogous to SQL `GROUP BY`).

### Q30: What does `$project` do?
**Answer:** `$project` reshapes documents, selecting specific fields, renaming fields, or computing new derived values using mathematical operators.

### Q31: What does `$sort` and `$limit` do?
**Answer:**
- `$sort` orders documents (`1` for ascending, `-1` for descending).
- `$limit` restricts the number of documents passed to the next stage or final output.

### Q32: What does `$lookup` do?
**Answer:** `$lookup` performs a left outer join between two collections within the same database, attaching matching documents from a foreign collection as an array field.

### Q33: What does `$unwind` do?
**Answer:** `$unwind` deconstructs an array field from input documents to output a document for each element in the array.

### Q34: Explain your most complex aggregation pipeline.
**Answer:** Aggregation 3 (Lost vs Found Resolution Rate) groups by `type`, counts total items and resolved items using conditional summation (`$cond`), then uses `$project` with mathematical expressions (`$multiply` and `$divide`) and `$round` to compute the exact recovery percentage per report type.

---

## F. PyMongo Questions

### Q35: What is PyMongo?
**Answer:** PyMongo is the official Python client library for interacting with MongoDB instances.

### Q36: How do you establish a connection to MongoDB in PyMongo?
**Answer:**
```python
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["campus_findback"]
```

### Q37: What does `MongoClient` do?
**Answer:** It creates and maintains a connection pool to the MongoDB server, handles server discovery, monitoring, authentication, and thread-safe request dispatching.

### Q38: How do you access a database and collection in PyMongo?
**Answer:**
Using attribute or dictionary notation:
```python
db = client.campus_findback  # or client["campus_findback"]
items_col = db.items         # or db["items"]
```

### Q39: How do you execute an aggregation pipeline in PyMongo?
**Answer:**
```python
pipeline = [
    {"$group": {"_id": "$category", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]
cursor = db.items.aggregate(pipeline)
results = list(cursor)
```

### Q40: How does PyMongo handle ObjectId conversion for web APIs?
**Answer:** MongoDB's `ObjectId` is not natively JSON serializable. We convert it to a string using `str(doc["_id"])` or exclude it in projections (`{"_id": 0}`).

---

## G. Project-Specific Viva Questions

### Q41: Why did you create two collections instead of one?
**Answer:** `users` stores user profile info (name, department, email, role), while `items` stores reports. Normalizing users avoids duplicating department and contact details across multiple item reports.

### Q42: Why is `status` stored in the item document?
**Answer:** Storing `status` directly inside the item document allows instant filtering of active reports (`open` / `matched`) and fast index lookups without cross-collection joins.

### Q43: How do you find all unresolved items in MongoDB?
**Answer:**
`db.items.find({ status: { $in: ["open", "matched"] } })`

### Q44: How would you find all Electronics reported lost in 'Central Library'?
**Answer:**
`db.items.find({ category: "Electronics", type: "lost", location: "Central Library" })`

### Q45: How would you modify the hotspot query to show only the top 3 locations?
**Answer:** Add `{ $limit: 3 }` as the final stage of the aggregation pipeline.

### Q46: How do you add a tag to an existing item's tag array?
**Answer:**
`db.items.updateOne({ item_id: "ITEM-2026-001" }, { $addToSet: { tags: "unclaimed" } })`

### Q47: What does `$addToSet` do compared to `$push`?
**Answer:** `$addToSet` adds an element to an array only if it does not already exist (prevents duplicates), whereas `$push` always appends the element.

### Q48: How do you calculate the total reward offered across all open lost items?
**Answer:**
```javascript
db.items.aggregate([
  { $match: { type: "lost", status: "open" } },
  { $group: { _id: null, totalReward: { $sum: "$reward" } } }
])
```

### Q49: What is the purpose of `seed_data.py`?
**Answer:** It populates the database with 12 realistic users and 40 lost/found items with valid timestamps and categories so queries and aggregations return meaningful statistical results.

### Q50: How do you know your `$jsonSchema` validation actually works?
**Answer:** We executed `scripts/demo_validation.py` and unit tests in `tests/test_database.py`, confirming that invalid categories, missing required fields, and illegal statuses are rejected by MongoDB with `Document failed validation`.

---

# PART 2: "QUERIES I SHOULD BE ABLE TO WRITE DURING VIVA"

## Section 1: Practice Tasks with Solution & Explanation

### Task 1: Find all lost items.
```javascript
db.items.find({ type: "lost" })
```
*Explanation:* Simple query filter matching the `type` field value `"lost"`.

---

### Task 2: Find all found items with only their name, location, and date reported.
```javascript
db.items.find(
  { type: "found" },
  { item_name: 1, location: 1, date_reported: 1, _id: 0 }
)
```
*Explanation:* Uses projection (second argument) to include only specified fields and suppress `_id`.

---

### Task 3: Find all items in the 'Electronics' category that are still 'open'.
```javascript
db.items.find({ category: "Electronics", status: "open" })
```
*Explanation:* Implicit `AND` condition between `category` and `status`.

---

### Task 4: Find items with a reward greater than or equal to ₹200.
```javascript
db.items.find({ reward: { $gte: 200 } })
```
*Explanation:* `$gte` comparison operator for numbers greater than or equal to 200.

---

### Task 5: Find items reported in either 'Central Library' OR 'Sports Complex'.
```javascript
db.items.find({ location: { $in: ["Central Library", "Sports Complex"] } })
```
*Explanation:* `$in` matches any value in the provided array.

---

### Task 6: Find a single item by its unique ID (`ITEM-2026-001`).
```javascript
db.items.findOne({ item_id: "ITEM-2026-001" })
```
*Explanation:* `findOne()` returns the single matching document.

---

### Task 7: Find items containing the keyword "calculator" in the item name (case-insensitive).
```javascript
db.items.find({ item_name: { $regex: "calculator", $options: "i" } })
```
*Explanation:* `$regex` performs pattern matching; `$options: "i"` ensures case-insensitivity.

---

### Task 8: Find all unresolved reports (status is 'open' or 'matched').
```javascript
db.items.find({ status: { $in: ["open", "matched"] } })
```
*Explanation:* Filters for active reports requiring action.

---

### Task 9: Update the status of item `ITEM-2026-003` to 'resolved'.
```javascript
db.items.updateOne(
  { item_id: "ITEM-2026-003" },
  { $set: { status: "resolved", updated_at: new Date() } }
)
```
*Explanation:* `updateOne` uses `$set` to change status and update the timestamp.

---

### Task 10: Increase the reward for item `ITEM-2026-001` by ₹100.
```javascript
db.items.updateOne(
  { item_id: "ITEM-2026-001" },
  { $inc: { reward: 100 }, $set: { updated_at: new Date() } }
)
```
*Explanation:* `$inc` atomically increments numeric field values.

---

### Task 11: Add a tag 'urgent' to item `ITEM-2026-001`.
```javascript
db.items.updateOne(
  { item_id: "ITEM-2026-001" },
  { $addToSet: { tags: "urgent" } }
)
```
*Explanation:* `$addToSet` appends to an array without introducing duplicates.

---

### Task 12: Delete an item by ID (`ITEM-2026-041`).
```javascript
db.items.deleteOne({ item_id: "ITEM-2026-041" })
```
*Explanation:* `deleteOne` removes the document matching the query.

---

### Task 13: Count total reports in each category (Aggregation).
```javascript
db.items.aggregate([
  { $group: { _id: "$category", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])
```
*Explanation:* Groups by `category`, counts via `$sum: 1`, and sorts descending.

---

### Task 14: Find the top 3 locations with the most reports.
```javascript
db.items.aggregate([
  { $group: { _id: "$location", totalReports: { $sum: 1 } } },
  { $sort: { totalReports: -1 } },
  { $limit: 3 }
])
```
*Explanation:* Groups by location, sorts descending, and limits output to 3.

---

### Task 15: Count the number of Lost vs Found items.
```javascript
db.items.aggregate([
  { $group: { _id: "$type", count: { $sum: 1 } } }
])
```
*Explanation:* Groups documents by the `type` field (`lost` or `found`).

---

### Task 16: Count reports by lifecycle status.
```javascript
db.items.aggregate([
  { $group: { _id: "$status", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])
```
*Explanation:* Evaluates status distribution across the dataset.

---

### Task 17: Calculate the average reward offered for lost Electronics.
```javascript
db.items.aggregate([
  { $match: { type: "lost", category: "Electronics" } },
  { $group: { _id: null, avgReward: { $avg: "$reward" } } }
])
```
*Explanation:* `$match` filters first, then `$group` computes `$avg`.

---

### Task 18: Find total items reported per user ID.
```javascript
db.items.aggregate([
  { $group: { _id: "$reported_by", totalReports: { $sum: 1 } } },
  { $sort: { totalReports: -1 } }
])
```
*Explanation:* Groups by the foreign key `reported_by`.

---

### Task 19: Join items with the users collection to see the reporter's full name.
```javascript
db.items.aggregate([
  { $match: { status: "open" } },
  {
    $lookup: {
      from: "users",
      localField: "reported_by",
      foreignField: "user_id",
      as: "user_details"
    }
  },
  { $unwind: "$user_details" },
  {
    $project: {
      item_name: 1,
      category: 1,
      reporter_name: "$user_details.name",
      reporter_email: "$user_details.email",
      _id: 0
    }
  }
])
```
*Explanation:* Demonstrates `$lookup` cross-collection join and `$unwind`.

---

### Task 20: Count how many items have tags containing "laptop".
```javascript
db.items.countDocuments({ tags: "laptop" })
```
*Explanation:* In MongoDB, querying an array field with a single value checks for element membership automatically.

---

## Section 2: Blank Practice Test (Queries Hidden for Live Practice)

Test yourself without looking at the answers above:

1. **Write a query to find all lost items.**
2. **Write a query to find all found items showing only `item_name` and `location`.**
3. **Write a query to find open items in the `Electronics` category.**
4. **Write a query to find items with `reward >= 200`.**
5. **Write a query to find items in either `Central Library` or `Sports Complex`.**
6. **Write a query to find a document with `item_id == "ITEM-2026-001"`.**
7. **Write a case-insensitive regex query to search for `"calculator"` in `item_name`.**
8. **Write a query to find items where status is either `'open'` or `'matched'`.**
9. **Write an update query to change the status of `ITEM-2026-003` to `'resolved'`.**
10. **Write an update query to increment the reward of `ITEM-2026-001` by 100.**
11. **Write an update query to add the tag `'urgent'` to `ITEM-2026-001` without duplicates.**
12. **Write a delete query to remove `ITEM-2026-041`.**
13. **Write an aggregation pipeline to group reports by `category` and count them.**
14. **Write an aggregation pipeline to find the top 3 reporting locations.**
15. **Write an aggregation pipeline to count total `lost` vs `found` items.**
16. **Write an aggregation pipeline to count items by `status`.**
17. **Write an aggregation pipeline to calculate the average reward for lost Electronics.**
18. **Write an aggregation pipeline to find total items reported by each `reported_by` user.**
19. **Write an aggregation pipeline using `$lookup` to join `items` with `users`.**
20. **Write a query to count all documents containing the tag `"laptop"`.**
