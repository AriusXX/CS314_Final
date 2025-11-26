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
