# models/provider.py
import json
import os
from .member import MemberDatabase
from .service_directory import ServiceDirectory
from .service_record import ServiceRecord

class Provider:
    def __init__(self, name, number, address, city, state, zip_code):
        self.name = name
        self.number = str(number)
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip_code

    # Validate provider number format (should be 9 digits)
    def is_valid_number(self):
        return len(self.number) == 9 and self.number.isdigit()

    # --- Provider database helper (static-ish) ---
    @staticmethod
    def load_providers(data_file=None):
        if data_file:
            data_path = data_file
        else:
            data_path = os.path.join(
                os.path.dirname(__file__), "..", "data", "providers.json"
            )

        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Missing providers.json at: {data_path}")

        with open(data_path, "r") as f:
            return json.load(f)

    @classmethod
    def from_number(cls, provider_number, data_file=None):
        """Create a Provider object from providers.json based on provider_number."""
        providers = cls.load_providers(data_file)
        provider_number = str(provider_number)
        record = providers.get(provider_number)
        if record is None:
            return None

        return cls(
            name=record["name"],
            number=provider_number,
            address=record["address"],
            city=record["city"],
            state=record["state"],
            zip_code=record["zip"],
        )

    # Validate member eligibility using MemberDatabase
    def validate_member(self, member_number):
        db = MemberDatabase()
        return db.validate_member(member_number)

    # Calculate service fee
    def calculate_fee(self, service_code):
        directory = ServiceDirectory()
        service_info = directory.lookup(service_code)
        return service_info  # dict: {"name": ..., "fee": ...} or None

    # Record a service — full ChocAn workflow
    def record_service(self, member_number, service_code, service_date, comments=""):
        # 1. Validate member
        status = self.validate_member(member_number)
        if status != "Validated":
            return {"success": False, "message": f"Service denied: {status}"}

        # 2. Validate service code
        service_info = self.calculate_fee(service_code)
        if service_info is None:
            return {"success": False, "message": "Invalid service code."}

        # 3. Create a ServiceRecord object
        record = ServiceRecord(
            provider_num=self.number,
            member_num=member_number,
            service_date=service_date,
            service_code=service_code,
            comments=comments,
        )

        # 4. Save to transactions.json
        self.save_transaction(record)

        return {
            "success": True,
            "message": "Service recorded successfully.",
            "fee": service_info["fee"],
            "service_name": service_info["name"],
        }

    def save_transaction(self, record: ServiceRecord):
        filepath = os.path.join(
            os.path.dirname(__file__), "..", "data", "transactions.json"
        )

        try:
            with open(filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(record.to_dict())

        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)

    def get_weekly_services(self):
        """Later used for weekly provider reports."""
        filepath = os.path.join(
            os.path.dirname(__file__), "..", "data", "transactions.json"
        )

        try:
            with open(filepath, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []

        results = []
        for entry in data:
            if entry["provider_num"] == self.number:
                results.append(entry)

        return results
