# FindBack — Campus Lost & Found Intelligence System
> **Academic MongoDB Continuous Assessment (CA-2) Project**  
> *A clean, complete, and demonstrable MongoDB & PyMongo application.*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-8.0%2B-green.svg)](https://www.mongodb.com/)
[![PyMongo](https://img.shields.io/badge/PyMongo-4.18-brightgreen.svg)](https://pymongo.readthedocs.io/)
[![Flask](https://img.shields.io/badge/Flask-3.1-black.svg)](https://flask.palletsprojects.com/)
[![Tests](https://img.shields.io/badge/Tests-14%2F14%20Passing-success.svg)]()

---

## 1. Project Overview

**FindBack** is a database-first campus lost-and-found intelligence system built for university environments. Misplacing valuables (laptops, books, calculators, ID cards, keys) is a frequent problem on campus. Traditional physical registers or chat groups lack searchability, data integrity, and analytical insights.

FindBack provides a centralized, document-oriented database in **MongoDB** that:
- Captures detailed lost and found reports.
- Enforces data integrity using server-side **MongoDB `$jsonSchema` collection validation**.
- Provides rapid multi-criteria **CRUD operations** (Create, Read, Update, Delete).
- Generates real-time campus intelligence using multi-stage **MongoDB Aggregation Pipelines**.
- Features both an interactive **Terminal CLI** and a clean **Flask Web UI** for live demonstration.

---

## 2. Key Features

-  **Strict Schema Validation:** Native `$jsonSchema` prevents missing required fields, illegal enums, and negative rewards.
-  **Complete CRUD Operations:** Demonstrated in both Python (PyMongo) and native MongoDB Shell (`mongosh`).
-  **6 Aggregation Pipelines:** Multi-stage analytics including category ranking, campus hotspots, recovery rates, and cross-collection joins (`$lookup`).
-  **Interactive Terminal CLI:** Color-coded menu interface with formatted tables for rapid query demonstration during viva.
-  **Flask Web Dashboard:** Visual metrics, reporting forms, status manager, filterable search, and aggregation displays.
-  **Automated Test Suite:** 14 automated unit and integration tests verifying database health.

---

## 3. Technology Stack

- **Database:** MongoDB Community Server (v8.0+)
- **Integration Driver:** PyMongo (v4.18+)
- **Programming Language:** Python 3.13+
- **Web UI Framework:** Flask 3.1+ & Bootstrap 5
- **CLI Utilities:** Tabulate, Colorama
- **Configuration:** Python-Dotenv

---

## 4. System Architecture

```
User (Student / Staff / Admin)
             │
             ▼
   Application Interfaces
   ├── Terminal CLI (app/cli.py)
   └── Flask Web UI (app/web_app.py)
             │
             ▼
      Python Logic Layer
   ├── models.py     (Schemas & Constants)
   ├── crud.py       (CRUD Functions)
   └── analytics.py  (Aggregation Pipelines)
             │
             ▼
     PyMongo Driver (MongoClient)
             │
             ▼
   MongoDB Engine (Database: campus_findback)
   ├── Collection: users (12 documents)
   └── Collection: items (40 documents)
```

---

## 5. Database & Collection Design

### Database Name: `campus_findback`

### 1. Collection: `users`
| Field | Type | Description |
|---|---|---|
| `_id` | `ObjectId` | Auto-generated primary key |
| `user_id` | `string` | Unique identifier (e.g., `USR-101`) |
| `name` | `string` | Full name of student/faculty |
| `email` | `string` | Campus email (regex-validated) |
| `role` | `string` | Enum: `student`, `faculty`, `staff`, `admin` |
| `department` | `string` | Department / School |
| `created_at` | `date` | Account creation timestamp |

### 2. Collection: `items`
| Field | Type | Description |
|---|---|---|
| `_id` | `ObjectId` | Auto-generated primary key |
| `item_id` | `string` | Unique reference ID (e.g., `ITEM-2026-001`) |
| `item_name` | `string` | Title of item (2-100 characters) |
| `category` | `string` | Enum: `Electronics`, `Books`, `Stationery`, `Clothing`, `Accessories`, `ID/Documents`, `Other` |
| `type` | `string` | Enum: `lost` or `found` |
| `description` | `string` | Physical description, distinguishing marks |
| `location` | `string` | Campus location where lost/found |
| `date_reported`| `date` | Date of incident/report |
| `status` | `string` | Enum: `open`, `matched`, `resolved`, `closed` |
| `reported_by` | `string` | Reference to `user_id` |
| `reward` | `number` | Optional monetary reward (>= 0) |
| `tags` | `array` | Array of search tags (e.g., `["dell", "laptop"]`) |
| `created_at` | `date` | Timestamp when record was created |
| `updated_at` | `date` | Timestamp when record was last updated |

---

## 6. Prerequisites

Ensure you have the following installed on your machine:
1. **Python 3.10+** ([python.org](https://www.python.org/downloads/))
2. **MongoDB Community Server 7.0+ or 8.0+** ([mongodb.com](https://www.mongodb.com/try/download/community))
3. **MongoDB Shell (`mongosh`)** or **MongoDB Compass** (Optional for visual inspection)
4. **Git**

---

## 7. Step-by-Step Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/username/FindBack.git
cd FindBack
```

### Step 2: Create and Activate Virtual Environment
**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## 8. Environment Configuration

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(On Windows: `copy .env.example .env`)*

Default configuration in `.env`:
```env
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=campus_findback
FLASK_PORT=5000
FLASK_DEBUG=True
SECRET_KEY=findback-dev-secret-key
```

---

## 9. Database Setup & Seeding

Run the seed script to create collections, configure `$jsonSchema` validation, set up indexes, and insert 12 users and 40 items:

```bash
python scripts/seed_data.py
```

---

## 10. Running the Application

### Option A: Interactive Terminal CLI (Recommended for Fast Viva Demos)
```bash
python -m app.main
```
or
```bash
python app/cli.py
```

### Option B: Flask Web Application
```bash
python -m app.main --web
```
Open your browser at: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 11. MongoDB Queries & Native Scripts

| File | Purpose | Execution Command |
|---|---|---|
| [mongodb/validation.js](file:///d:/ca-2%20mongodb/mongodb/validation.js) | `$jsonSchema` collection validation & indexes | `mongosh mongodb/validation.js` |
| [mongodb/crud_queries.js](file:///d:/ca-2%20mongodb/mongodb/crud_queries.js) | Native CRUD queries (`insertOne`, `find`, `updateOne`, `deleteOne`) | `mongosh mongodb/crud_queries.js` |
| [mongodb/aggregation_queries.js](file:///d:/ca-2%20mongodb/mongodb/aggregation_queries.js) | 6 Multi-stage aggregation pipelines | `mongosh mongodb/aggregation_queries.js` |
| [mongodb/sample_data.json](file:///d:/ca-2%20mongodb/mongodb/sample_data.json) | 40 items and 12 users sample dataset | Seeded via `seed_data.py` |

---

## 12. Aggregation Pipelines Summary

1. **Pipeline 1: Reports by Category** (`$group`, `$project`, `$sort`) — Identifies highest reporting categories.
2. **Pipeline 2: Location Hotspots** (`$group`, `$sort`, `$limit`) — Identifies top campus areas with highest incidents.
3. **Pipeline 3: Lost vs Found Recovery Rate** (`$group`, `$project`, `$round`) — Calculates recovery percentage.
4. **Pipeline 4: Status Breakdown** (`$group`, `$sort`) — Tracks lifecycle distribution (`open`, `matched`, `resolved`).
5. **Pipeline 5: High-Value Open Electronics** (`$match`, `$group`, `$avg`) — Evaluates pending electronics and average rewards.
6. **Pipeline 6: Cross-Collection Join** (`$lookup`, `$unwind`, `$project`) — Joins items with reporter details.

---

## 13. Running Automated Tests

Run the test suite covering connection, validation rules, CRUD, and aggregations:

```bash
python tests/test_database.py
```
*Expected Output:* **`Ran 14 tests in 0.228s -> OK`**

---

## 14. Project Structure

```
FindBack/
├── app/
│   ├── __init__.py           # Package initializer
│   ├── database.py           # PyMongo connection manager
│   ├── models.py             # Schema rules, constants, & doc constructor
│   ├── crud.py               # Create, Read, Update, Delete PyMongo functions
│   ├── analytics.py          # 6 PyMongo aggregation pipelines
│   ├── cli.py                # Interactive Terminal CLI
│   ├── web_app.py            # Flask Web Application routes
│   ├── templates/            # HTML templates (Bootstrap 5)
│   │   ├── layout.html
│   │   ├── dashboard.html
│   │   ├── report.html
│   │   ├── browse.html
│   │   ├── analytics.html
│   │   └── validation.html
│   └── main.py               # Unified application launcher
│
├── mongodb/
│   ├── validation.js         # Native mongosh schema validation
│   ├── crud_queries.js       # Native mongosh CRUD query examples
│   ├── aggregation_queries.js# Native mongosh aggregation pipelines
│   └── sample_data.json      # 40 items & 12 users JSON dataset
│
├── scripts/
│   ├── setup_database.py     # Database initializer script
│   ├── seed_data.py          # Dataset population script
│   └── demo_validation.py    # Schema validation rejection demonstration
│
├── tests/
│   └── test_database.py      # Automated 14-test test suite
│
├── screenshots/
│   └── SCREENSHOTS_GUIDE.md  # Screenshot guide & output logs
│
├── docs/
│   ├── PROJECT_GUIDE.md      # Master project understanding guide (20 sections)
│   ├── VIVA_PREPARATION.md   # 50+ Viva Q&A + 20 Practice Queries
│   ├── PRESENTATION_GUIDE.md # 10-slide presentation script & demo flow
│   └── PROJECT_REPORT.md     # Academic project report
│
├── .env.example              # Environment variables template
├── .env                      # Local environment configuration
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT License
└── README.md                 # Main project documentation
```

---

## 15. Documentation Quick Links

- [ Master Project Understanding Guide](file:///d:/ca-2%20mongodb/docs/PROJECT_GUIDE.md)
- [ 50+ Viva Questions & 20 Practice Queries](file:///d:/ca-2%20mongodb/docs/VIVA_PREPARATION.md)
- [ 10-Slide Presentation Guide & Demo Flow](file:///d:/ca-2%20mongodb/docs/PRESENTATION_GUIDE.md)
- [ Academic Project Report](file:///d:/ca-2%20mongodb/docs/PROJECT_REPORT.md)
- [ Screenshots & Output Guide](file:///d:/ca-2%20mongodb/screenshots/SCREENSHOTS_GUIDE.md)

---

## 16. License

This project is open source and available under the [MIT License](file:///d:/ca-2%20mongodb/LICENSE).
