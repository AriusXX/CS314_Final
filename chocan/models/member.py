import json
import os
class Member:
    def __init__(self, name, number, address, city, state, zip_code, status="active"):
        self.name = name
        self.number = number
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.status = status  # active or suspended

    def is_valid(self):
        return self.status == "active"

class MemberDatabase:
# loads and manages member records
# Provides member lookup andProvides member lookup and validation functionalities
    def __init__(self, data_file=None):
        # Path to JSON file
        if data_file:
            self.DATA_FILE = data_file
        else: 
            self.DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "members.json")

            self.members = self._load_members()

    def _load_members(self):
        # Loads all members from the JSON file as a dictionary."""
        if not os.path.exists(self.DATA_FILE):
            raise FileNotFoundError(f"Missing members.json file at: {self.DATA_FILE}")

        with open(self.DATA_FILE, "r") as f:
            return json.load(f)

    def get_member(self, member_id):
        
       # Returns a Member object if the ID exists, otherwise None.
        
        member_id = str(member_id)
        record = self.members.get(member_id)

        if record is None:
            return None

        return Member(
            name=record["name"],
            number=member_id,
            address=record["address"],
            city=record["city"],
            state=record["state"],
            zip_code=record["zip"],
            status=record["status"]
        )

    def validate_member(self, member_id):

        m = self.get_member(member_id)

        if m is None:
            return "Invalid Number"
        if not m.is_valid():
            return "Suspended"
        return "Validated"
