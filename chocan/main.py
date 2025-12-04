from models.member import MemberDatabase
from models.provider import ProviderDatabase, Provider
from models.service_directory import ServiceDirectory
from models.service_record import ServiceRecord
from models import reports

def main_menu():
    print("\n=== ChocAn Data Processing System ===")
    print("1. Validate Member")
    print("2. Bill ChocAn for Service")
    print("3. Provider Directory")
    print("4. Manager Options")
    print("5. Exit")

    return input("Select an option: ").strip()


def manager_menu():
    print("\n=== Manager / Reporting Options ===")
    print("1. Generate Member Reports")
    print("2. Generate Provider Reports")
    print("3. Generate Summary Report")
    print("4. Back to Main Menu")
    return input("Select an option: ").strip()


def main():
    member_db = MemberDatabase()
    provider_db = ProviderDatabase()
    directory = ServiceDirectory()

    while True:
        choice = main_menu()

        #
        # VALIDATE MEMBER
        if choice == "1":
            print("\n--- Validate Member ---")
            member_number = input("Enter member number: ").strip()
            status = member_db.validate_member(member_number)
            print("Status:", status, "\n")

        # BILL CHOCAN / RECORD SERVICE
        elif choice == "2":
            print("\n--- Bill ChocAn for Service ---")

            provider_number = input("Enter provider number: ").strip()
            provider = provider_db.get_provider(provider_number)

            if provider is None:
                print("Invalid provider number.\n")
                continue

            member_number = input("Enter member number: ").strip()
            status = member_db.validate_member(member_number)

            if status != "Validated":
                print(f"Cannot continue — Member is {status}\n")
                continue

            service_code = input("Enter 6-digit service code: ").strip()
            service_info = directory.lookup(service_code)

            if service_info is None:
                print("Invalid service code.\n")
                continue

            service_date = input("Enter date of service (MM-DD-YYYY): ").strip()
            comments = input("Optional comments: ").strip()

            # Create and save service record
            record = ServiceRecord(
                provider_num=provider_number,
                member_num=member_number,
                service_code=service_code,
                service_date=service_date,
                comments=comments
            )
            record.save()

            print("\nService recorded successfully!")
            print(f"Service: {service_info['name']}")
            print(f"Fee: ${service_info['fee']:.2f}\n")

        # 
        # PROVIDER DIRECTORY
        elif choice == "3":
            print("\n--- Provider Directory ---")
            directory.print_directory()

       
        # MANAGER OPTIONS
        
        elif choice == "4":
            while True:
                m_choice = manager_menu()

                if m_choice == "1":
                    print("\nGenerating Member Reports...")
                    paths = reports.generate_member_reports()
                    print(f"Generated {len(paths)} member reports.\n")

                elif m_choice == "2":
                    print("\nGenerating Provider Reports...")
                    paths = reports.generate_provider_reports()
                    print(f"Generated {len(paths)} provider reports.\n")

                elif m_choice == "3":
                    print("\nGenerating Summary Report...")
                    path = reports.generate_summary_report()
                    print(f"Summary report saved at:\n{path}\n")

                elif m_choice == "4":
                    break
                else:
                    print("Invalid option. Try again.\n")

        # -----------------------------
        # EXIT
        # -----------------------------
        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.\n")


if __name__ == "__main__":
    main()