# models/member.py
import json
import os

class Member:
    def __init__(self, name, number, address, city, state, zip_code, status="active"):
        self.name = name
        self.number = str(number)
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.status = status  # "active" or "suspended"

    def is_valid(self):
        return self.status == "active"


class MemberDatabase:
    """Loads and manages member records.
    Provides member lookup and validation functionalities.
    """

    def __init__(self, data_file=None):
        if data_file:
            self.DATA_FILE = data_file
        else:
            # ../data/members.json relative to this file
            self.DATA_FILE = os.path.join(
                os.path.dirname(__file__), "..", "data", "members.json"
            )

        self.members = self._load_members()

    def _load_members(self):
        """Loads all members from the JSON file as a dict."""
        if not os.path.exists(self.DATA_FILE):
            raise FileNotFoundError(f"Missing members.json file at: {self.DATA_FILE}")

        with open(self.DATA_FILE, "r") as f:
            return json.load(f)

    def _save_members(self):
        """Writes the current members dict back to JSON (for add/update/delete)."""
        with open(self.DATA_FILE, "w") as f:
            json.dump(self.members, f, indent=4)

    def get_member(self, member_id):
        """Returns a Member object if the ID exists, otherwise None."""
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
            status=record["status"],
        )

    def validate_member(self, member_id):
        """Returns status string: 'Invalid Number', 'Suspended', or 'Validated'."""
        m = self.get_member(member_id)

        if m is None:
            return "Invalid Number"
        if not m.is_valid():
            return "Member suspended"
        return "Validated"

    # Optional: manager functionality

    def add_member(self, member_id, name, address, city, state, zip_code, status="active"):
        member_id = str(member_id)
        self.members[member_id] = {
            "name": name,
            "address": address,
            "city": city,
            "state": state,
            "zip": zip_code,
            "status": status,
        }
        self._save_members()

    def delete_member(self, member_id):
        member_id = str(member_id)
        if member_id in self.members:
            del self.members[member_id]
            self._save_members()

    def update_member_status(self, member_id, status):
        member_id = str(member_id)
        if member_id in self.members:
            self.members[member_id]["status"] = status
            self._save_members()
