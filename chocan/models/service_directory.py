# models/service_directory.py

import json
import os

class ServiceDirectory:

    def __init__(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "data", "services.json")
        file_path = os.path.abspath(file_path)

        with open(file_path, "r") as f:
            self.services = json.load(f)

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
        if code not in self.services:
            return None

        name = self.services[code]["name"]
        fee = float(self.services[code]["fee"])   # <-- FIX HERE
        return name, fee

    # -----------------------------------------------------
    # Print full directory (for debugging)
    # -----------------------------------------------------
    def print_directory(self):
        print("\n=== Provider Directory ===")
        for code, info in self.services.items():
            print(f"{info['name']:30} Code: {code}   Fee: ${info['fee']:.2f}")
        print()
