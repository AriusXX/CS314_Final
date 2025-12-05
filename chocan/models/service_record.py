# service_record.py
import json
import os
from datetime import datetime

# Path to transactions.json inside /data
TRANSACTION_FILE = os.path.join(
    os.path.dirname(__file__), "..", "data", "transactions.json"
)


class ServiceRecord:
    """
    Represents a single service performed by a provider for a member.
    Stored in transactions.json for reporting and billing.
    """

    def __init__(self, provider_num, member_num, service_code, service_date, comments=""):
        self.timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        self.service_date = service_date
        self.provider_num = provider_num
        self.member_num = member_num
        self.service_code = service_code
        self.comments = comments

    def to_dict(self):
        """Convert the service record into a dictionary for JSON storage."""
        return {
            "timestamp": self.timestamp,
            "service_date": self.service_date,
            "provider_num": self.provider_num,
            "member_num": self.member_num,
            "service_code": self.service_code,
            "comments": self.comments,
        }


def save_service_record(record: ServiceRecord):
    """
    Saves a service record to transactions.json.
    Creates the file if it does not exist.
    """

    record_data = record.to_dict()

    # Ensure directory exists
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    os.makedirs(abs_path, exist_ok=True)

    # Load existing records
    if os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []  # corrupted file = start fresh
    else:
        data = []

    # Add new entry
    data.append(record_data)

    # Save back to JSON
    with open(TRANSACTION_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return True