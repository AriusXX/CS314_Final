# models/service_record.py

from datetime import datetime
import json
import os


class ServiceRecord:
    """
    Represents a single service entry created by a provider.
    Stored later in transactions.json for reporting.
    """

    def __init__(self, provider_num, member_num, service_code, service_date, comments=""):
        self.timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        self.service_date = service_date
        self.provider_num = provider_num
        self.member_num = member_num
        self.service_code = service_code
        self.comments = comments

    # --------------------------------------------------
    # Convert the service record to a dictionary
    # --------------------------------------------------
    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "service_date": self.service_date,
            "provider_num": self.provider_num,
            "member_num": self.member_num,
            "service_code": self.service_code,
            "comments": self.comments
        }

    # --------------------------------------------------
    # Save this record to transactions.json
    # --------------------------------------------------
    def save(self, file_path="chocan/data/transactions.json"):
        # Create file if missing
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump([], f)

        # Load existing transactions
        with open(file_path, "r") as f:
            data = json.load(f)

        # Add new record
        data.append(self.to_dict())

        # Write back to file
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        return True
