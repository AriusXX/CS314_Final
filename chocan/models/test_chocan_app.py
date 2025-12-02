import pytest
from unittest.mock import patch, MagicMock
from models.provider import Provider
from models.service_directory import ServiceDirectory
from models.service_record import ServiceRecord
from models.main import main_menu, main
from datetime import datetime

class TestDataClasses:
    """Tests for ServiceDirectory and ServiceRecord."""

    def test_service_directory_lookup_valid(self):
        """Verify lookup returns correct service and fee."""
        directory = ServiceDirectory()
        # Test hardcoded service 598470 [3]
        assert directory.lookup("598470") == ("Dietitian Session", 45.00)

    def test_service_directory_lookup_invalid(self):
        """Verify lookup returns None for invalid code."""
        directory = ServiceDirectory()
        assert directory.lookup("000000") is None

    def test_service_directory_print_directory(self, capsys):
        """Verify the directory prints correctly and is formatted."""
        directory = ServiceDirectory()
        directory.print_directory()
        captured = capsys.readouterr()
        
        # Check for expected services and formatting [2]
        assert "=== Provider Directory ===" in captured.out
        # Check for one of the hardcoded services [3]
        assert "Dietitian Session        Code: 598470 Fee: $45.00" in captured.out
        # Check sorting order based on name (Aerobics comes before Dietitian)
        assert captured.out.index("Aerobics Exercise Session") < captured.out.index("Dietitian Session")

    @patch('test_chocan_app.datetime')
    def test_service_record_initialization(self, mock_datetime):
        """Verify ServiceRecord stores data and generates a timestamp."""
        # Mock the current time to ensure deterministic timestamp format checking [2]
        mock_now = MagicMock()
        mock_now.strftime.return_value = "01-01-2023 12:00:00"
        mock_datetime.now.return_value = mock_now
        mock_datetime.now().strftime.return_value = "01-01-2023 12:00:00"
        
        # Initialize a record with test data [2]
        record = ServiceRecord(
            provider_num="111", 
            member_num="222", 
            service_code="333", 
            service_date="12-25-2023", 
            comments="Test comment"
        )
        
        # Assertions check the integrity of the stored data [2]
        assert record.provider_num == "111"
        assert record.service_date == "12-25-2023"
        assert record.comments == "Test comment"
        assert record.timestamp == "01-01-2023 12:00:00"

def test_main_menu_output(capsys):
    """Verify that main_menu prints the required options correctly."""
    
    # Mock user input to avoid halting the test
    with patch('builtins.input', return_value='1'):
        main_menu()
    
    captured = capsys.readouterr()
    expected_output = [
        "=== ChocAn Data Processing System ===",
        "1. Validate Member",
        "2. Bill ChocAn for Service",
        "3. Provider Directory",
        "4. Manager Options",
        "5. Exit"
    ]
    
    # Check that all elements of the menu are present in the captured output [1]
    for line in expected_output:
        assert line in captured.out

def test_main_menu_input_handling():
    """Verify main_menu strips whitespace from input [1]."""
    with patch('builtins.input', return_value=' 1 '):
        choice = main_menu()
        assert choice == '1'

# --- INTEGRATION/FLOW TESTS (main function) ---

# We use the capsys fixture to verify output shown on the screen (simulating the terminal display) [6].

def test_main_option_3_provider_directory(capsys):
    """Test flow for option 3 (Provider Directory) and then exit."""
    
    # Simulate entering '3' followed by '5' (Exit)
    input_sequence = iter(['3', '5'])
    with patch('builtins.input', lambda prompt: next(input_sequence)):
        main()
    
    captured = capsys.readouterr()
    
    # Assert that the directory printing logic was executed [4]
    assert "--- Provider Directory ---" in captured.out
    
    # Assert that the directory content was printed (check against the content test above)
    assert "Dietitian Session" in captured.out
    
    # Assert that the exit mechanism worked [3]
    assert "Exiting..." in captured.out

def test_main_option_1_placeholder(capsys):
    """Test flow for option 1 (Validate Member) placeholder and then exit."""
    
    # Simulate entering '1', then member number '123456789', then '5' (Exit)
    input_sequence = iter(['1', '123456789', '5'])
    with patch('builtins.input', lambda prompt: next(input_sequence)):
        main()
        
    captured = capsys.readouterr()
    
    # Assert that the placeholder code path was reached [4]
    assert "--- Validate Member ---" in captured.out
    assert "Validation feature not implemented yet.\n" in captured.out
    assert "Exiting..." in captured.out

def test_main_option_invalid(capsys):
    """Test flow for an invalid option, followed by exit."""
    
    # Simulate entering invalid option '9', followed by '5' (Exit)
    input_sequence = iter(['9', '5'])
    with patch('builtins.input', lambda prompt: next(input_sequence)):
        main()
        
    captured = capsys.readouterr()
    
    # Assert that the error message for an invalid option was printed [3]
    assert "Invalid option. Try again.\n" in captured.out
    assert "Exiting..." in captured.out

def test_main_option_5_exit():
    """Test option 5 immediately breaks the loop and terminates the program [3]."""
    
    # If the program does not break, the test will hang or fail (e.g., TimeoutError)
    input_sequence = iter(['5'])
    with patch('builtins.input', lambda prompt: next(input_sequence)):
        # We ensure the function runs without infinitely looping
        main()