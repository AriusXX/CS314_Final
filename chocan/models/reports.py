import os
import json
from datetime import datetime
from .member import MemberDatabase
from .provider import ProviderDatabase
from .service_directory import ServiceDirectory

# Directories
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)

# -------------------------------------------------------------------
# Load all transactions
# -------------------------------------------------------------------
def _load_transactions():
    path = os.path.join(DATA_DIR, "transactions.json")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# -------------------------------------------------------------------
#  MEMBER REPORTS
# -------------------------------------------------------------------
def generate_member_reports():
    members_db = MemberDatabase()
    txs = _load_transactions()
    today_str = datetime.now().strftime("%Y%m%d")

    by_member = {}
    for t in txs:
        by_member.setdefault(t["member_num"], []).append(t)

    generated_paths = []

    directory = ServiceDirectory()

    for member_num, services in by_member.items():
        member = members_db.get_member(member_num)
        if member is None:
            continue

        filename = f"{member.name.replace(' ', '_')}_{today_str}.txt"
        filepath = os.path.join(REPORTS_DIR, filename)

        total_fee = 0.0

        with open(filepath, "w") as out:

            out.write(f"Member name: {member.name}\n")
            out.write(f"Member number: {member.number}\n")
            out.write(f"Address: {member.address}, {member.city}, {member.state} {member.zip_code}\n\n")

            for t in services:
                service_info = directory.lookup(t["service_code"])

                if service_info:
                    service_name = service_info["name"]
                    fee = float(service_info["fee"])
                else:
                    service_name = "Unknown Service"
                    fee = 0.0

                total_fee += fee

                out.write(f"Service Date: {t['service_date']}\n")
                out.write(f"Provider Number: {t['provider_num']}\n")
                out.write(f"Service Name: {service_name}\n")
                out.write(f"Fee: ${fee:.2f}\n\n")

            out.write(f"Total Fee for Member: ${total_fee:.2f}\n")

        generated_paths.append(filepath)

    return generated_paths


# -------------------------------------------------------------------
#  PROVIDER REPORTS
# -------------------------------------------------------------------
def generate_provider_reports():
    txs = _load_transactions()
    today_str = datetime.now().strftime("%Y%m%d")

    by_provider = {}
    for t in txs:
        by_provider.setdefault(t["provider_num"], []).append(t)

    generated_paths = []

    provider_db = ProviderDatabase()
    members_db = MemberDatabase()
    directory = ServiceDirectory()

    for provider_num, services in by_provider.items():
        provider = provider_db.get_provider(provider_num)
        if provider is None:
            continue

        filename = f"{provider.name.replace(' ', '_')}_{today_str}.txt"
        filepath = os.path.join(REPORTS_DIR, filename)

        total_fee = 0.0
        service_count = 0

        with open(filepath, "w") as out:
            out.write(f"Provider Name: {provider.name}\n")
            out.write(f"Provider Number: {provider.number}\n")
            out.write(f"Address: {provider.address}, {provider.city}, {provider.state} {provider.zip}\n\n")

            for t in services:
                service_count += 1

                # Service info
                service_info = directory.lookup(t["service_code"])
                if service_info:
                    service_name = service_info["name"]
                    fee = float(service_info["fee"])
                else:
                    service_name = "Unknown Service"
                    fee = 0.0

                total_fee += fee

                # Member info
                member_obj = members_db.get_member(t["member_num"])
                member_name = member_obj.name if member_obj else "Unknown Member"

                out.write(f"Date of Service: {t['service_date']}\n")
                out.write(f"Date Received: {t['current_datetime']}\n")
                out.write(f"Member Name: {member_name}\n")
                out.write(f"Member Number: {t['member_num']}\n")
                out.write(f"Service Code: {t['service_code']}\n")
                out.write(f"Service Name: {service_name}\n")
                out.write(f"Fee: ${fee:.2f}\n\n")

            out.write("----- Totals -----\n")
            out.write(f"Total Consultations: {service_count}\n")
            out.write(f"Total Fee to Provider: ${total_fee:.2f}\n")

        generated_paths.append(filepath)

    return generated_paths


# -------------------------------------------------------------------
#  SUMMARY REPORT
# -------------------------------------------------------------------
def generate_summary_report():
    txs = _load_transactions()
    today_str = datetime.now().strftime("%Y%m%d")

    filepath = os.path.join(REPORTS_DIR, f"Summary_{today_str}.txt")

    provider_totals = {}  # provider_num: {"count": X, "fee": Y}
    directory = ServiceDirectory()

    for t in txs:
        provider_num = t["provider_num"]

        if provider_num not in provider_totals:
            provider_totals[provider_num] = {"count": 0, "fee": 0.0}

        provider_totals[provider_num]["count"] += 1

        service_info = directory.lookup(t["service_code"])
        if service_info:
            provider_totals[provider_num]["fee"] += float(service_info["fee"])

    with open(filepath, "w") as out:
        out.write("====== Summary Report ======\n\n")

        overall_count = 0
        overall_fee = 0.0

        for provider_num, data in provider_totals.items():
            overall_count += data["count"]
            overall_fee += data["fee"]

            out.write(f"Provider {provider_num} — Consultations: {data['count']}, Total Fee: ${data['fee']:.2f}\n")

        out.write("\n----- System Totals -----\n")
        out.write(f"Total Providers Paid: {len(provider_totals)}\n")
        out.write(f"Total Services Provided: {overall_count}\n")
        out.write(f"Total Overall Fee: ${overall_fee:.2f}\n")

    return filepath
