/**
 * FindBack — Campus Lost & Found Intelligence System
 * Database: campus_findback
 * File: mongodb/aggregation_queries.js
 *
 * Description:
 * Meaningful multi-stage MongoDB Aggregation Pipelines.
 * Demonstrates: $match, $group, $sort, $project, $limit, $sum, $avg, $lookup
 */

// Switch to the project database
db = db.getSiblingDB('campus_findback');

print("=================================================");
print("   FINDBACK MONGODB AGGREGATION PIPELINES        ");
print("=================================================\n");

// ============================================================================
// AGGREGATION 1: Total Reports Grouped by Category
// Problem: Which item categories are reported most frequently on campus?
// Stages:
//   1. $group: Group by $category, count occurrences using $sum: 1
//   2. $project: Format the output fields clearly
//   3. $sort: Sort in descending order of total_reports
// ============================================================================
print("--- Aggregation 1: Total Reports by Category ---");
const aggCategory = db.items.aggregate([
  {
    $group: {
      _id: "$category",
      total_reports: { $sum: 1 },
      lost_count: {
        $sum: { $cond: [{ $eq: ["$type", "lost"] }, 1, 0] }
      },
      found_count: {
        $sum: { $cond: [{ $eq: ["$type", "found"] }, 1, 0] }
      }
    }
  },
  {
    $project: {
      _id: 0,
      category: "$_id",
      total_reports: 1,
      lost_count: 1,
      found_count: 1
    }
  },
  {
    $sort: { total_reports: -1 }
  }
]).toArray();
printjson(aggCategory);


// ============================================================================
// AGGREGATION 2: Hotspot Analysis - Reports Grouped by Campus Location
// Problem: Which campus locations have the highest loss/found activity?
// Stages:
//   1. $group: Group by $location and count reports
//   2. $project: Format result fields
//   3. $sort: Sort by count descending
//   4. $limit: Return top 5 campus hotspots
// ============================================================================
print("\n--- Aggregation 2: Top Campus Location Hotspots ---");
const aggLocation = db.items.aggregate([
  {
    $group: {
      _id: "$location",
      report_count: { $sum: 1 },
      unresolved_count: {
        $sum: { $cond: [{ $in: ["$status", ["open", "matched"]] }, 1, 0] }
      }
    }
  },
  {
    $project: {
      _id: 0,
      location: "$_id",
      report_count: 1,
      unresolved_count: 1
    }
  },
  {
    $sort: { report_count: -1 }
  },
  {
    $limit: 5
  }
]).toArray();
printjson(aggLocation);


// ============================================================================
// AGGREGATION 3: Lost vs Found Overview & Resolution Rate
// Problem: What is the distribution and breakdown between Lost and Found items?
// Stages:
//   1. $group: Group by $type (lost vs found), count total & resolved items
//   2. $project: Calculate resolution rate percentage
//   3. $sort: Order by total_items descending
// ============================================================================
print("\n--- Aggregation 3: Lost vs Found Breakdown ---");
const aggType = db.items.aggregate([
  {
    $group: {
      _id: "$type",
      total_items: { $sum: 1 },
      resolved_items: {
        $sum: { $cond: [{ $eq: ["$status", "resolved"] }, 1, 0] }
      },
      open_items: {
        $sum: { $cond: [{ $eq: ["$status", "open"] }, 1, 0] }
      }
    }
  },
  {
    $project: {
      _id: 0,
      report_type: "$_id",
      total_items: 1,
      resolved_items: 1,
      open_items: 1,
      resolution_rate_percent: {
        $round: [
          { $multiply: [{ $divide: ["$resolved_items", "$total_items"] }, 100] },
          1
        ]
      }
    }
  },
  {
    $sort: { total_items: -1 }
  }
]).toArray();
printjson(aggType);


// ============================================================================
// AGGREGATION 4: Lifecycle Status Distribution
// Problem: How many items are in each lifecycle status (open, matched, resolved, closed)?
// Stages:
//   1. $group: Group by $status and count occurrences
//   2. $project: Alias _id to status
//   3. $sort: Order by count descending
// ============================================================================
print("\n--- Aggregation 4: Status Distribution ---");
const aggStatus = db.items.aggregate([
  {
    $group: {
      _id: "$status",
      count: { $sum: 1 }
    }
  },
  {
    $project: {
      _id: 0,
      status: "$_id",
      count: 1
    }
  },
  {
    $sort: { count: -1 }
  }
]).toArray();
printjson(aggStatus);


// ============================================================================
// AGGREGATION 5: High-Value Unclaimed Electronics by Location
// Problem: Where are high-value or open Electronics currently located?
// Stages:
//   1. $match: Filter for category "Electronics" and status "open"
//   2. $group: Group by location, calculate total open items and avg reward
//   3. $project: Format fields and round avg_reward
//   4. $sort: Highest count first
// ============================================================================
print("\n--- Aggregation 5: Open High-Value Electronics Hotspots ---");
const aggElectronics = db.items.aggregate([
  {
    $match: {
      category: "Electronics",
      status: "open"
    }
  },
  {
    $group: {
      _id: "$location",
      open_electronics_count: { $sum: 1 },
      average_reward: { $avg: "$reward" }
    }
  },
  {
    $project: {
      _id: 0,
      location: "$_id",
      open_electronics_count: 1,
      average_reward: { $round: ["$average_reward", 2] }
    }
  },
  {
    $sort: { open_electronics_count: -1 }
  }
]).toArray();
printjson(aggElectronics);


// ============================================================================
// AGGREGATION 6: Reporter Lookup (Cross-Collection $lookup)
// Problem: Join item records with user details to see reporter name, email, department
// Stages:
//   1. $match: Filter open lost items
//   2. $lookup: Join with `users` collection on reported_by == user_id
//   3. $unwind: Deconstruct the joined array
//   4. $project: Select key fields for clean display
//   5. $limit: Display top 5
// ============================================================================
print("\n--- Aggregation 6: Item & User Join ($lookup) ---");
const aggLookup = db.items.aggregate([
  {
    $match: { type: "lost", status: "open" }
  },
  {
    $lookup: {
      from: "users",
      localField: "reported_by",
      foreignField: "user_id",
      as: "reporter_info"
    }
  },
  {
    $unwind: {
      path: "$reporter_info",
      preserveNullAndEmptyArrays: true
    }
  },
  {
    $project: {
      _id: 0,
      item_id: 1,
      item_name: 1,
      category: 1,
      location: 1,
      reward: 1,
      reporter_name: "$reporter_info.name",
      department: "$reporter_info.department",
      reporter_role: "$reporter_info.role"
    }
  },
  {
    $limit: 5
  }
]).toArray();
printjson(aggLookup);
