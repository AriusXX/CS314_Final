# models/reports.py
import os
import json
from datetime import datetime
from .member import MemberDatabase
from .provider import Provider

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)

def _load_transactions():
    path = os.path.join(DATA_DIR, "transactions.json")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def generate_member_reports():
    members_db = MemberDatabase()
    txs = _load_transactions()
    today_str = datetime.now().strftime("%Y%m%d")

    # Group by member_num
    by_member = {}
    for t in txs:
        by_member.setdefault(t["member_num"], []).append(t)

    for member_num, services in by_member.items():
        member = members_db.get_member(member_num)
        if member is None:
            continue

        filename = f"{member.name.replace(' ', '_')}_{today_str}.txt"
        filepath = os.path.join(REPORTS_DIR, filename)

        with open(filepath, "w") as out:
            out.write(f"Member name: {member.name}\n")
            out.write(f"Member number: {member.number}\n")
            out.write(f"Address: {member.address}, {member.city}, {member.state} {member.zip_code}\n\n")

            # For each service: date of service, provider name, service name
            # You’ll need Provider lookup + ServiceDirectory here
            # (stub out now, fill later)
