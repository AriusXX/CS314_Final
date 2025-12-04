from models.member import MemberDatabase
from models.provider import Provider
from models.service_directory import ServiceDirectory
from models.service_record import ServiceRecord

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
    member_db = MemberDatabase()
    while True:
        choice = main_menu()

        if choice == "1":
            print("\n--- Validate Member ---")
            member_number = input("Enter member number: ").strip()
            status = member_db.validate_member(member_number)
            print(status + "\n")

        elif choice == "2":
            print("\n--- Bill ChocAn for Service ---")
            # TODO: implement service billing
            print("Billing feature not implemented yet.\n")

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
