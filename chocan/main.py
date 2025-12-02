from models.member import Member
from models.provider import Provider
from models.service_directory import ServiceDirectory
from models.service_record import ServiceRecord

class ChocAnData:
    """Mock Data Manager for Validation (as implemented previously)"""
    def __init__(self):
        self.members = {"111222333": {"name": "Valid Member", "status": "Validated"}}
        self.providers = {"999000111": {"name": "Dr. Example", "type": "Provider"}}

    def validate_member_eligibility(self, member_number):
        member = self.members.get(member_number)
        if not member:
            return "Invalid Number", None
        return member["status"], member["name"]

    def is_valid_provider(self, provider_number):
        return provider_number in self.providers

def write_service_record_to_disk(record):
    print("\n[SYSTEM] Writing Service Record to Disk...")
    print(f"Fee to be paid: **$45.00** (Simulated)")
    print("[SYSTEM] Service Record Successfully Written.\n")
# ----------------------------------------------------


def handle_service_billing(directory, data_manager):
    """Handles all steps required to record a service billed to ChocAn."""
    print("\n--- Bill ChocAn for Service ---")
    
    # 1. Collect Required Data Inputs
    service_date = input("Enter date service was provided (MM-DD-YYYY): ")
    provider_num = input("Enter provider number (9 digits): ")
    member_num = input("Enter member number (9 digits): ")
    service_code = input("Enter 6-digit service code: ")
    comments = input("Enter comments (optional, max 100 characters): ")
    comments = comments[:100]

    # 2. Validation Checks
    
    # Member Eligibility
    status, member_name = data_manager.validate_member_eligibility(member_num)
    if status != "Validated":
        print(f"\nError: Member is {status}. Service cannot be billed.")
        return

    # Provider Existence
    if not data_manager.is_valid_provider(provider_num):
        print("\nError: Provider number is invalid. Billing stopped.")
        return

    # Service Code validity and retrieval
    service_info = directory.lookup(service_code)
    
    if service_info is None:
        print("\nError: Invalid Service Code. Billing stopped.")
        return
    
    service_name, fee = service_info
    
    # 3. Verification and Confirmation
    print(f"\nService Validated: {service_name}")
    print(f"Fee to be paid: **${fee:.2f}**")
    
    confirmation = input("Confirm billing? (y/n): ").lower()
    if confirmation != 'y':
        print("Billing cancelled.\n")
        return

    # 4. Record the Transaction
    new_record = ServiceRecord(
        provider_num=provider_num,
        member_num=member_num,
        service_code=service_code,
        service_date=service_date,
        comments=comments
    )
    
    # Write the record to disk, simulating output to a file (Section 7.3 discusses file I/O)
    write_service_record_to_disk(new_record)
    
def main_menu():
    print("\n=== ChocAn Data Processing System ===")
    print("1. Validate Member")
    print("2. Bill ChocAn for Service")
    print("3. Provider Directory")
    print("4. Manager Options")
    print("5. Exit")

    return input("Select an option: ").strip()

def main():
    directory = ServiceDirectory()
    chocan_data = ChocAnData()
    member = Member()
    while True:
        choice = main_menu()

        if choice == "1":
            print("\n--- Validate Member ---")
            member_number = input("Enter member number: ")
            # TODO: call member validation function
            print("Validation feature not implemented yet.\n")

        elif choice == "2":
            print("\n--- Bill ChocAn for Service ---")
            # TODO: implement service billing
            handle_service_billing(directory, chocan_data)
            #print("Billing feature not implemented yet.\n")

        elif choice == "3":
            print("\n--- Provider Directory ---")
            directory.print_directory()

        elif choice == "4":
            print("\n--- Manager Options ---")
            print("Manager features not implemented yet.\n")

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.\n")

if __name__ == "__main__":
    main()
