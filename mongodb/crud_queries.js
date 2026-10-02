/**
 * FindBack — Campus Lost & Found Intelligence System
 * Database: campus_findback
 * File: mongodb/crud_queries.js
 *
 * Description:
 * Native MongoDB Shell (mongosh) commands demonstrating full CRUD operations:
 * - Create: insertOne(), insertMany()
 * - Read: find(), findOne(), filtering with comparison & logical operators
 * - Update: updateOne(), updateMany()
 * - Delete: deleteOne(), deleteMany()
 */

// Switch to the project database
db = db.getSiblingDB('campus_findback');

print("=================================================");
print("  FINDBACK MONGODB CRUD DEMONSTRATION QUERIES   ");
print("=================================================\n");

// ==========================================
// 1. CREATE (INSERT) OPERATIONS
// ==========================================

print("--- 1.1 CREATE: Insert a Single Lost Item (insertOne) ---");
db.items.insertOne({
  item_id: "ITEM-2026-041",
  item_name: "MacBook Air M2 (Midnight Blue)",
  category: "Electronics",
  type: "lost",
  description: "13-inch midnight blue MacBook Air with python sticker on top lid.",
  location: "Central Library",
  date_reported: new Date("2026-03-15T10:00:00Z"),
  status: "open",
  reported_by: "USR-101",
  contact_email: "aarav.sharma@campus.edu",
  contact_phone: "+91-9876543210",
  reward: 1000,
  tags: ["apple", "macbook", "laptop", "midnight"],
  created_at: new Date(),
  updated_at: new Date()
});

print("--- 1.2 CREATE: Insert Multiple Items (insertMany) ---");
db.items.insertMany([
  {
    item_id: "ITEM-2026-042",
    item_name: "Sony Wireless Earbuds WF-1000XM5",
    category: "Electronics",
    type: "found",
    description: "Black charging case with right bud found under seat 12.",
    location: "Main Auditorium",
    date_reported: new Date("2026-03-15T11:30:00Z"),
    status: "open",
    reported_by: "USR-105",
    contact_email: "vikram.m@campus.edu",
    contact_phone: "+91-9876543214",
    reward: 0,
    tags: ["earbuds", "sony", "audio"],
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    item_id: "ITEM-2026-043",
    item_name: "Discrete Mathematics Notes (Binder)",
    category: "Books",
    type: "lost",
    description: "Yellow ring binder containing lecture handwritten notes.",
    location: "Science Block 1",
    date_reported: new Date("2026-03-15T14:00:00Z"),
    status: "open",
    reported_by: "USR-108",
    contact_email: "sneha.reddy@campus.edu",
    contact_phone: "+91-9876543217",
    reward: 50,
    tags: ["notes", "maths", "binder"],
    created_at: new Date(),
    updated_at: new Date()
  }
]);


// ==========================================
// 2. READ (FIND) OPERATIONS
// ==========================================

print("\n--- 2.1 READ: Find All Lost Items (Projection: item_id, item_name, location, status) ---");
db.items.find(
  { type: "lost" },
  { item_id: 1, item_name: 1, location: 1, status: 1, _id: 0 }
).limit(5);

print("\n--- 2.2 READ: Find By Category ('Electronics') and Status ('open') ---");
db.items.find(
  { category: "Electronics", status: "open" },
  { item_id: 1, item_name: 1, category: 1, location: 1, type: 1, _id: 0 }
);

print("\n--- 2.3 READ: Find Items Reported in Central Library with High Reward (>= 200) ---");
db.items.find(
  {
    location: "Central Library",
    reward: { $gte: 200 }
  },
  { item_id: 1, item_name: 1, location: 1, reward: 1, _id: 0 }
);

print("\n--- 2.4 READ: Find Specific Single Item by Unique item_id (findOne) ---");
db.items.findOne(
  { item_id: "ITEM-2026-001" },
  { item_id: 1, item_name: 1, description: 1, status: 1, contact_email: 1, _id: 0 }
);

print("\n--- 2.5 READ: Find Unresolved Items (Status is 'open' OR 'matched') ---");
db.items.find(
  { status: { $in: ["open", "matched"] } },
  { item_id: 1, item_name: 1, status: 1, location: 1, _id: 0 }
).limit(5);


// ==========================================
// 3. UPDATE OPERATIONS
// ==========================================

print("\n--- 3.1 UPDATE: Update Status of a Specific Item (updateOne) ---");
db.items.updateOne(
  { item_id: "ITEM-2026-001" },
  {
    $set: {
      status: "matched",
      updated_at: new Date()
    }
  }
);

print("\n--- 3.2 UPDATE: Update Location and Description with $set (updateOne) ---");
db.items.updateOne(
  { item_id: "ITEM-2026-002" },
  {
    $set: {
      location: "Campus Security Desk",
      description: "Handed over to Security Desk. Black Logitech M331 silent wireless mouse.",
      updated_at: new Date()
    }
  }
);

print("\n--- 3.3 UPDATE: Update Multiple Open Found Items with a Tag (updateMany) ---");
db.items.updateMany(
  { type: "found", status: "open" },
  {
    $addToSet: { tags: "unclaimed" },
    $set: { updated_at: new Date() }
  }
);


// ==========================================
// 4. DELETE OPERATIONS
// ==========================================

print("\n--- 4.1 DELETE: Delete a Specific Test or Incorrect Report (deleteOne) ---");
db.items.deleteOne({ item_id: "ITEM-2026-043" });

print("\n--- 4.2 DELETE: Delete Multiple Test Records by Condition (deleteMany) ---");
// Example: Safely removing demo test items
db.items.deleteMany({
  item_id: { $in: ["ITEM-2026-041", "ITEM-2026-042"] }
});

print("\n CRUD Operations Demonstration Script completed successfully.");
