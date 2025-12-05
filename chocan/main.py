from models.member import MemberDatabase
from models.provider import ProviderDatabase, Provider
from models.service_directory import ServiceDirectory
from models.service_record import ServiceRecord
from models import reports
from models.reports import (
    generate_member_reports,
    generate_provider_reports,
    generate_summary_report
)
from models.provider import Provider, ProviderDatabase
from models.provider import ProviderActions




# ----------------------------
# MAIN MENUS
# ----------------------------

def main_menu():
    print("\n=== ChocAn Data Processing System ===")
    print("1. Validate Member")
    print("2. Provider Terminal")
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


# ----------------------------
# PROVIDER LOGIN
# ----------------------------

def provider_login():
    print("\n=== ChocAn Provider Login ===")
    db = ProviderDatabase()

    while True:
        provider_num = input("Enter provider number (9 digits): ").strip()

        if len(provider_num) != 9 or not provider_num.isdigit():
            print("Invalid format. Must be 9 digits.\n")
            continue

        provider = db.get_provider(provider_num)
        if provider is None:
            print("Provider not found. Try again.\n")
            continue

        print(f"\nWelcome, {provider.name}!")
        return provider

# ----------------------------
# PROVIDER TERMINAL (Nested Menu)
# ----------------------------

def provider_terminal():
    provider = provider_login()

    while True:
        print("---- Provider Menu ----")
        print("1. Validate Member")
        print("2. Bill ChocAn for Service")
        print("3. Provider Directory")
        print("4. Logout")

        choice = input("Select an option: ").strip()

        if choice == "1":
            member_num = input("Enter member number: ").strip()
            status = provider.validate_member(member_num)
            print(f"Member Status: {status}\n")

        elif choice == "2":
            bill_service(provider)

        elif choice == "3":
            directory = ServiceDirectory()
            directory.print_directory()
            print()

        elif choice == "4":
            print("Logging out...\n")
            break

        else:
            print("Invalid option. Try again.\n")


# ----------------------------
# BILLING A SERVICE (Provider Terminal)
# ----------------------------

def bill_service(provider):
    print("\n--- Bill ChocAn for Service ---")

    actions = ProviderActions(provider)  # <-- IMPORTANT FIX

    member_number = input("Enter member number: ").strip()
    status = actions.validate_member(member_number)

    if status != "Validated":
        print(f"Cannot continue — Member is {status}\n")
        return

    service_date = input("Enter date of service (MM-DD-YYYY): ").strip()
    service_code = input("Enter 6-digit service code: ").strip()
    comments = input("Optional comments: ").strip()

    result = actions.record_service(
        member_number=member_number,
        service_code=service_code,
        service_date=service_date,
        comments=comments
    )

    if result["success"]:
        print("Service recorded successfully!")
        print(f"Service: {result['service_name']}")
        print(f"Fee: ${result['fee']:.2f}\n")
    else:
        print("Error: " + result["message"] + "\n")


# ----------------------------
# MAIN PROGRAM LOOP
# ----------------------------

def main():
    member_db = MemberDatabase()
    directory = ServiceDirectory()

    while True:
        choice = main_menu()

        # Validate a Member
        if choice == "1":
            print("\n--- Validate Member ---")
            member_number = input("Enter member number: ").strip()
            status = member_db.validate_member(member_number)
            print("Status:", status, "\n")

        # Provider Terminal
        elif choice == "2":
            provider_terminal()

        # Provider Directory
        elif choice == "3":
            print("\n--- Provider Directory ---")
            directory.print_directory()

        # Manager Options
        elif choice == "4":
            while True:
                m_choice = manager_menu()

                if m_choice == "1":
                    print("\nGenerating Member Reports...")
                    paths = generate_member_reports()
                    print(f"Generated {len(paths)} member reports.\n")

                elif m_choice == "2":
                    print("\nGenerating Provider Reports...")
                    paths = generate_provider_reports()
                    print(f"Generated {len(paths)} provider reports.\n")

                elif m_choice == "3":
                    print("\nGenerating Summary Report...")
                    path = generate_summary_report()
                    print(f"Summary report saved at:\n{path}\n")

                elif m_choice == "4":
                    break
                else:
                    print("Invalid option. Try again.\n")

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.\n")


if __name__ == "__main__":
    main()