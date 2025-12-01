from datetime import datetime

class ServiceRecord:
    def __init__(self, provider_num, member_num, service_code, service_date, comments=""):
        self.timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        self.service_date = service_date
        self.provider_num = provider_num
        self.member_num = member_num
        self.service_code = service_code
        self.comments = comments

