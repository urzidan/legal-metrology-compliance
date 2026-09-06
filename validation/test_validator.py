import unittest
import sys
import os

# Add the project root to sys.path so we can import validation.validator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from validation.validator import (
    validate_mrp,
    validate_quantity,
    validate_manufacturer,
    validate_date,
    validate_fields,
    validate_field
)

class TestValidationEngine(unittest.TestCase):

    # MRP tests
    def test_mrp_valid(self):
        valid_cases = [
            "₹199.00",
            "₹ 199.00",
            "Rs. 199",
            "Rs 199.50",
            "rs. 50",
            "RS 123.45"
        ]
        for case in valid_cases:
            with self.subTest(case=case):
                self.assertTrue(validate_mrp(case)[0])

    def test_mrp_invalid(self):
        invalid_cases = [
            "199.00",          # missing currency symbol
            "₹ 199.001",       # more than 2 decimal places
            "₹ abc",           # non-numeric
            "Rs. ",            # empty amount
            "",                # empty string
            "₹",               # only symbol
            "Rs. 12 34",       # space inside number
        ]
        for case in invalid_cases:
            with self.subTest(case=case):
                self.assertFalse(validate_mrp(case)[0])

    # Quantity tests
    def test_quantity_valid(self):
        valid_cases = [
            "500 g",
            "500g",
            "2.5 kg",
            "100 ml",
            "1 L",
            "0.5 mg",
            "1000ML",          # no space, uppercase
            "2.5Kg",           # mixed case
        ]
        for case in valid_cases:
            with self.subTest(case=case):
                self.assertTrue(validate_quantity(case)[0])

    def test_quantity_invalid(self):
        invalid_cases = [
            "500",             # missing unit
            "500 xyz",         # invalid unit
            "500.",            # trailing dot (no digits after dot)
            "g 500",           # wrong order
            "",                # empty
            "2.5kl",           # invalid unit (kiloliter not allowed)
            "2.5KL",           # same
        ]
        for case in invalid_cases:
            with self.subTest(case=case):
                self.assertFalse(validate_quantity(case)[0])

    # Manufacturer tests
    def test_manufacturer_valid(self):
        valid_cases = [
            "ABC Foods Ltd",
            "XYZ Corp",
            "M.K. Enterprises",
            "Test-O-Prod",
            "Bob's Factory",
            "A",               # single letter
            "Test.",           # trailing dot allowed as basic punctuation
        ]
        for case in valid_cases:
            with self.subTest(case=case):
                self.assertTrue(validate_manufacturer(case)[0])

    def test_manufacturer_invalid(self):
        invalid_cases = [
            "",                # empty
            "A"*101,           # too long
            "Test@123",        # invalid char @
            "Test 123",        # digits not allowed per our regex (we only allow letters, spaces, . , ' -)
        ]
        for case in invalid_cases:
            with self.subTest(case=case):
                self.assertFalse(validate_manufacturer(case)[0])

    # Date tests
    def test_date_valid(self):
        valid_cases = [
            "03/24/23",
            "24/03/23",
            "03-24-23",
            "03/24/2023",
            "24/03/2023",
            "03-24-2023",
            "03/24",           # month/day no year
            "24/03",           # day/month no year
            "03-24",
            "12/01",
            "01-12",
        ]
        for case in valid_cases:
            with self.subTest(case=case):
                self.assertTrue(validate_date(case)[0])

    def test_date_invalid(self):
        invalid_cases = [
            "",                # empty
            "32/24/23",        # day >31
            "24/32/23",        # month >12 (if interpreted as month/day)
            "03/24/23/extra",  # extra part
            "03-24-23-",       # trailing separator
            "03/24/2",         # year too short? we accept 2 or 4 digits; 1 digit invalid
            "03/24/202",       # 3 digits invalid
            "03/24/20234",     # 5 digits invalid
            "ab/cd/ef",        # non-numeric
        ]
        for case in invalid_cases:
            with self.subTest(case=case):
                self.assertFalse(validate_date(case)[0])

    # Combined fields test
    def test_validate_fields(self):
        fields = [
            {"field": "MRP", "text": "₹199.00", "confidence": 0.95},
            {"field": "quantity", "text": "500 g", "confidence": 0.93},
            {"field": "manufacturer", "text": "ABC Foods Ltd", "confidence": 0.97},
            {"field": "date", "text": "03/24/23", "confidence": 0.9},
            {"field": "MRP", "text": "199.00", "confidence": 0.9},   # invalid MRP
            {"field": "quantity", "text": "500", "confidence": 0.9}, # invalid quantity
        ]
        results = validate_fields(fields)
        self.assertEqual(len(results), 6)
        # Check first four PASS
        for i in range(4):
            self.assertEqual(results[i]["status"], "PASS")
        # Check MRP invalid -> FAIL (confidence high)
        self.assertEqual(results[4]["status"], "FAIL")
        self.assertIn("Invalid MRP format", results[4]["details"])
        # Check quantity invalid -> FAIL
        self.assertEqual(results[5]["status"], "FAIL")
        self.assertIn("Invalid quantity format", results[5]["details"])

    # Confidence -> UNCERTAIN
    def test_uncertain_low_confidence(self):
        fields = [
            {"field": "MRP", "text": "199.00", "confidence": 0.4},  # invalid but low conf
        ]
        results = validate_fields(fields)
        self.assertEqual(results[0]["status"], "UNCERTAIN")
        # If confidence high, should be FAIL
        fields2 = [
            {"field": "MRP", "text": "199.00", "confidence": 0.6},
        ]
        results2 = validate_fields(fields2)
        self.assertEqual(results2[0]["status"], "FAIL")

    # Single field convenience
    def test_validate_field(self):
        res = validate_field("MRP", "₹199.00", 0.95)
        self.assertEqual(res["status"], "PASS")
        res2 = validate_field("MRP", "199.00", 0.9)
        self.assertEqual(res2["status"], "FAIL")

if __name__ == '__main__':
    unittest.main()