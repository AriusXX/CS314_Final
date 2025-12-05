import pytest
from unittest.mock import patch, MagicMock, mock_open
from chocan.models.member import MemberDatabase, Member
from chocan.models.provider import ProviderActions, Provider
from chocan.models.service_directory import ServiceDirectory
from chocan.models.service_record import ServiceRecord
from chocan.models.reports import (
    generate_member_reports,
    generate_provider_reports,
    generate_summary_report,
)
import json
from datetime import datetime

# ---------------------------
# I. UNIT TESTS
# ---------------------------

class TestMemberDatabase:
    def setup_method(self):
        # Create a mocked MemberDatabase
        self.db = MemberDatabase()
        self.db.members = {
            "111111111": {"name": "Alice Example", "status": "active"},
            "222333444": {"name": "Bob Test", "status": "suspended"},
        }

    def test_validate_member_active(self):
        assert self.db.validate_member("111111111") == "Validated"

    def test_validate_member_invalid(self):
        assert self.db.validate_member("000000000") == "Invalid Number"

    def test_validate_member_suspended(self):
        assert self.db.validate_member("222333444") == "Member suspended"

    @patch("builtins.open", new_callable=mock_open)
    def test_add_and_delete_member(self, mock_file):
        new_member = Member("333333333", "Charlie", "active")
        self.db.add_member(new_member)
        assert "333333333" in self.db.members
        self.db.delete_member("333333333")
        assert "333333333" not in self.db.members


class TestProviderActions:
    def setup_method(self):
        self.directory = ServiceDirectory()
        self.provider = ProviderActions()

    def test_calculate_fee_valid(self):
        result = self.provider.calculate_fee("598470")
        assert result == {"name": "Dietitian Session", "fee": 45.00}

    def test_calculate_fee_invalid(self):
        result = self.provider.calculate_fee("000000")
        assert result is None

    @patch("chocan.models.service_record.json.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_record_service_success(self, mock_file, mock_json):
        member_db = MemberDatabase()
        member_db.members = {"111111111": {"name": "Alice", "status": "active"}}
        # Successful service
        response = self.provider.record_service(
            member_db, "111111111", "598470", "12-01-2025", "Test comments"
        )
        assert response["success"] is True
        # Check that the transaction was saved
        mock_json.assert_called()

    def test_record_service_invalid_member(self):
        member_db = MemberDatabase()
        member_db.members = {}
        response = self.provider.record_service(
            member_db, "000000000", "598470", "12-01-2025", ""
        )
        assert response == "Invalid Number"

    def test_record_service_suspended_member(self):
        member_db = MemberDatabase()
        member_db.members = {"222333444": {"name": "Bob", "status": "suspended"}}
        response = self.provider.record_service(
            member_db, "222333444", "598470", "12-01-2025", ""
        )
        assert response == "Member suspended"

    def test_record_service_invalid_service_code(self):
        member_db = MemberDatabase()
        member_db.members = {"111111111": {"name": "Alice", "status": "active"}}
        response = self.provider.record_service(
            member_db, "111111111", "000000", "12-01-2025", ""
        )
        assert response == "Invalid service code."


class TestServiceRecord:
    def test_to_dict_contains_all_fields(self):
        record = ServiceRecord("111", "222", "598470", "12-01-2025", "Comment")
        record_dict = record.to_dict()
        expected_keys = ["provider_num", "member_num", "service_code", "service_date", "comments", "timestamp"]
        for key in expected_keys:
            assert key in record_dict


# ---------------------------
# II. INTEGRATION TESTS: REPORTS
# ---------------------------

class TestReports:
    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    @patch("json.load", return_value=[
        {"provider_num": "111", "member_num": "222", "service_code": "598470", "service_date": "12-01-2025", "comments": ""}
    ])
    def test_generate_member_reports(self, mock_json, mock_file):
        generate_member_reports("mock_transactions.json", output_dir="/tmp")
        mock_file.assert_called()

    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    @patch("json.load", return_value=[
        {"provider_num": "111", "member_num": "222", "service_code": "598470", "service_date": "12-01-2025", "comments": ""}
    ])
    def test_generate_provider_reports(self, mock_json, mock_file):
        generate_provider_reports("mock_transactions.json", output_dir="/tmp")
        mock_file.assert_called()

    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    @patch("json.load", return_value=[
        {"provider_num": "111", "member_num": "222", "service_code": "598470", "service_date": "12-01-2025", "comments": ""}
    ])
    def test_generate_summary_report(self, mock_json, mock_file):
        result = generate_summary_report("mock_transactions.json")
        assert "Total Providers Paid" in result
        assert "Total Services Provided" in result
        assert "Total Overall Fee" in result


# ---------------------------
# III. FUNCTIONAL / FLOW TESTS
# ---------------------------

from chocan.main import main_menu, main

def test_main_menu_input_output(capsys):
    # simulate selecting '5' for exit
    with patch("builtins.input", side_effect=["5"]):
        choice = main_menu()
        captured = capsys.readouterr()
        assert "=== ChocAn Data Processing System ===" in captured.out
        assert choice == "5"

def test_main_option_1_placeholder_output(capsys):
    # simulate selecting '1', entering member number, then exit
    with patch("builtins.input", side_effect=["1", "111111111", "5"]):
        main()
        captured = capsys.readouterr()
        # Placeholder may not be implemented yet; if implemented, verify output
        # Adjust assertion depending on your current main.py behavior
        assert "Validate Member" in captured.out or "Validation feature not implemented" in captured.out

def test_main_option_3_provider_directory_flow(capsys):
    with patch("builtins.input", side_effect=["3", "5"]):
        main()
        captured = capsys.readouterr()
        assert "Provider Directory" in captured.out

def test_main_option_4_manager_reporting_menu(capsys):
    with patch("builtins.input", side_effect=["4", "4", "5"]):
        main()
        captured = capsys.readouterr()
        assert "Manager / Reporting Options" in captured.out
        # Depending on implementation, check for report generation placeholders
        assert "Back to Main Menu" in captured.out
