"""
Test script to verify validation integration in the backend API
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
backend_path = project_root / "backend"
sys.path.append(str(project_root))
sys.path.append(str(backend_path))
sys.path.append(str(backend_path / "api"))

def test_validation_logic():
    """Test that our validation logic works correctly"""
    print("Testing validation logic...")

    # Import the validation function
    try:
        from validation.validator import validate_fields
        print("[OK] Successfully imported validation module")
    except ImportError as e:
        print("[ERROR] Failed to import validation module: {e}")
        return False

    # Test cases that should pass
    test_cases_pass = [
        {"field": "MRP", "text": "₹199.00", "confidence": 0.95},
        {"field": "MRP", "text": "Rs. 199", "confidence": 0.90},
        {"field": "Quantity", "text": "500 g", "confidence": 0.93},
        {"field": "Quantity", "text": "2.5 kg", "confidence": 0.91},
        {"field": "Manufacturer", "text": "ABC Foods Ltd", "confidence": 0.97},
        {"field": "Date", "text": "03/24/23", "confidence": 0.90},
    ]

    # Test cases that should fail
    test_cases_fail = [
        {"field": "MRP", "text": "199.00", "confidence": 0.9},  # missing currency
        {"field": "MRP", "text": "Rs 199.00 USD", "confidence": 0.8},  # extra text
        {"field": "Quantity", "text": "500", "confidence": 0.9},  # missing unit
        {"field": "Quantity", "text": "500 lbs", "confidence": 0.85},  # wrong unit
        {"field": "Manufacturer", "text": "", "confidence": 0.8},  # empty
        {"field": "Manufacturer", "text": "ABC@#$%", "confidence": 0.7},  # invalid chars
        {"field": "Date", "text": "32/24/23", "confidence": 0.8},  # invalid day
        {"field": "Date", "text": "03/00/23", "confidence": 0.8},  # invalid month
    ]

    print("\n--- Testing PASS cases ---")
    all_passed = True
    for i, case in enumerate(test_cases_pass):
        results = validate_fields([case])
        result = results[0]
        if result["status"] == "PASS":
            print("[OK] Test {i+1}: {case['field']} = '{case['text']}' -> {result['status']}")
        else:
            print("[ERROR] Test {i+1}: {case['field']} = '{case['text']}' -> {result['status']} ({result['details']})")
            all_passed = False

    print("\n--- Testing FAIL cases ---")
    for i, case in enumerate(test_cases_fail):
        results = validate_fields([case])
        result = results[0]
        if result["status"] == "FAIL":
            print("[OK] Test {i+1}: {case['field']} = '{case['text']}' -> {result['status']}")
        else:
            print("[ERROR] Test {i+1}: {case['field']} = '{case['text']}' -> {result['status']} (expected FAIL)")
            all_passed = False

    return all_passed

def test_api_integration():
    """Test that our API can be imported and initialized"""
    print("\nTesting API integration...")

    try:
        # Change to backend directory to import properly
        os.chdir(str(project_root / "backend"))
        from api.main import LegalMetrologyPipeline, get_expected_value, generate_violation_for_field, calculate_risk_score
        print("[OK] Successfully imported API components")

        # Test helper functions
        expected = get_expected_value("MRP")
        print("[OK] get_expected_value('MRP') = '{expected}'")

        violation = generate_violation_for_field("MRP", "Missing currency symbol")
        if violation and "rule" in violation:
            print("[OK] generate_violation_for_field works: {violation['rule']}")
        else:
            print("[ERROR] generate_violation_for_field failed")
            return False

        score = calculate_risk_score([{"severity": "Medium"}, {"severity": "Low"}])
        print("[OK] calculate_risk_score([Medium, Low]) = {score}")

        return True
    except Exception as e:
        print("[ERROR] API integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Return to original directory
        os.chdir(project_root)

if __name__ == "__main__":
    print("=" * 60)
    print("PackSure Validation Integration Test")
    print("=" * 60)

    test1_passed = test_validation_logic()
    test2_passed = test_api_integration()

    print("\n" + "=" * 60)
    if test1_passed and test2_passed:
        print("[SUCCESS] ALL TESTS PASSED - Validation integration is working!")
        print("[READY] Ready to test with actual detection/OCR pipeline")
    else:
        print("[FAILURE] SOME TESTS FAILED - Please fix issues before proceeding")
    print("=" * 60)