# models/service_directory.py

import json

class ServiceDirectory:

    def __init__(self):
        self.services = self.load_services()

    # -----------------------------------------------------
    # Load services from JSON file
    # services.json format:
    # {
    #   "598470": {"name": "Dietitian Session", "fee": 45.00},
    #   "883948": {"name": "Aerobics Exercise Session", "fee": 25.00}
    # }
    # -----------------------------------------------------
    def load_services(self):
        try:
            with open("chocan/data/services.json", "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print("ERROR: services.json not found.")
            return {}
        except json.JSONDecodeError:
            print("ERROR: services.json is improperly formatted.")
            return {}

    # -----------------------------------------------------
    # Lookup a service by code
    # Returns None if not found
    # -----------------------------------------------------
    def lookup(self, code):
        code = str(code)
        return self.services.get(code, None)

    # -----------------------------------------------------
    # Print full directory (for debugging)
    # -----------------------------------------------------
    def print_directory(self):
        print("\n=== Provider Directory ===")
        for code, info in self.services.items():
            print(f"{info['name']:30} Code: {code}   Fee: ${info['fee']:.2f}")
        print()
