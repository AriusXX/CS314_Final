import json
from datetime import datetime
from .member import Member
from .service_directory import ServiceDirectory
from .service_record import ServiceRecord
class Provider:
    def __init__(self, name, number, address, city, state, zip_code):
        self.name = name
        self.number = number
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip_code

    # Validate provider number format (should be 9 digits)
    def is_valid_number(self):
        return len(str(self.number)) == 9 and str(self.number).isdigit()

    # Load all members from members.json
    def load_members(self):
        with open("chocan/data/members.json", "r") as file:
            data = json.load(file)
        return data

    # Validate member eligibility (calls Member module)
    def validate_member(self, member_number):
        members = self.load_members()

        if str(member_number) not in members:
            return "Invalid Number"

        member_data = members[str(member_number)]
        member = Member(
            member_data["name"],
            member_number,
            member_data["address"],
            member_data["city"],
            member_data["state"],
            member_data["zip_code"],
            member_data["status"]
        )

        return "Validated" if member.is_valid() else "Suspended"

    # Calculate service fee (calls ServiceDirectory)
    def calculate_fee(self, service_code):
        directory = ServiceDirectory()
        service_info = directory.lookup(service_code)
        return service_info  # returns dict: {"name": ..., "fee": ...}

    # Record a service — FULL ChocAn workflow
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
            comments=comments
        )

        # 4. Save it to transactions.json
        self.save_transaction(record)

        return {
            "success": True,
            "message": "Service recorded successfully.",
            "fee": service_info["fee"],
            "service_name": service_info["name"]
        }

    # Save ServiceRecord to transactions.json
    def save_transaction(self, record: ServiceRecord):
        filepath = "chocan/data/transactions.json"

        try:
            with open(filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(record.to_dict())

        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)

    # Retrieve all transactions for this provider
    # Used by Manager module for weekly reports
    def get_weekly_services(self):
        filepath = "chocan/data/transactions.json"

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