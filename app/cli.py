"""
Interactive Terminal Interface for FindBack.
Allows live demonstration of CRUD, Aggregations, and Validation during Viva.
"""

import sys
import os
from datetime import datetime, timezone
from tabulate import tabulate
from colorama import init, Fore, Style

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import test_connection, get_db
from app.models import CATEGORIES, ITEM_TYPES, STATUSES, CAMPUS_LOCATIONS, build_item_document
from app.crud import (
    create_item,
    get_items,
    get_item_by_id,
    search_items,
    update_item_status,
    delete_item,
    get_dashboard_counts
)
from app.analytics import (
    get_reports_by_category,
    get_reports_by_location,
    get_lost_vs_found_stats,
    get_status_distribution,
    get_open_electronics_by_location,
    get_items_with_reporter_details
)

init(autoreset=True)


def print_banner():
    print(Fore.CYAN + Style.BRIGHT + "=" * 65)
    print(Fore.YELLOW + Style.BRIGHT + "  FINDBACK — Campus Lost & Found Intelligence System")
    print(Fore.CYAN + "  MongoDB & PyMongo CA-2 Academic Project Demonstration")
    print(Fore.CYAN + Style.BRIGHT + "=" * 65)


def show_dashboard():
    print(Fore.GREEN + "\n--- REAL-TIME MONGODB DASHBOARD METRICS ---")
    counts = get_dashboard_counts()
    data = [
        ["Total Registered Reports", counts["total_reports"]],
        ["Lost Items Filed", counts["lost_items"]],
        ["Found Items Reported", counts["found_items"]],
        ["Open (Pending Action)", counts["open_reports"]],
        ["Matched (Possible Owner Found)", counts["matched_reports"]],
        ["Resolved (Returned to Owner)", counts["resolved_reports"]],
        ["Closed", counts["closed_reports"]],
    ]
    print(tabulate(data, headers=["Metric", "Count"], tablefmt="fancy_grid"))


def handle_view_items():
    print(Fore.GREEN + "\n--- BROWSE / FILTER ITEMS FROM MONGODB ---")
    print("1. View All Items (Latest 15)")
    print("2. Filter by Category")
    print("3. Filter by Type (Lost / Found)")
    print("4. Filter by Status (Open / Matched / Resolved)")
    print("5. Search Keyword")
    choice = input(Fore.YELLOW + "Select filter option (1-5): ").strip()

    items = []
    if choice == "1":
        items = get_items(limit=15)
    elif choice == "2":
        print(f"Available Categories: {', '.join(CATEGORIES)}")
        cat = input("Enter Category: ").strip()
        items = search_items(category=cat)
    elif choice == "3":
        t = input("Enter Type (lost / found): ").strip()
        items = search_items(item_type=t)
    elif choice == "4":
        s = input("Enter Status (open / matched / resolved / closed): ").strip()
        items = search_items(status=s)
    elif choice == "5":
        kw = input("Enter keyword (item name, tag, location): ").strip()
        items = search_items(keyword=kw)
    else:
        items = get_items(limit=10)

    if not items:
        print(Fore.RED + "[-] No items found matching the specified query.")
        return

    table_data = []
    for item in items:
        table_data.append([
            item.get("item_id"),
            item.get("item_name")[:25],
            item.get("category"),
            item.get("type").upper(),
            item.get("location")[:18],
            item.get("status"),
            f"₹{item.get('reward', 0)}"
        ])

    print(tabulate(
        table_data,
        headers=["Item ID", "Name", "Category", "Type", "Location", "Status", "Reward"],
        tablefmt="grid"
    ))
    print(f"Total matching documents retrieved from MongoDB: {len(items)}")


def handle_report_item():
    print(Fore.GREEN + "\n--- REPORT NEW ITEM (CREATE: insertOne) ---")
    print("Note: This operation is validated in real-time by MongoDB $jsonSchema.")
    
    item_id = input("Enter Item ID (e.g., ITEM-2026-099): ").strip()
    if not item_id:
        import random
        item_id = f"ITEM-2026-{random.randint(100, 999)}"
        print(f"Auto-generated Item ID: {item_id}")

    name = input("Item Name (e.g., Blue Casio Calculator): ").strip()
    print(f"Categories: {CATEGORIES}")
    category = input("Category: ").strip()
    print("Type: lost / found")
    item_type = input("Type (lost/found): ").strip()
    desc = input("Description: ").strip()
    print(f"Locations: {CAMPUS_LOCATIONS}")
    location = input("Location: ").strip()
    reporter = input("Reported By (User ID, e.g. USR-101): ").strip() or "USR-101"
    contact_email = input("Contact Email: ").strip() or "student@campus.edu"
    reward_input = input("Reward Amount in ₹ (0 for none): ").strip() or "0"
    
    try:
        reward = float(reward_input)
    except ValueError:
        reward = 0.0

    doc = build_item_document(
        item_id=item_id,
        item_name=name,
        category=category,
        item_type=item_type,
        description=desc,
        location=location,
        reported_by=reporter,
        contact_email=contact_email,
        reward=reward
    )

    print(Fore.CYAN + "\nSending document to MongoDB via PyMongo...")
    res = create_item(doc)
    if res["success"]:
        print(Fore.GREEN + f"[V] SUCCESS: {res['message']} (MongoDB _id: {res.get('inserted_id')})")
    else:
        print(Fore.RED + f"[X] ERROR [{res.get('error')}]: {res['message']}")


def handle_update_status():
    print(Fore.GREEN + "\n--- UPDATE ITEM STATUS (UPDATE: updateOne) ---")
    item_id = input("Enter Item ID to update (e.g. ITEM-2026-001): ").strip()
    doc = get_item_by_id(item_id)
    if not doc:
        print(Fore.RED + f"[-] Item with ID '{item_id}' not found.")
        return

    print(f"Current Status of '{doc.get('item_name')}': {Fore.YELLOW}{doc.get('status')}")
    print("Allowed Statuses: open, matched, resolved, closed")
    new_status = input("Enter new status: ").strip().lower()

    if new_status not in STATUSES:
        print(Fore.RED + f"[-] Invalid status '{new_status}'. Allowed: {STATUSES}")
        return

    res = update_item_status(item_id, new_status)
    if res["success"]:
        print(Fore.GREEN + f"[V] SUCCESS: {res['message']}")
    else:
        print(Fore.RED + f"[X] UPDATE FAILED: {res.get('message')}")


def handle_delete_item():
    print(Fore.GREEN + "\n--- DELETE AN ITEM (DELETE: deleteOne) ---")
    item_id = input("Enter Item ID to delete (e.g. ITEM-2026-041): ").strip()
    doc = get_item_by_id(item_id)
    if not doc:
        print(Fore.RED + f"[-] Item with ID '{item_id}' not found.")
        return

    confirm = input(f"Are you sure you want to permanently delete '{doc.get('item_name')}'? (y/N): ").strip().lower()
    if confirm == 'y':
        res = delete_item(item_id)
        if res["success"]:
            print(Fore.GREEN + f"[V] SUCCESS: {res['message']}")
        else:
            print(Fore.RED + f"[X] DELETE FAILED: {res.get('message')}")
    else:
        print("Deletion cancelled.")


def handle_analytics():
    while True:
        print(Fore.CYAN + "\n==========================================")
        print(Fore.YELLOW + "     MONGODB AGGREGATION ANALYTICS")
        print(Fore.CYAN + "==========================================")
        print("1. Aggregation 1: Total Reports by Category ($group, $project, $sort)")
        print("2. Aggregation 2: Top Campus Location Hotspots ($group, $sort, $limit)")
        print("3. Aggregation 3: Lost vs Found Breakdown & Resolution Rate")
        print("4. Aggregation 4: Status Distribution")
        print("5. Aggregation 5: Open High-Value Electronics Hotspots ($match, $group, $avg)")
        print("6. Aggregation 6: Item & User Join ($lookup, $unwind)")
        print("7. Return to Main Menu")
        
        choice = input(Fore.YELLOW + "\nSelect aggregation pipeline (1-7): ").strip()
        if choice == "1":
            print(Fore.GREEN + "\n--- AGGREGATION 1: Reports by Category ---")
            data = get_reports_by_category()
            table = [[d["category"], d["total_reports"], d["lost_count"], d["found_count"]] for d in data]
            print(tabulate(table, headers=["Category", "Total Reports", "Lost", "Found"], tablefmt="fancy_grid"))
        elif choice == "2":
            print(Fore.GREEN + "\n--- AGGREGATION 2: Campus Hotspots (Top 5) ---")
            data = get_reports_by_location(limit=5)
            table = [[d["location"], d["report_count"], d["unresolved_count"]] for d in data]
            print(tabulate(table, headers=["Campus Location", "Total Reports", "Unresolved Reports"], tablefmt="fancy_grid"))
        elif choice == "3":
            print(Fore.GREEN + "\n--- AGGREGATION 3: Lost vs Found Resolution Rate ---")
            data = get_lost_vs_found_stats()
            table = [[d["report_type"].upper(), d["total_items"], d["resolved_items"], d["open_items"], f"{d['resolution_rate_percent']}%"] for d in data]
            print(tabulate(table, headers=["Type", "Total Items", "Resolved", "Open", "Resolution %"], tablefmt="fancy_grid"))
        elif choice == "4":
            print(Fore.GREEN + "\n--- AGGREGATION 4: Lifecycle Status Distribution ---")
            data = get_status_distribution()
            table = [[d["status"].upper(), d["count"]] for d in data]
            print(tabulate(table, headers=["Status", "Count"], tablefmt="fancy_grid"))
        elif choice == "5":
            print(Fore.GREEN + "\n--- AGGREGATION 5: Open Electronics Hotspots & Avg Reward ---")
            data = get_open_electronics_by_location()
            table = [[d["location"], d["open_electronics_count"], f"₹{d['average_reward']}"] for d in data]
            print(tabulate(table, headers=["Location", "Open Electronics Count", "Average Reward"], tablefmt="fancy_grid"))
        elif choice == "6":
            print(Fore.GREEN + "\n--- AGGREGATION 6: Item & User Join ($lookup cross-collection) ---")
            data = get_items_with_reporter_details(limit=5)
            table = [[d["item_id"], d["item_name"][:20], d["category"], d.get("reporter_name", "N/A"), d.get("department", "N/A"), d.get("reporter_role", "N/A")] for d in data]
            print(tabulate(table, headers=["Item ID", "Item Name", "Category", "Reporter Name", "Department", "Role"], tablefmt="fancy_grid"))
        elif choice == "7":
            break


def run_cli():
    print_banner()
    if not test_connection():
        print(Fore.RED + "[!] FATAL: Cannot connect to MongoDB server. Start MongoDB and try again.")
        return

    while True:
        print(Fore.CYAN + "\n" + "=" * 50)
        print(Fore.YELLOW + "               MAIN MENU")
        print(Fore.CYAN + "=" * 50)
        print("1. View Dashboard & Real-Time Stats")
        print("2. Browse / Search Items (READ: find, findOne)")
        print("3. Report New Lost / Found Item (CREATE: insertOne)")
        print("4. Update Item Status (UPDATE: updateOne)")
        print("5. Delete an Item Report (DELETE: deleteOne)")
        print("6. Run MongoDB Aggregation Analytics (Pipelines 1-6)")
        print("7. Run Schema Validation Demonstration ($jsonSchema)")
        print("8. Exit Application")
        
        choice = input(Fore.YELLOW + "\nEnter choice (1-8): ").strip()
        if choice == "1":
            show_dashboard()
        elif choice == "2":
            handle_view_items()
        elif choice == "3":
            handle_report_item()
        elif choice == "4":
            handle_update_status()
        elif choice == "5":
            handle_delete_item()
        elif choice == "6":
            handle_analytics()
        elif choice == "7":
            from scripts.demo_validation import run_validation_demonstration
            run_validation_demonstration()
        elif choice == "8":
            print(Fore.GREEN + "\nThank you for using FindBack! Exiting...")
            break
        else:
            print(Fore.RED + "Invalid selection. Please choose an option from 1 to 8.")


if __name__ == "__main__":
    run_cli()
