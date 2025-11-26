class ServiceDirectory:
    def __init__(self):
        # TEMPORARY hardcoded services — later replace with JSON file
        self.services = {
            "598470": ("Dietitian Session", 45.00),
            "883948": ("Aerobics Exercise Session", 25.00)
        }

    def lookup(self, code):
        return self.services.get(code, None)

    def print_directory(self):
        print("\n=== Provider Directory ===")
        for code, (name, fee) in sorted(self.services.items(), key=lambda x: x[1][0]):
            print(f"{name:25}  Code: {code}  Fee: ${fee:.2f}")
        print()
