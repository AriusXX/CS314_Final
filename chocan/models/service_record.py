# models/service_record.py
from datetime import datetime

class ServiceRecord:
    """
    Represents a single service entry created by a provider.
    Stored later in transactions.json for reporting.
    """

    def __init__(self, provider_num, member_num, service_code, service_date, comments=""):
        self.timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        self.service_date = service_date              # MM-DD-YYYY
        self.provider_num = str(provider_num)
        self.member_num = str(member_num)
        self.service_code = str(service_code)
        self.comments = comments

    def to_dict(self):
        """Convert to a plain dict for JSON storage."""
        return {
            "timestamp": self.timestamp,
            "service_date": self.service_date,
            "provider_num": self.provider_num,
            "member_num": self.member_num,
            "service_code": self.service_code,
            "comments": self.comments,
        }
