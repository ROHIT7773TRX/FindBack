"""
Flask Web Application for FindBack.
Provides a clean, intuitive web interface to demonstrate:
- Dashboard metrics
- Item reporting (Create)
- Browsing, filtering, and text search (Read)
- Status lifecycle updates (Update)
- Report deletion (Delete)
- MongoDB Aggregation Analytics
- Live $jsonSchema Validation Testing
"""

import os
import random
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

load_dotenv()

from app.database import test_connection, get_items_collection
from app.models import CATEGORIES, ITEM_TYPES, STATUSES, CAMPUS_LOCATIONS, build_item_document
from app.crud import (
    create_item,
    get_items,
    get_item_by_id,
    search_items,
    update_item_status,
    delete_item,
    get_dashboard_counts,
    get_all_users
)
from app.analytics import (
    get_reports_by_category,
    get_reports_by_location,
    get_lost_vs_found_stats,
    get_status_distribution,
    get_open_electronics_by_location,
    get_items_with_reporter_details
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "findback-super-secret-key-for-session")


@app.route("/")
def dashboard():
    """Renders the main overview dashboard with real-time MongoDB metrics."""
    counts = get_dashboard_counts()
    recent_items = get_items(limit=8)
    top_locations = get_reports_by_location(limit=4)
    category_stats = get_reports_by_category()[:4]
    return render_template(
        "dashboard.html",
        title="Dashboard",
        counts=counts,
        recent_items=recent_items,
        top_locations=top_locations,
        category_stats=category_stats
    )


@app.route("/browse")
def browse():
    """Renders the item browsing, search, and filtering interface."""
    keyword = request.args.get("keyword")
    category = request.args.get("category")
    item_type = request.args.get("type")
    location = request.args.get("location")
    status = request.args.get("status")

    if any([keyword, category, item_type, location, status]):
        items = search_items(
            keyword=keyword,
            category=category,
            item_type=item_type,
            location=location,
            status=status
        )
    else:
        items = get_items(limit=100)

    return render_template(
        "browse.html",
        title="Browse & Search",
        items=items,
        categories=CATEGORIES,
        locations=CAMPUS_LOCATIONS,
        statuses=STATUSES
    )


@app.route("/report", methods=["GET", "POST"])
def report():
    """Handles item creation form submission and MongoDB insertion."""
    if request.method == "POST":
        item_id = request.form.get("item_id", "").strip()
        item_name = request.form.get("item_name", "").strip()
        category = request.form.get("category", "").strip()
        item_type = request.form.get("type", "").strip()
        description = request.form.get("description", "").strip()
        location = request.form.get("location", "").strip()
        reported_by = request.form.get("reported_by", "").strip()
        contact_email = request.form.get("contact_email", "").strip()
        reward = request.form.get("reward", "0").strip()
        tags_raw = request.form.get("tags", "").strip()

        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

        try:
            reward_val = float(reward) if reward else 0.0
        except ValueError:
            reward_val = 0.0

        doc = build_item_document(
            item_id=item_id,
            item_name=item_name,
            category=category,
            item_type=item_type,
            description=description,
            location=location,
            reported_by=reported_by,
            contact_email=contact_email,
            reward=reward_val,
            tags=tags
        )

        result = create_item(doc)
        if result["success"]:
            flash(f"Success: {result['message']}", "success")
            return redirect(url_for("browse"))
        else:
            flash(f"MongoDB Error [{result.get('error')}]: {result['message']}", "danger")

    suggested_id = f"ITEM-2026-{random.randint(100, 999)}"
    users = get_all_users()
    return render_template(
        "report.html",
        title="Report Item",
        suggested_id=suggested_id,
        categories=CATEGORIES,
        locations=CAMPUS_LOCATIONS,
        users=users
    )


@app.route("/update-status", methods=["POST"])
def update_status_route():
    """Updates an item's status via updateOne()."""
    item_id = request.form.get("item_id")
    new_status = request.form.get("status")

    if not item_id or not new_status:
        flash("Missing Item ID or Status.", "warning")
        return redirect(url_for("browse"))

    result = update_item_status(item_id, new_status)
    if result["success"]:
        flash(f"Status of item '{item_id}' updated to '{new_status}'.", "success")
    else:
        flash(f"Update failed: {result['message']}", "danger")

    return redirect(request.referrer or url_for("browse"))


@app.route("/delete-item", methods=["POST"])
def delete_item_route():
    """Deletes an item document via deleteOne()."""
    item_id = request.form.get("item_id")
    if not item_id:
        flash("Invalid item reference.", "warning")
        return redirect(url_for("browse"))

    result = delete_item(item_id)
    if result["success"]:
        flash(f"Report '{item_id}' deleted successfully from MongoDB.", "info")
    else:
        flash(f"Delete failed: {result['message']}", "danger")

    return redirect(request.referrer or url_for("browse"))


@app.route("/analytics")
def analytics():
    """Executes and renders the 6 MongoDB aggregation pipelines."""
    category_stats = get_reports_by_category()
    location_stats = get_reports_by_location(limit=10)
    type_stats = get_lost_vs_found_stats()
    status_stats = get_status_distribution()
    electronics_stats = get_open_electronics_by_location()
    lookup_stats = get_items_with_reporter_details(limit=10)

    return render_template(
        "analytics.html",
        title="Aggregation Analytics",
        category_stats=category_stats,
        location_stats=location_stats,
        type_stats=type_stats,
        status_stats=status_stats,
        electronics_stats=electronics_stats,
        lookup_stats=lookup_stats
    )


@app.route("/validation-demo")
def validation_demo():
    """Renders the validation demonstration interface."""
    return render_template("validation.html", title="Schema Validation")


@app.route("/validation-demo/run", methods=["POST"])
def validation_demo_run():
    """Executes live validation tests and reports MongoDB's exact response."""
    test_type = request.form.get("test_type")
    col = get_items_collection()
    now = datetime.now(timezone.utc)

    if test_type == "valid":
        doc = {
            "item_id": f"TEST-VAL-{random.randint(100, 999)}",
            "item_name": "Operating Systems Concepts",
            "category": "Books",
            "type": "lost",
            "description": "Hardcover Silberschatz OS dinosaur textbook.",
            "location": "Central Library",
            "date_reported": now,
            "status": "open",
            "reported_by": "USR-101",
            "created_at": now,
            "updated_at": now
        }
        res = create_item(doc)
        if res["success"]:
            flash(f"[VALIDATION SUCCESS] Document inserted! MongoDB _id: {res['inserted_id']}", "success")
        else:
            flash(f"[FAILED] {res['message']}", "danger")

    elif test_type == "invalid_category":
        doc = {
            "item_id": f"TEST-VAL-{random.randint(100, 999)}",
            "item_name": "Prohibited Item Test",
            "category": "ILLEGAL_CATEGORY_TEST",
            "type": "lost",
            "description": "Testing category enum validation rejection.",
            "location": "Hostel Block C",
            "date_reported": now,
            "status": "open",
            "reported_by": "USR-101",
            "created_at": now,
            "updated_at": now
        }
        res = create_item(doc)
        if not res["success"]:
            flash(f"[VALIDATION REJECTED AS EXPECTED] MongoDB $jsonSchema caught enum violation: {res['message']}", "danger")
        else:
            flash("Unexpected: Document was accepted without valid category.", "warning")

    elif test_type == "missing_location":
        doc = {
            "item_id": f"TEST-VAL-{random.randint(100, 999)}",
            "item_name": "Item Missing Location",
            "category": "Stationery",
            "type": "lost",
            "description": "Testing required location field rejection.",
            "date_reported": now,
            "status": "open",
            "reported_by": "USR-101",
            "created_at": now,
            "updated_at": now
        }
        res = create_item(doc)
        if not res["success"]:
            flash(f"[VALIDATION REJECTED AS EXPECTED] MongoDB rejected document because mandatory 'location' was omitted.", "danger")
        else:
            flash("Unexpected: Document was accepted without required location.", "warning")

    elif test_type == "invalid_status":
        doc = {
            "item_id": f"TEST-VAL-{random.randint(100, 999)}",
            "item_name": "Item Invalid Status",
            "category": "Accessories",
            "type": "lost",
            "description": "Testing status enum violation.",
            "location": "Cafeteria Block B",
            "date_reported": now,
            "status": "in_review",
            "reported_by": "USR-101",
            "created_at": now,
            "updated_at": now
        }
        res = create_item(doc)
        if not res["success"]:
            flash(f"[VALIDATION REJECTED AS EXPECTED] MongoDB rejected invalid status 'in_review' (Allowed: open, matched, resolved, closed).", "danger")
        else:
            flash("Unexpected: Document was accepted with invalid status.", "warning")

    return redirect(url_for("validation_demo"))


def create_app():
    return app


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    print(f"[*] Starting FindBack Flask Server on http://127.0.0.1:{port} ...")
    app.run(host="127.0.0.1", port=port, debug=debug)
