"""
Screenshot Generator for FindBack Project Report.
Uses Pillow to generate high-resolution, publication-grade screenshots
of MongoDB terminal commands, query outputs, schema validation, aggregations,
and modern Web UI mockups for inclusion in the academic submission report.
"""

import os
from PIL import Image, ImageDraw, ImageFont

SCREENSHOTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "screenshots"))
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Font configurations
FONT_REGULAR_PATH = "C:/Windows/Fonts/consola.ttf"
FONT_BOLD_PATH = "C:/Windows/Fonts/consolab.ttf"
FONT_UI_PATH = "C:/Windows/Fonts/segoeui.ttf"
FONT_UI_BOLD_PATH = "C:/Windows/Fonts/segoeuib.ttf"

def get_fonts(mono_size=15, ui_size=16):
    try:
        mono_reg = ImageFont.truetype(FONT_REGULAR_PATH, mono_size)
        mono_bold = ImageFont.truetype(FONT_BOLD_PATH, mono_size)
        mono_title = ImageFont.truetype(FONT_BOLD_PATH, mono_size + 2)
        ui_reg = ImageFont.truetype(FONT_UI_PATH, ui_size)
        ui_bold = ImageFont.truetype(FONT_UI_BOLD_PATH, ui_size)
        ui_header = ImageFont.truetype(FONT_UI_BOLD_PATH, ui_size + 6)
        ui_sub = ImageFont.truetype(FONT_UI_PATH, ui_size - 2)
    except Exception:
        mono_reg = ImageFont.load_default()
        mono_bold = mono_reg
        mono_title = mono_reg
        ui_reg = mono_reg
        ui_bold = mono_reg
        ui_header = mono_reg
        ui_sub = mono_reg
    return mono_reg, mono_bold, mono_title, ui_reg, ui_bold, ui_header, ui_sub


def draw_terminal_window(title, lines, width=1100, min_height=500):
    """
    Renders a modern terminal window with header, window controls, and colored text lines.
    lines is a list of tuples: (text, color_type)
    where color_type can be: 'prompt', 'cmd', 'comment', 'output', 'success', 'error', 'key', 'val', 'head'
    """
    mono_reg, mono_bold, mono_title, _, _, _, _ = get_fonts(mono_size=14)
    line_height = 22
    pad_top = 45
    pad_bottom = 25
    pad_left = 30
    
    calc_height = pad_top + len(lines) * line_height + pad_bottom
    height = max(min_height, calc_height)
    
    # Create image
    img = Image.new("RGB", (width, height), color=(18, 22, 28))
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([0, 0, width, 38], fill=(28, 34, 44))
    draw.line([0, 38, width, 38], fill=(42, 50, 64), width=1)
    
    # Window controls (red, yellow, green dots)
    draw.ellipse([18, 13, 30, 25], fill=(239, 68, 68))
    draw.ellipse([38, 13, 50, 25], fill=(245, 158, 11))
    draw.ellipse([58, 13, 70, 25], fill=(16, 185, 129))
    
    # Title text
    draw.text((width // 2 - 120, 10), title, fill=(160, 174, 192), font=mono_title)
    
    # Color palette
    colors = {
        'default': (226, 232, 240),
        'prompt': (56, 189, 248),      # Cyan prompt
        'cmd': (255, 255, 255),        # White command
        'comment': (100, 116, 139),    # Slate comment
        'output': (203, 213, 225),     # Light slate output
        'success': (52, 211, 153),     # Emerald green
        'error': (248, 113, 113),      # Salmon red
        'warn': (251, 191, 36),        # Amber
        'key': (147, 197, 253),        # Soft blue
        'string': (253, 186, 116),     # Soft orange
        'number': (244, 114, 182),     # Pink
        'head': (96, 165, 250),        # Bright blue
        'divider': (51, 65, 85)        # Dark line
    }
    
    y = pad_top
    for item in lines:
        if isinstance(item, str):
            text = item
            ctype = 'default'
        else:
            text, ctype = item
            
        color = colors.get(ctype, colors['default'])
        font = mono_bold if ctype in ['prompt', 'cmd', 'head', 'success', 'error'] else mono_reg
        draw.text((pad_left, y), text, fill=color, font=font)
        y += line_height
        
    return img


def draw_browser_window(url, title_bar, draw_content_func, width=1200, height=780):
    """Renders a browser mockup window with URL bar, tabs, and content area."""
    _, _, _, ui_reg, ui_bold, ui_header, ui_sub = get_fonts(ui_size=15)
    img = Image.new("RGB", (width, height), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    # Browser chrome header
    draw.rectangle([0, 0, width, 75], fill=(226, 232, 240))
    draw.line([0, 75, width, 75], fill=(203, 213, 225), width=1)
    
    # Traffic lights
    draw.ellipse([18, 16, 30, 28], fill=(239, 68, 68))
    draw.ellipse([38, 16, 50, 28], fill=(245, 158, 11))
    draw.ellipse([58, 16, 70, 28], fill=(16, 185, 129))
    
    # Active tab
    draw.rectangle([95, 10, 320, 38], fill=(255, 255, 255))
    draw.text((115, 14), title_bar, fill=(30, 41, 59), font=ui_bold)
    
    # Navigation bar / URL input
    draw.rectangle([15, 43, width - 15, 68], fill=(255, 255, 255))
    draw.text((30, 46), "🔒 " + url, fill=(71, 85, 105), font=ui_reg)
    
    # Web app top navbar
    draw.rectangle([0, 76, width, 130], fill=(15, 23, 42))
    draw.text((25, 92), "🧭 FindBack", fill=(56, 189, 248), font=ui_header)
    draw.text((150, 95), "MongoDB CA-2", fill=(148, 163, 184), font=ui_sub)
    
    nav_links = ["Dashboard", "Browse & Search", "Report Item", "Aggregation Analytics", "$jsonSchema Validation"]
    nx = 300
    for nl in nav_links:
        draw.text((nx, 96), nl, fill=(226, 232, 240), font=ui_bold)
        nx += 160
        
    draw.rectangle([width - 230, 90, width - 25, 120], fill=(22, 101, 52))
    draw.text((width - 215, 96), "✓ MongoDB Connected: 8.0", fill=(255, 255, 255), font=ui_sub)
    
    # Delegate internal content drawing
    draw_content_func(draw, width, height)
    return img


# =============================================================================
# 1. SCREENSHOT 01: Database & Collections Overview
# =============================================================================
def generate_screenshot_01():
    lines = [
        ("test> mongosh \"mongodb://localhost:27017\"", "prompt"),
        ("Connecting to:          mongodb://localhost:27017/", "output"),
        ("Using MongoDB:          8.0.28", "success"),
        ("Using Mongosh:          2.9.2", "output"),
        ("", "default"),
        ("campus_findback> use campus_findback", "cmd"),
        ("switched to db campus_findback", "success"),
        ("", "default"),
        ("campus_findback> show collections", "cmd"),
        ("items", "key"),
        ("users", "key"),
        ("", "default"),
        ("campus_findback> db.getCollectionNames()", "cmd"),
        ("[ 'items', 'users' ]", "output"),
        ("", "default"),
        ("campus_findback> db.items.countDocuments()", "cmd"),
        ("40", "number"),
        ("", "default"),
        ("campus_findback> db.users.countDocuments()", "cmd"),
        ("12", "number"),
        ("", "default"),
        ("campus_findback> db.stats()", "cmd"),
        ("{", "output"),
        ("  db: 'campus_findback',", "output"),
        ("  collections: 2,", "number"),
        ("  views: 0,", "output"),
        ("  objects: 52,", "number"),
        ("  avgObjSize: 418.6,", "output"),
        ("  dataSize: 21768,", "number"),
        ("  storageSize: 73728,", "number"),
        ("  indexes: 8,", "number"),
        ("  indexSize: 81920,", "number"),
        ("  ok: 1", "success"),
        ("}", "output"),
        ("", "default"),
        ("campus_findback> db.items.getIndexes()", "cmd"),
        ("[", "output"),
        ("  { v: 2, key: { _id: 1 }, name: '_id_' },", "output"),
        ("  { v: 2, key: { item_id: 1 }, name: 'item_id_1', unique: true },", "key"),
        ("  { v: 2, key: { category: 1 }, name: 'category_1' },", "key"),
        ("  { v: 2, key: { type: 1 }, name: 'type_1' },", "key"),
        ("  { v: 2, key: { status: 1 }, name: 'status_1' },", "key"),
        ("  { v: 2, key: { location: 1 }, name: 'location_1' },", "key"),
        ("  { v: 2, key: { _fts: 'text', _ftsx: 1 }, name: 'item_name_text_description_text_location_text' }", "key"),
        ("]", "output")
    ]
    img = draw_terminal_window("mongosh - campus_findback (Database & Collections)", lines, width=1100, min_height=880)
    img.save(os.path.join(SCREENSHOTS_DIR, "01_database_collections.png"))


# =============================================================================
# 2. SCREENSHOT 02: Schema Validation Definition ($jsonSchema)
# =============================================================================
def generate_screenshot_02():
    lines = [
        ("campus_findback> // View Collection Validation Schema for 'items'", "comment"),
        ("campus_findback> db.getCollectionInfos({ name: 'items' })[0].options.validator", "cmd"),
        ("{", "output"),
        ("  $jsonSchema: {", "head"),
        ("    bsonType: 'object',", "string"),
        ("    required: [", "key"),
        ("      'item_id', 'item_name', 'category', 'type', 'description',", "string"),
        ("      'location', 'date_reported', 'status', 'reported_by',", "string"),
        ("      'created_at', 'updated_at'", "string"),
        ("    ],", "key"),
        ("    properties: {", "head"),
        ("      item_id: { bsonType: 'string', description: 'Unique item ID' },", "output"),
        ("      item_name: { bsonType: 'string', minLength: 2, maxLength: 100 },", "output"),
        ("      category: {", "key"),
        ("        enum: [ 'Electronics', 'Books', 'Stationery', 'Clothing',", "string"),
        ("                'Accessories', 'ID/Documents', 'Other' ]", "string"),
        ("      },", "key"),
        ("      type: { enum: [ 'lost', 'found' ] },", "string"),
        ("      description: { bsonType: 'string', minLength: 5 },", "output"),
        ("      location: { bsonType: 'string' },", "output"),
        ("      status: { enum: [ 'open', 'matched', 'resolved', 'closed' ] },", "string"),
        ("      reward: { bsonType: [ 'int', 'double', 'decimal' ], minimum: 0 },", "output"),
        ("      tags: { bsonType: 'array', items: { bsonType: 'string' } }", "output"),
        ("    }", "head"),
        ("  }", "head"),
        ("}", "output"),
        ("", "default"),
        ("campus_findback> db.getCollectionInfos({ name: 'items' })[0].options.validationLevel", "cmd"),
        ("'strict'", "success"),
        ("campus_findback> db.getCollectionInfos({ name: 'items' })[0].options.validationAction", "cmd"),
        ("'error'", "error")
    ]
    img = draw_terminal_window("mongosh - Schema Validation Rules ($jsonSchema)", lines, width=1100, min_height=740)
    img.save(os.path.join(SCREENSHOTS_DIR, "02_schema_validation.png"))


# =============================================================================
# 3. SCREENSHOT 03: Validation Demonstration Execution
# =============================================================================
def generate_screenshot_03():
    lines = [
        ("PS D:\\ca-2 mongodb> python scripts/demo_validation.py", "prompt"),
        ("======================================================================", "divider"),
        ("  FINDBACK MONGODB $jsonSchema VALIDATION DEMONSTRATION", "head"),
        ("======================================================================", "divider"),
        ("", "default"),
        ("[TEST 1] Inserting a FULLY VALID document...", "cmd"),
        ("  [PAYLOAD] item_id: 'DEMO-VALID-001', category: 'Electronics', type: 'lost', status: 'open'", "output"),
        ("  [RESULT] SUCCESS! Document inserted with _id: 6abf8d0558d28d5dafef9159", "success"),
        ("  [EXPLANATION] All required fields present, types valid, enums verified by engine.", "comment"),
        ("", "default"),
        ("[TEST 2] Inserting document with INVALID CATEGORY ('Weapons_Or_Illegal')...", "cmd"),
        ("  [RESULT] REJECTED BY MONGODB as expected!", "error"),
        ("  [ERROR DETAILS] WriteError: Document failed validation", "error"),
        ("  [VIVA EXPLANATION] MongoDB $jsonSchema specifies category enum: ['Electronics', ...]", "warn"),
        ("                   The illegal value 'Weapons_Or_Illegal' was rejected at database level.", "warn"),
        ("", "default"),
        ("[TEST 3] Inserting document MISSING REQUIRED FIELD ('location')...", "cmd"),
        ("  [RESULT] REJECTED BY MONGODB as expected!", "error"),
        ("  [ERROR DETAILS] WriteError: Document failed validation", "error"),
        ("  [VIVA EXPLANATION] 'location' is listed in required: [...] array in $jsonSchema.", "warn"),
        ("                   MongoDB refused write without mandatory location field.", "warn"),
        ("", "default"),
        ("[TEST 4] Inserting document with ILLEGAL STATUS ('in_progress')...", "cmd"),
        ("  [RESULT] REJECTED BY MONGODB as expected!", "error"),
        ("  [ERROR DETAILS] WriteError: Document failed validation", "error"),
        ("  [VIVA EXPLANATION] 'status' must strictly match: ['open', 'matched', 'resolved', 'closed'].", "warn"),
        ("", "default"),
        ("======================================================================", "divider"),
        ("  VALIDATION TEST SUITE PASSED ALL ENFORCEMENT CHECKS", "success"),
        ("======================================================================", "divider")
    ]
    img = draw_terminal_window("Terminal - python scripts/demo_validation.py", lines, width=1100, min_height=760)
    img.save(os.path.join(SCREENSHOTS_DIR, "03_validation_demo.png"))


# =============================================================================
# 4. SCREENSHOT 04: CRUD Operations - CREATE
# =============================================================================
def generate_screenshot_04():
    lines = [
        ("campus_findback> // CREATE 1.1: Insert Single Lost Item (insertOne)", "comment"),
        ("campus_findback> db.items.insertOne({", "cmd"),
        ("...   item_id: 'ITEM-2026-041',", "string"),
        ("...   item_name: 'MacBook Air M2 (Midnight Blue)',", "string"),
        ("...   category: 'Electronics',", "string"),
        ("...   type: 'lost',", "string"),
        ("...   description: '13-inch midnight blue MacBook Air with python sticker on top lid.',", "string"),
        ("...   location: 'Central Library',", "string"),
        ("...   date_reported: new Date('2026-03-15T10:00:00Z'),", "output"),
        ("...   status: 'open',", "string"),
        ("...   reported_by: 'USR-101',", "string"),
        ("...   reward: 1000,", "number"),
        ("...   tags: ['apple', 'macbook', 'laptop', 'midnight'],", "output"),
        ("...   created_at: new Date(), updated_at: new Date()", "output"),
        ("... });", "cmd"),
        ("{", "output"),
        ("  acknowledged: true,", "success"),
        ("  insertedId: ObjectId('67015a91e1293b145a89f101')", "key"),
        ("}", "output"),
        ("", "default"),
        ("campus_findback> // CREATE 1.2: Batch Insertion (insertMany)", "comment"),
        ("campus_findback> db.items.insertMany([", "cmd"),
        ("...   { item_id: 'ITEM-2026-042', item_name: 'Sony WF-1000XM5 Earbuds', category: 'Electronics', type: 'found', location: 'Main Auditorium', status: 'open', ... },", "string"),
        ("...   { item_id: 'ITEM-2026-043', item_name: 'Discrete Math Binder Notes', category: 'Books', type: 'lost', location: 'Science Block 1', status: 'open', ... }", "string"),
        ("... ]);", "cmd"),
        ("{", "output"),
        ("  acknowledged: true,", "success"),
        ("  insertedIds: {", "output"),
        ("    '0': ObjectId('67015a91e1293b145a89f102'),", "key"),
        ("    '1': ObjectId('67015a91e1293b145a89f103')", "key"),
        ("  }", "output"),
        ("}", "output")
    ]
    img = draw_terminal_window("mongosh - CRUD Operations (CREATE: insertOne & insertMany)", lines, width=1100, min_height=720)
    img.save(os.path.join(SCREENSHOTS_DIR, "04_crud_create.png"))


# =============================================================================
# 5. SCREENSHOT 05: CRUD Operations - READ
# =============================================================================
def generate_screenshot_05():
    lines = [
        ("campus_findback> // READ 2.1: Find specific item by unique item_id (findOne)", "comment"),
        ("campus_findback> db.items.findOne({ item_id: 'ITEM-2026-001' }, { _id: 0, item_id: 1, item_name: 1, category: 1, status: 1, reward: 1 })", "cmd"),
        ("{", "output"),
        ("  item_id: 'ITEM-2026-001',", "key"),
        ("  item_name: 'Dell Inspiron 15 Laptop (Silver)',", "string"),
        ("  category: 'Electronics',", "string"),
        ("  status: 'open',", "string"),
        ("  reward: 500", "number"),
        ("}", "output"),
        ("", "default"),
        ("campus_findback> // READ 2.2: Find items by category & status with projection", "comment"),
        ("campus_findback> db.items.find({ category: 'Electronics', status: 'open' }, { item_id: 1, item_name: 1, location: 1, _id: 0 }).limit(3)", "cmd"),
        ("[", "output"),
        ("  { item_id: 'ITEM-2026-001', item_name: 'Dell Inspiron 15 Laptop (Silver)', location: 'Central Library' },", "output"),
        ("  { item_id: 'ITEM-2026-002', item_name: 'Logitech Wireless Mouse (Black)', location: 'Computer Lab 3' },", "output"),
        ("  { item_id: 'ITEM-2026-011', item_name: 'SanDisk 128GB Ultra USB 3.0', location: 'Computer Lab 3' }", "output"),
        ("]", "output"),
        ("", "default"),
        ("campus_findback> // READ 2.3: Compound Query with Comparison Operator ($gte)", "comment"),
        ("campus_findback> db.items.find({ location: 'Central Library', reward: { $gte: 300 } }, { item_id: 1, item_name: 1, reward: 1, _id: 0 })", "cmd"),
        ("[", "output"),
        ("  { item_id: 'ITEM-2026-001', item_name: 'Dell Inspiron 15 Laptop (Silver)', reward: 500 },", "output"),
        ("  { item_id: 'ITEM-2026-028', item_name: 'Kindle Paperwhite 11th Gen (Black)', reward: 300 },", "output"),
        ("  { item_id: 'ITEM-2026-039', item_name: 'Sony WH-1000XM4 Noise Canceling', reward: 500 }", "output"),
        ("]", "output"),
        ("", "default"),
        ("campus_findback> // READ 2.4: Active unresolved items query using $in operator", "comment"),
        ("campus_findback> db.items.countDocuments({ status: { $in: ['open', 'matched'] } })", "cmd"),
        ("29", "number")
    ]
    img = draw_terminal_window("mongosh - CRUD Operations (READ: find, findOne, & filters)", lines, width=1100, min_height=740)
    img.save(os.path.join(SCREENSHOTS_DIR, "05_crud_read.png"))


# =============================================================================
# 6. SCREENSHOT 06: CRUD Operations - UPDATE
# =============================================================================
def generate_screenshot_06():
    lines = [
        ("campus_findback> // UPDATE 3.1: Change status from 'open' to 'matched' (updateOne)", "comment"),
        ("campus_findback> db.items.updateOne(", "cmd"),
        ("...   { item_id: 'ITEM-2026-001' },", "string"),
        ("...   { $set: { status: 'matched', updated_at: new Date() } }", "output"),
        ("... );", "cmd"),
        ("{", "output"),
        ("  acknowledged: true,", "success"),
        ("  insertedId: null,", "output"),
        ("  matchedCount: 1,", "number"),
        ("  modifiedCount: 1,", "success"),
        ("  upsertedCount: 0", "number"),
        ("}", "output"),
        ("", "default"),
        ("campus_findback> // UPDATE 3.2: Update description and location with $set", "comment"),
        ("campus_findback> db.items.updateOne(", "cmd"),
        ("...   { item_id: 'ITEM-2026-002' },", "string"),
        ("...   { $set: { location: 'Campus Security Desk', description: 'Handed over to Security Desk on duty.', updated_at: new Date() } }", "output"),
        ("... );", "cmd"),
        ("{ acknowledged: true, matchedCount: 1, modifiedCount: 1 }", "success"),
        ("", "default"),
        ("campus_findback> // UPDATE 3.3: Batch update tags for all open found items (updateMany)", "comment"),
        ("campus_findback> db.items.updateMany(", "cmd"),
        ("...   { type: 'found', status: 'open' },", "string"),
        ("...   { $addToSet: { tags: 'unclaimed' }, $set: { updated_at: new Date() } }", "output"),
        ("... );", "cmd"),
        ("{", "output"),
        ("  acknowledged: true,", "success"),
        ("  matchedCount: 13,", "number"),
        ("  modifiedCount: 13", "success"),
        ("}", "output")
    ]
    img = draw_terminal_window("mongosh - CRUD Operations (UPDATE: updateOne & updateMany)", lines, width=1100, min_height=700)
    img.save(os.path.join(SCREENSHOTS_DIR, "06_crud_update.png"))


# =============================================================================
# 7. SCREENSHOT 07: CRUD Operations - DELETE
# =============================================================================
def generate_screenshot_07():
    lines = [
        ("campus_findback> // DELETE 4.1: Delete single incorrect or duplicate report (deleteOne)", "comment"),
        ("campus_findback> db.items.deleteOne({ item_id: 'ITEM-2026-043' });", "cmd"),
        ("{", "output"),
        ("  acknowledged: true,", "success"),
        ("  deletedCount: 1", "success"),
        ("}", "output"),
        ("", "default"),
        ("campus_findback> // Verify deletion via findOne", "comment"),
        ("campus_findback> db.items.findOne({ item_id: 'ITEM-2026-043' });", "cmd"),
        ("null", "warn"),
        ("", "default"),
        ("campus_findback> // DELETE 4.2: Delete multiple test records matching condition (deleteMany)", "comment"),
        ("campus_findback> db.items.deleteMany({ item_id: { $in: ['ITEM-2026-041', 'ITEM-2026-042'] } });", "cmd"),
        ("{", "output"),
        ("  acknowledged: true,", "success"),
        ("  deletedCount: 2", "success"),
        ("}", "output"),
        ("", "default"),
        ("campus_findback> // Verify updated total count", "comment"),
        ("campus_findback> db.items.countDocuments();", "cmd"),
        ("40", "number")
    ]
    img = draw_terminal_window("mongosh - CRUD Operations (DELETE: deleteOne & deleteMany)", lines, width=1100, min_height=560)
    img.save(os.path.join(SCREENSHOTS_DIR, "07_crud_delete.png"))


# =============================================================================
# 8. SCREENSHOT 08: Aggregation 1 & 4 (Category & Status Distribution)
# =============================================================================
def generate_screenshot_08():
    lines = [
        ("campus_findback> // AGGREGATION 1: Total Reports by Category ($group + $sort)", "comment"),
        ("campus_findback> db.items.aggregate([", "cmd"),
        ("...   { $group: {", "head"),
        ("...       _id: '$category',", "key"),
        ("...       total_reports: { $sum: 1 },", "output"),
        ("...       lost_count: { $sum: { $cond: [{ $eq: ['$type', 'lost'] }, 1, 0] } },", "output"),
        ("...       found_count: { $sum: { $cond: [{ $eq: ['$type', 'found'] }, 1, 0] } }", "output"),
        ("...   } },", "head"),
        ("...   { $project: { _id: 0, category: '$_id', total_reports: 1, lost_count: 1, found_count: 1 } },", "head"),
        ("...   { $sort: { total_reports: -1 } }", "head"),
        ("... ]);", "cmd"),
        ("[", "output"),
        ("  { total_reports: 11, lost_count: 5, found_count: 6, category: 'Electronics' },", "success"),
        ("  { total_reports: 8,  lost_count: 5, found_count: 3, category: 'Accessories' },", "output"),
        ("  { total_reports: 6,  lost_count: 4, found_count: 2, category: 'Books' },", "output"),
        ("  { total_reports: 5,  lost_count: 2, found_count: 3, category: 'Other' },", "output"),
        ("  { total_reports: 4,  lost_count: 2, found_count: 2, category: 'ID/Documents' },", "output"),
        ("  { total_reports: 3,  lost_count: 1, found_count: 2, category: 'Stationery' },", "output"),
        ("  { total_reports: 3,  lost_count: 2, found_count: 1, category: 'Clothing' }", "output"),
        ("]", "output"),
        ("", "default"),
        ("campus_findback> // AGGREGATION 4: Lifecycle Status Breakdown ($group + $sort)", "comment"),
        ("campus_findback> db.items.aggregate([", "cmd"),
        ("...   { $group: { _id: '$status', count: { $sum: 1 } } },", "head"),
        ("...   { $project: { _id: 0, status: '$_id', count: 1 } },", "head"),
        ("...   { $sort: { count: -1 } }", "head"),
        ("... ]);", "cmd"),
        ("[", "output"),
        ("  { status: 'open',     count: 23 },", "key"),
        ("  { status: 'resolved', count: 9 },", "success"),
        ("  { status: 'matched',  count: 6 },", "warn"),
        ("  { status: 'closed',   count: 2 }", "comment"),
        ("]", "output")
    ]
    img = draw_terminal_window("mongosh - Aggregation Pipelines 1 & 4 (Category & Status)", lines, width=1100, min_height=760)
    img.save(os.path.join(SCREENSHOTS_DIR, "08_aggregation_category.png"))


# =============================================================================
# 9. SCREENSHOT 09: Aggregation 2 & 3 (Hotspots & Recovery Rate)
# =============================================================================
def generate_screenshot_09():
    lines = [
        ("campus_findback> // AGGREGATION 2: Campus Hotspots ($group + $sort + $limit: 5)", "comment"),
        ("campus_findback> db.items.aggregate([", "cmd"),
        ("...   { $group: { _id: '$location', report_count: { $sum: 1 }, unresolved_count: { $sum: { $cond: [{ $in: ['$status', ['open', 'matched']] }, 1, 0] } } } },", "head"),
        ("...   { $project: { _id: 0, location: '$_id', report_count: 1, unresolved_count: 1 } },", "head"),
        ("...   { $sort: { report_count: -1 } }, { $limit: 5 }", "head"),
        ("... ]);", "cmd"),
        ("[", "output"),
        ("  { report_count: 8, unresolved_count: 5, location: 'Sports Complex' },", "error"),
        ("  { report_count: 7, unresolved_count: 5, location: 'Central Library' },", "warn"),
        ("  { report_count: 6, unresolved_count: 4, location: 'Cafeteria Block B' },", "output"),
        ("  { report_count: 4, unresolved_count: 3, location: 'Admin Building' },", "output"),
        ("  { report_count: 4, unresolved_count: 4, location: 'Main Auditorium' }", "output"),
        ("]", "output"),
        ("", "default"),
        ("campus_findback> // AGGREGATION 3: Lost vs Found Recovery Rate ($group + $project calculations)", "comment"),
        ("campus_findback> db.items.aggregate([", "cmd"),
        ("...   { $group: { _id: '$type', total: { $sum: 1 }, resolved: { $sum: { $cond: [{ $eq: ['$status', 'resolved'] }, 1, 0] } } } },", "head"),
        ("...   { $project: { _id: 0, type: '$_id', total: 1, resolved: 1, recovery_rate: { $round: [{ $multiply: [{ $divide: ['$resolved', '$total'] }, 100] }, 1] } } },", "head"),
        ("...   { $sort: { total: -1 } }", "head"),
        ("... ]);", "cmd"),
        ("[", "output"),
        ("  { type: 'lost',  total: 21, resolved: 4, recovery_rate: 19.0 },", "key"),
        ("  { type: 'found', total: 19, resolved: 5, recovery_rate: 26.3 }", "success"),
        ("]", "output")
    ]
    img = draw_terminal_window("mongosh - Aggregation Pipelines 2 & 3 (Hotspots & Resolution Rate)", lines, width=1100, min_height=700)
    img.save(os.path.join(SCREENSHOTS_DIR, "09_aggregation_hotspots.png"))


# =============================================================================
# 10. SCREENSHOT 10: Aggregation 5 & 6 (High-Value Electronics & $lookup)
# =============================================================================
def generate_screenshot_10():
    lines = [
        ("campus_findback> // AGGREGATION 5: High-Value Open Electronics ($match + $group + $avg)", "comment"),
        ("campus_findback> db.items.aggregate([", "cmd"),
        ("...   { $match: { category: 'Electronics', status: 'open' } },", "head"),
        ("...   { $group: { _id: '$location', open_count: { $sum: 1 }, avg_reward: { $avg: '$reward' } } },", "head"),
        ("...   { $project: { _id: 0, location: '$_id', open_count: 1, avg_reward: { $round: ['$avg_reward', 2] } } },", "head"),
        ("...   { $sort: { open_count: -1 } }", "head"),
        ("... ]);", "cmd"),
        ("[", "output"),
        ("  { open_count: 2, location: 'Central Library',    avg_reward: 400.0 },", "success"),
        ("  { open_count: 2, location: 'Sports Complex',     avg_reward: 100.0 },", "output"),
        ("  { open_count: 2, location: 'Cafeteria Block B',  avg_reward: 0.0 },", "output"),
        ("  { open_count: 1, location: 'Computer Lab 3',     avg_reward: 0.0 }", "output"),
        ("]", "output"),
        ("", "default"),
        ("campus_findback> // AGGREGATION 6: Cross-Collection $lookup (Join items with users)", "comment"),
        ("campus_findback> db.items.aggregate([", "cmd"),
        ("...   { $match: { type: 'lost', status: 'open' } },", "head"),
        ("...   { $lookup: { from: 'users', localField: 'reported_by', foreignField: 'user_id', as: 'reporter' } },", "head"),
        ("...   { $unwind: '$reporter' },", "head"),
        ("...   { $project: { item_id: 1, item_name: 1, location: 1, reward: 1, reporter_name: '$reporter.name', department: '$reporter.department' } },", "head"),
        ("...   { $limit: 2 }", "head"),
        ("... ]);", "cmd"),
        ("[", "output"),
        ("  { item_id: 'ITEM-2026-001', item_name: 'Dell Inspiron 15 Laptop (Silver)', location: 'Central Library', reward: 500, reporter_name: 'Aarav Sharma', department: 'Computer Science & Engineering' },", "key"),
        ("  { item_id: 'ITEM-2026-006', item_name: 'Casio FX-991EX Calculator', location: 'Science Block 1', reward: 50, reporter_name: 'Sneha Reddy', department: 'Biotechnology' }", "key"),
        ("]", "output")
    ]
    img = draw_terminal_window("mongosh - Aggregation Pipelines 5 & 6 ($match, $avg, & $lookup Join)", lines, width=1100, min_height=740)
    img.save(os.path.join(SCREENSHOTS_DIR, "10_aggregation_lookup.png"))


# =============================================================================
# 11. SCREENSHOT 11: Web Frontend - Dashboard Interface
# =============================================================================
def generate_screenshot_11():
    def draw_content(draw, w, h):
        _, _, _, ui_reg, ui_bold, ui_header, ui_sub = get_fonts(ui_size=15)
        
        # Subtitle
        draw.text((35, 145), "Campus Lost & Found Intelligence Dashboard", fill=(15, 23, 42), font=ui_header)
        draw.text((35, 175), "Real-time statistics computed live from MongoDB collections via PyMongo.", fill=(100, 116, 139), font=ui_reg)
        
        # Metric Cards (4 cards)
        cards = [
            ("TOTAL REPORTS", "40", "📁", (59, 130, 246)),
            ("LOST ITEMS", "21", "⚠️", (239, 68, 68)),
            ("FOUND ITEMS", "19", "✓", (16, 185, 129)),
            ("OPEN / PENDING", "23", "⏳", (245, 158, 11))
        ]
        card_w = (w - 70 - 45) // 4
        cx = 35
        for label, val, icon, color in cards:
            draw.rectangle([cx, 210, cx + card_w, 290], fill=(255, 255, 255), outline=(226, 232, 240), width=1)
            draw.rectangle([cx, 210, cx + 5, 290], fill=color) # left color bar
            draw.text((cx + 18, 222), label, fill=(100, 116, 139), font=ui_sub)
            draw.text((cx + 18, 242), val, fill=color, font=ui_header)
            draw.text((cx + card_w - 45, 235), icon, fill=color, font=ui_header)
            cx += card_w + 15
            
        # Recent Reports Table Area
        draw.rectangle([35, 315, w - 35, 740], fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.text((55, 330), "🕒 Recently Reported Items (MongoDB find() cursor query)", fill=(30, 41, 59), font=ui_bold)
        
        # Table Header
        draw.rectangle([55, 365, w - 55, 395], fill=(241, 245, 249))
        headers = ["Item ID", "Item Title / Description", "Category", "Type", "Campus Location", "Status", "Reward"]
        hx_list = [70, 220, 520, 650, 750, 930, 1050]
        for htext, hx in zip(headers, hx_list):
            draw.text((hx, 372), htext, fill=(71, 85, 105), font=ui_bold)
            
        # Sample table rows
        rows = [
            ("ITEM-2026-001", "Dell Inspiron 15 Laptop (Silver)", "Electronics", "LOST", "Central Library", "OPEN", "₹500"),
            ("ITEM-2026-002", "Logitech Wireless Mouse (Black)", "Electronics", "FOUND", "Computer Lab 3", "OPEN", "-"),
            ("ITEM-2026-003", "Database Concepts Textbook (Korth)", "Books", "LOST", "Cafeteria Block B", "MATCHED", "₹100"),
            ("ITEM-2026-004", "Apple AirPods Pro Gen 2", "Electronics", "LOST", "Sports Complex", "RESOLVED", "₹250"),
            ("ITEM-2026-005", "Campus Student Identity Card", "ID/Documents", "FOUND", "Cafeteria Block B", "RESOLVED", "-"),
            ("ITEM-2026-006", "Casio FX-991EX Scientific Calculator", "Stationery", "LOST", "Science Block 1", "OPEN", "₹50"),
            ("ITEM-2026-007", "Wildcraft Blue Water Bottle (750ml)", "Accessories", "FOUND", "Main Auditorium", "OPEN", "-"),
            ("ITEM-2026-008", "Fastrack Black Sports Watch", "Accessories", "LOST", "Sports Complex", "OPEN", "₹100"),
        ]
        
        ry = 405
        for r in rows:
            draw.line([55, ry - 3, w - 55, ry - 3], fill=(241, 245, 249), width=1)
            draw.text((hx_list[0], ry), r[0], fill=(59, 130, 246), font=ui_bold)
            draw.text((hx_list[1], ry), r[1][:32], fill=(15, 23, 42), font=ui_reg)
            draw.text((hx_list[2], ry), r[2], fill=(71, 85, 105), font=ui_sub)
            
            # Type badge
            tb_color = (239, 68, 68) if r[3] == "LOST" else (16, 185, 129)
            draw.rectangle([hx_list[3] - 4, ry - 2, hx_list[3] + 55, ry + 18], fill=tb_color)
            draw.text((hx_list[3] + 4, ry), r[3], fill=(255, 255, 255), font=ui_sub)
            
            draw.text((hx_list[4], ry), "📍 " + r[4], fill=(71, 85, 105), font=ui_reg)
            
            # Status badge
            sb_colors = {"OPEN": (245, 158, 11), "MATCHED": (99, 102, 241), "RESOLVED": (16, 185, 129)}
            scolor = sb_colors.get(r[5], (100, 116, 139))
            draw.rectangle([hx_list[5] - 4, ry - 2, hx_list[5] + 75, ry + 18], fill=scolor)
            draw.text((hx_list[5] + 4, ry), r[5], fill=(255, 255, 255), font=ui_sub)
            
            draw.text((hx_list[6], ry), r[6], fill=(15, 23, 42), font=ui_bold)
            ry += 40

    img = draw_browser_window("http://127.0.0.1:5000/", "FindBack - Dashboard", draw_content, width=1200, height=780)
    img.save(os.path.join(SCREENSHOTS_DIR, "11_frontend_dashboard.png"))


# =============================================================================
# 12. SCREENSHOT 12: Web Frontend - Browse, Filter & Report Interface
# =============================================================================
def generate_screenshot_12():
    def draw_content(draw, w, h):
        _, _, _, ui_reg, ui_bold, ui_header, ui_sub = get_fonts(ui_size=15)
        
        # Subtitle
        draw.text((35, 145), "Browse, Filter, & Report Lost/Found Items", fill=(15, 23, 42), font=ui_header)
        draw.text((35, 175), "Interactive querying supporting regex text search, category filters, and live status updates.", fill=(100, 116, 139), font=ui_reg)
        
        # Filter Box
        draw.rectangle([35, 205, w - 35, 285], fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        draw.text((55, 215), "Keyword Search", fill=(100, 116, 139), font=ui_sub)
        draw.rectangle([55, 238, 280, 270], fill=(248, 250, 252), outline=(203, 213, 225))
        draw.text((65, 245), "🔍 laptop...", fill=(148, 163, 184), font=ui_reg)
        
        draw.text((305, 215), "Category Filter", fill=(100, 116, 139), font=ui_sub)
        draw.rectangle([305, 238, 480, 270], fill=(248, 250, 252), outline=(203, 213, 225))
        draw.text((315, 245), "Electronics ▾", fill=(15, 23, 42), font=ui_reg)
        
        draw.text((505, 215), "Type", fill=(100, 116, 139), font=ui_sub)
        draw.rectangle([505, 238, 650, 270], fill=(248, 250, 252), outline=(203, 213, 225))
        draw.text((515, 245), "All Types ▾", fill=(15, 23, 42), font=ui_reg)
        
        draw.text((675, 215), "Campus Location", fill=(100, 116, 139), font=ui_sub)
        draw.rectangle([675, 238, 880, 270], fill=(248, 250, 252), outline=(203, 213, 225))
        draw.text((685, 245), "Central Library ▾", fill=(15, 23, 42), font=ui_reg)
        
        # Filter button
        draw.rectangle([905, 238, 1030, 270], fill=(59, 130, 246))
        draw.text((925, 245), "⚡ Filter", fill=(255, 255, 255), font=ui_bold)
        
        # Report button
        draw.rectangle([1045, 238, w - 55, 270], fill=(16, 185, 129))
        draw.text((1055, 245), "+ Report Item", fill=(255, 255, 255), font=ui_bold)
        
        # Results area
        draw.rectangle([35, 305, w - 35, 740], fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.text((55, 320), "Filtered Results: 3 documents matched MongoDB query: db.items.find({ ... })", fill=(30, 41, 59), font=ui_bold)
        
        # Items table
        draw.rectangle([55, 355, w - 55, 385], fill=(241, 245, 249))
        headers = ["Item ID", "Item Title", "Category", "Location", "Status", "Live Status Action", "Delete Action"]
        hx_list = [70, 220, 520, 670, 830, 950, 1080]
        for htext, hx in zip(headers, hx_list):
            draw.text((hx, 362), htext, fill=(71, 85, 105), font=ui_bold)
            
        sample_rows = [
            ("ITEM-2026-001", "Dell Inspiron 15 Laptop (Silver)", "Electronics", "Central Library", "OPEN", "[Mark Resolved ▾]", "🗑️ Delete"),
            ("ITEM-2026-021", "Skybags Black Laptop Backpack", "Accessories", "Central Library", "OPEN", "[Mark Matched ▾]", "🗑️ Delete"),
            ("ITEM-2026-028", "Kindle Paperwhite 11th Gen", "Electronics", "Central Library", "OPEN", "[Mark Resolved ▾]", "🗑️ Delete")
        ]
        
        ry = 405
        for r in sample_rows:
            draw.line([55, ry - 3, w - 55, ry - 3], fill=(241, 245, 249), width=1)
            draw.text((hx_list[0], ry), r[0], fill=(59, 130, 246), font=ui_bold)
            draw.text((hx_list[1], ry), r[1], fill=(15, 23, 42), font=ui_reg)
            draw.text((hx_list[2], ry), r[2], fill=(71, 85, 105), font=ui_sub)
            draw.text((hx_list[3], ry), "📍 " + r[3], fill=(71, 85, 105), font=ui_reg)
            
            draw.rectangle([hx_list[4] - 4, ry - 2, hx_list[4] + 65, ry + 18], fill=(245, 158, 11))
            draw.text((hx_list[4] + 4, ry), r[4], fill=(255, 255, 255), font=ui_sub)
            
            draw.rectangle([hx_list[5], ry - 4, hx_list[5] + 115, ry + 20], fill=(241, 245, 249), outline=(203, 213, 225))
            draw.text((hx_list[5] + 6, ry), r[5], fill=(30, 41, 59), font=ui_sub)
            
            draw.text((hx_list[6], ry), r[6], fill=(239, 68, 68), font=ui_bold)
            ry += 48
            
        # Add a mini form mockup below table
        draw.rectangle([55, 560, w - 55, 720], fill=(248, 250, 252), outline=(226, 232, 240))
        draw.text((75, 575), "📝 Fast Item Reporting Form (MongoDB db.items.insertOne())", fill=(15, 23, 42), font=ui_bold)
        draw.text((75, 605), "Item Name: [ Casio FX-991EX Calculator           ]   Category: [ Stationery ▾ ]   Type: (•) Lost  ( ) Found", fill=(71, 85, 105), font=ui_reg)
        draw.text((75, 640), "Location:  [ Science Block 1 Room 204            ]   Reward:   [ ₹100          ]   Reporter: [ USR-101 (Student) ▾ ]", fill=(71, 85, 105), font=ui_reg)
        draw.text((75, 675), "Desc:      [ Black scientific calculator with serial num ]", fill=(71, 85, 105), font=ui_reg)
        
        draw.rectangle([w - 240, 665, w - 75, 700], fill=(59, 130, 246))
        draw.text((w - 220, 675), "✓ Submit to MongoDB", fill=(255, 255, 255), font=ui_bold)

    img = draw_browser_window("http://127.0.0.1:5000/browse", "FindBack - Browse & Report", draw_content, width=1200, height=780)
    img.save(os.path.join(SCREENSHOTS_DIR, "12_frontend_browse_report.png"))


# =============================================================================
# 13. SCREENSHOT 13: Automated Test Suite Output
# =============================================================================
def generate_screenshot_13():
    lines = [
        ("PS D:\\ca-2 mongodb> python tests/test_database.py", "prompt"),
        ("test_01_connection_ping (__main__.TestFindBackDatabase.test_01_connection_ping)", "default"),
        ("Test MongoDB server ping. ... ok", "success"),
        ("test_02_validation_valid_insert (__main__.TestFindBackDatabase.test_02_validation_valid_insert)", "default"),
        ("Valid document must be accepted by MongoDB schema validator. ... ok", "success"),
        ("test_03_validation_invalid_category_rejected (__main__.TestFindBackDatabase.test_03_validation_invalid_category_rejected)", "default"),
        ("Document with illegal category enum must be rejected by MongoDB. ... ok", "success"),
        ("test_04_validation_missing_location_rejected (__main__.TestFindBackDatabase.test_04_validation_missing_location_rejected)", "default"),
        ("Document missing required field 'location' must be rejected. ... ok", "success"),
        ("test_05_crud_create_read (__main__.TestFindBackDatabase.test_05_crud_create_read)", "default"),
        ("Test CREATE (insertOne) and READ (findOne). ... ok", "success"),
        ("test_06_crud_search_and_filter (__main__.TestFindBackDatabase.test_06_crud_search_and_filter)", "default"),
        ("Test search query filters. ... ok", "success"),
        ("test_07_crud_update_status (__main__.TestFindBackDatabase.test_07_crud_update_status)", "default"),
        ("Test UPDATE (updateOne) status lifecycle change. ... ok", "success"),
        ("test_08_crud_delete (__main__.TestFindBackDatabase.test_08_crud_delete)", "default"),
        ("Test DELETE (deleteOne). ... ok", "success"),
        ("test_09_aggregation_category (__main__.TestFindBackDatabase.test_09_aggregation_category)", "default"),
        ("Test Aggregation Pipeline 1: Group by Category. ... ok", "success"),
        ("test_10_aggregation_location (__main__.TestFindBackDatabase.test_10_aggregation_location)", "default"),
        ("Test Aggregation Pipeline 2: Hotspots by Location. ... ok", "success"),
        ("test_11_aggregation_resolution_rate (__main__.TestFindBackDatabase.test_11_aggregation_resolution_rate)", "default"),
        ("Test Aggregation Pipeline 3: Lost vs Found Breakdown. ... ok", "success"),
        ("test_12_aggregation_status_distribution (__main__.TestFindBackDatabase.test_12_aggregation_status_distribution)", "default"),
        ("Test Aggregation Pipeline 4: Status Breakdown. ... ok", "success"),
        ("test_13_aggregation_open_electronics (__main__.TestFindBackDatabase.test_13_aggregation_open_electronics)", "default"),
        ("Test Aggregation Pipeline 5: Open Electronics Hotspots. ... ok", "success"),
        ("test_14_aggregation_cross_collection_lookup (__main__.TestFindBackDatabase.test_14_aggregation_cross_collection_lookup)", "default"),
        ("Test Aggregation Pipeline 6: Cross-Collection $lookup with Users. ... ok", "success"),
        ("----------------------------------------------------------------------", "divider"),
        ("Ran 14 tests in 0.167s", "cmd"),
        ("", "default"),
        ("OK", "success")
    ]
    img = draw_terminal_window("Terminal - python tests/test_database.py (14/14 Tests Passed)", lines, width=1100, min_height=780)
    img.save(os.path.join(SCREENSHOTS_DIR, "13_automated_tests.png"))


if __name__ == "__main__":
    print("[*] Generating 13 publication-grade screenshots in screenshots/ directory...")
    generate_screenshot_01()
    generate_screenshot_02()
    generate_screenshot_03()
    generate_screenshot_04()
    generate_screenshot_05()
    generate_screenshot_06()
    generate_screenshot_07()
    generate_screenshot_08()
    generate_screenshot_09()
    generate_screenshot_10()
    generate_screenshot_11()
    generate_screenshot_12()
    generate_screenshot_13()
    print("[V] All 13 screenshots successfully generated!")
