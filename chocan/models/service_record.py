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
