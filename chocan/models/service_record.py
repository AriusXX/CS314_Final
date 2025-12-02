from datetime import datetime

class ServiceRecord:
    def __init__(self, provider_num, member_num, service_code, service_date, comments=""):
        self.timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        self.service_date = service_date
        self.provider_num = provider_num
        self.member_num = member_num
        self.service_code = service_code
        self.comments = comments
class Member(object):
    """
    Represents a ChocAn member and holds identifying information 
    and eligibility status.
    """

    def __init__(self, number, name, street, city, state, zip_code, status="Validated"):
        # Member Identification and Status
        # The member number must be a nine-digit number [5].
        self._member_number = number
        # Status indicates eligibility (e.g., "Validated" or "Suspended") [6, 7].
        self._status = status
        
        # Personal and Contact Information
        # Name is limited to 25 characters [2].
        self._name = name[:25]
        # Street address is limited to 25 characters [2].
        self._street_address = street[:25]
        # City is limited to 14 characters [2].
        self._city = city[:14]
        # State is limited to 2 letters [2].
        self._state = state[:2]
        # Zip code is limited to 5 digits [2].
        self._zip_code = zip_code[:5]
        
        # Note: These instance variables start with an underscore to indicate 
        # they are private to the class (information hiding) [8-10].

    # Example method (Getter) needed for system interaction (e.g., Validation, Billing)
    def get_member_number(self):
        """Returns the member's nine-digit number."""
        return self._member_number

    # Example method for eligibility checks (Core Use Case)
    def get_status(self):
        """Returns the current eligibility status (e.g., 'Validated' or 'Suspended')."""
        return self._status

    # Example method for updating status (Manager Options or Acme Accounting interface) [11]
    def set_status(self, new_status):
        """Updates the member's eligibility status."""
        self._status = new_status