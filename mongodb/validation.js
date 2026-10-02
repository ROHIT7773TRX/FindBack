/**
 * FindBack — Campus Lost & Found Intelligence System
 * Database: campus_findback
 * File: mongodb/validation.js
 *
 * Description:
 * Sets up collection-level schema validation using MongoDB $jsonSchema.
 * This ensures data integrity at the database layer (preventing invalid types,
 * missing required fields, or illegal enum values).
 */

// Switch to the target database
db = db.getSiblingDB('campus_findback');

// 1. Create or Update 'users' collection with $jsonSchema validation
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'name', 'email', 'role', 'department', 'created_at'],
      properties: {
        user_id: {
          bsonType: 'string',
          description: 'Unique user identifier (e.g., USR-101) - required string'
        },
        name: {
          bsonType: 'string',
          minLength: 2,
          description: 'Full name of the user - required string (min 2 chars)'
        },
        email: {
          bsonType: 'string',
          pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$',
          description: 'Valid email address - required string pattern'
        },
        role: {
          enum: ['student', 'faculty', 'staff', 'admin'],
          description: 'Role on campus - must be one of: student, faculty, staff, admin'
        },
        department: {
          bsonType: 'string',
          description: 'Academic or administrative department - required string'
        },
        phone: {
          bsonType: 'string',
          description: 'Contact phone number - optional string'
        },
        created_at: {
          bsonType: 'date',
          description: 'Timestamp when user was registered - required date'
        }
      }
    }
  },
  validationLevel: 'strict',
  validationAction: 'error'
});

// Create unique index on users.user_id and users.email
db.users.createIndex({ user_id: 1 }, { unique: true });
db.users.createIndex({ email: 1 }, { unique: true });

print(" Users collection validation schema & unique indexes configured successfully.");


// 2. Create or Update 'items' collection with $jsonSchema validation
db.createCollection('items', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: [
        'item_id',
        'item_name',
        'category',
        'type',
        'description',
        'location',
        'date_reported',
        'status',
        'reported_by',
        'created_at',
        'updated_at'
      ],
      properties: {
        item_id: {
          bsonType: 'string',
          description: 'Unique item reference ID (e.g. ITEM-2026-001) - required'
        },
        item_name: {
          bsonType: 'string',
          minLength: 2,
          maxLength: 100,
          description: 'Short descriptive title of the item - required string (2-100 chars)'
        },
        category: {
          enum: [
            'Electronics',
            'Books',
            'Stationery',
            'Clothing',
            'Accessories',
            'ID/Documents',
            'Other'
          ],
          description: 'Must match one of the recognized categories'
        },
        type: {
          enum: ['lost', 'found'],
          description: 'Report type - must be lost or found'
        },
        description: {
          bsonType: 'string',
          minLength: 5,
          description: 'Detailed description (color, brand, distinguishing marks) - required string'
        },
        location: {
          bsonType: 'string',
          description: 'Campus location where item was lost or found - required string'
        },
        date_reported: {
          bsonType: ['date', 'string'],
          description: 'Date when lost/found was observed or filed - required'
        },
        status: {
          enum: ['open', 'matched', 'resolved', 'closed'],
          description: 'Lifecycle status - must be open, matched, resolved, or closed'
        },
        reported_by: {
          bsonType: 'string',
          description: 'Reference to user_id or reporter name - required string'
        },
        contact_email: {
          bsonType: 'string',
          description: 'Contact email for updates - optional string'
        },
        contact_phone: {
          bsonType: 'string',
          description: 'Contact phone number - optional string'
        },
        reward: {
          bsonType: ['int', 'double', 'long', 'decimal'],
          minimum: 0,
          description: 'Optional monetary or token reward offered (>= 0)'
        },
        tags: {
          bsonType: 'array',
          items: {
            bsonType: 'string'
          },
          description: 'Optional array of search keyword tags'
        },
        created_at: {
          bsonType: 'date',
          description: 'Document creation timestamp'
        },
        updated_at: {
          bsonType: 'date',
          description: 'Document last modified timestamp'
        }
      }
    }
  },
  validationLevel: 'strict',
  validationAction: 'error'
});

// Create performance indexes for common query fields
db.items.createIndex({ item_id: 1 }, { unique: true });
db.items.createIndex({ category: 1 });
db.items.createIndex({ type: 1 });
db.items.createIndex({ status: 1 });
db.items.createIndex({ location: 1 });
db.items.createIndex({ item_name: 'text', description: 'text', location: 'text' });

print(" Items collection validation schema & indexes configured successfully.");
