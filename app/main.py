"""
FindBack — Main Application Launcher
Usage:
    python -m app.main           # Launches interactive Terminal CLI
    python -m app.main --web     # Launches Flask Web UI (http://127.0.0.1:5000)
    python -m app.main --cli     # Explicitly launches CLI
"""

import sys
import os

# Add project root to Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import test_connection


def main():
    print("=" * 60)
    print("  FINDBACK: Campus Lost & Found Intelligence System")
    print("=" * 60)

    # Check MongoDB connection
    if not test_connection():
        print("[!] ERROR: Cannot connect to MongoDB server.")
        print("    Please ensure your MongoDB service is running on port 27017.")
        print("    Run 'mongod' or start the MongoDB Windows service.")
        sys.exit(1)

    # Check command line arguments
    if "--web" in sys.argv or "-w" in sys.argv:
        from app.web_app import app
        port = int(os.getenv("FLASK_PORT", 5000))
        print(f"[+] Starting FindBack Web Application at http://127.0.0.1:{port}")
        print("    Press Ctrl+C to stop the web server.\n")
        app.run(host="127.0.0.1", port=port, debug=True)
    else:
        from app.cli import run_cli
        run_cli()


if __name__ == "__main__":
    main()
