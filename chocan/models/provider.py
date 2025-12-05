# models/provider.py

import json
import os
from .member import MemberDatabase
from .service_directory import ServiceDirectory
from .service_record import ServiceRecord


# Provider Data Structure
class Provider:
    def __init__(self, name, number, address, city, state, zip_code):
        self.name = name
        self.number = str(number)
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip_code

    def is_valid_number(self):
        """Return True if provider number is a valid 9-digit ID."""
        return len(self.number) == 9 and self.number.isdigit()

# Provider Database Loader
class ProviderDatabase:
    def __init__(self):
        base = os.path.dirname(os.path.dirname(__file__))  # go up /models → project root
        self.file_path = os.path.join(base, "data", "providers.json")

        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                self.providers = json.load(f)
        else:
            self.providers = {}

    def get_provider(self, provider_number):
        """Return a Provider object or None."""
        provider_number = str(provider_number)

        record = self.providers.get(provider_number)
        if not record:
            return None

        return Provider(
            name=record["name"],
            number=provider_number,
            address=record["address"],
            city=record["city"],
            state=record["state"],
            zip_code=record["zip"]
        )

# Provider Workflow Methods
class ProviderActions:
    """Handles real provider actions such as billing and validation."""

    def __init__(self, provider_obj: Provider):
        self.provider = provider_obj
        self.member_db = MemberDatabase()
        self.directory = ServiceDirectory()

    def validate_member(self, member_number):
        """Return 'Validated' or failure reason."""
        return self.member_db.validate_member(member_number)

    def calculate_fee(self, service_code):
        """Return dict with service_name and fee."""
        lookup = self.directory.lookup(service_code)

        if lookup is None:
            return None

        # lookup returns tuple (name, fee)
        name, fee = lookup
        return {"name": name, "fee": float(fee)}

    def record_service(self, member_number, service_code, service_date, comments=""):
        """Full billing workflow: validate → calculate → save → return summary."""

        # 1. Validate member
        status = self.validate_member(member_number)
        if status != "Validated":
            return {"success": False, "message": status}

        # 2. Validate service code
        service_info = self.calculate_fee(service_code)
        if service_info is None:
            return {"success": False, "message": "Invalid service code."}

        # 3. Build a service record object
        record = ServiceRecord(
            provider_num=self.provider.number,
            member_num=member_number,
            service_code=service_code,
            service_date=service_date,
            comments=comments
        )

        # 4. Save transaction
        self._save_transaction(record)

        return {
            "success": True,
            "message": "Service recorded successfully.",
            "service_name": service_info["name"],
            "fee": service_info["fee"]
        }

    def _save_transaction(self, record: ServiceRecord):
        """Append a service record into transactions.json."""

        base = os.path.dirname(os.path.dirname(__file__))  # project root
        filepath = os.path.join(base, "data", "transactions.json")

        try:
            with open(filepath, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(record.to_dict())

        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)