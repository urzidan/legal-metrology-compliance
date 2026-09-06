"""
Validation Engine for Legal Metrology Compliance
Validates extracted text fields against Legal Metrology (Packaged Commodities) Rules, 2011
"""

import re
from typing import Tuple, List, Dict, Union

def validate_mrp(text: str) -> Tuple[bool, str]:
    """
    Validate MRP (Maximum Retail Price) field.
    Rules: Must be in Indian Rupees, prefixed with ₹ or Rs., optional space,
           followed by digits with up to two decimal places.
    Examples valid: "₹199.00", "₹ 199.00", "Rs. 199", "Rs 199.50"
    """
    if not text or not isinstance(text, str):
        return False, "MRP text is empty or not a string"

    # Remove leading/trailing whitespace
    text = text.strip()

    # Regex pattern for MRP:
    # ^(?:₹|Rs\.?)\s*\d+(?:\.\d{1,2})?$
    # Explanation:
    # ^ - start of string
    # (?:₹|Rs\.?) - either ₹ or Rs. (with optional period)
    # \s* - optional whitespace
    # \d+ - one or more digits
    # (?:\.\d{1,2})? - optional decimal point with 1 or 2 digits
    # $ - end of string
    pattern = r'^(?:₹|Rs\.?)\s*\d+(?:\.\d{1,2})?$'

    if re.match(pattern, text, re.IGNORECASE):
        return True, f"Valid MRP format: {text}"
    else:
        return False, f"Invalid MRP format: '{text}'. Expected format: ₹ or Rs. followed by amount with up to 2 decimal places."

def validate_quantity(text: str) -> Tuple[bool, str]:
    """
    Validate Net Quantity field.
    Rules: Must be a number (integer or decimal) followed by a space and a valid unit.
           Valid units: g, kg, mg, ml, l (case-insensitive).
           Optional space between number and unit.
    Examples valid: "500 g", "500g", "2.5 kg", "100 ml", "1 L"
    """
    if not text or not isinstance(text, str):
        return False, "Quantity text is empty or not a string"

    text = text.strip()

    # Regex pattern for quantity:
    # ^\d+(?:\.\d+)?\s*(?:g|kg|mg|ml|l)\s*$
    # Explanation:
    # ^ - start
    # \d+(?:\.\d+)? - integer or decimal number
    # \s* - optional whitespace
    # (?:g|kg|mg|ml|l) - unit (case-insensitive)
    # \s* - optional trailing whitespace
    # $ - end
    pattern = r'^\d+(?:\.\d+)?\s*(?:g|kg|mg|ml|l)\s*$'

    if re.match(pattern, text, re.IGNORECASE):
        return True, f"Valid quantity format: {text}"
    else:
        return False, f"Invalid quantity format: '{text}'. Expected format: number followed by unit (g, kg, mg, ml, l)."

def validate_manufacturer(text: str) -> Tuple[bool, str]:
    """
    Validate Manufacturer/Packer/Importer field.
    Rules: Must not be empty, should contain only alphabets, spaces, and basic punctuation.
           Length reasonable (1-100 characters).
    """
    if not text or not isinstance(text, str):
        return False, "Manufacturer text is empty or not a string"

    text = text.strip()

    if len(text) == 0:
        return False, "Manufacturer name cannot be empty"

    if len(text) > 100:
        return False, "Manufacturer name too long (max 100 characters)"

    # Allow letters, spaces, dots, hyphens, apostrophes, and commas
    if not re.match(r"^[A-Za-z\s\.\,\'\-]+$", text):
        return False, "Manufacturer name contains invalid characters"

    return True, f"Valid manufacturer name: {text}"

def validate_date(text: str) -> Tuple[bool, str]:
    """
    Validate Date field (e.g., manufacturing date, expiry date).
    Rules: Must be a valid date in common formats: DD/MM/YY, DD/MM/YYYY, MM/DD/YY, MM/DD/YYYY,
           or DD/MM, MM/DD (without year). Separators can be '/' or '-'.
    Does not validate calendar correctness (e.g., Feb 30), only basic ranges.
    """
    if not text or not isinstance(text, str):
        return False, "Date text is empty or not a string"

    text = text.strip()

    # Accept separators / or -
    # Split by separator
    sep = None
    if '/' in text:
        sep = '/'
    elif '-' in text:
        sep = '-'
    else:
        return False, f"Invalid date format: '{text}'. Expected separator '/' or '-'"

    parts = text.split(sep)
    if len(parts) not in (2, 3):
        return False, f"Invalid date format: '{text}'. Expected 2 or 3 parts separated by '{sep}'"

    # Convert parts to integers, reject if non-numeric or empty
    try:
        nums = [int(p) for p in parts]
    except ValueError:
        return False, f"Invalid date format: '{text}'. Parts must be numeric"

    # Validate each component is positive
    if any(n <= 0 for n in nums):
        return False, f"Invalid date format: '{text}'. Components must be positive"

    if len(nums) == 3:
        # Interpret as day/month/year or month/day/year
        a, b, year = nums
        # Year validation
        if len(str(year)) == 2:
            if not (0 <= year <= 99):
                return False, f"Invalid two-digit year: {year}"
        elif len(str(year)) == 4:
            if not (1000 <= year <= 9999):
                return False, f"Invalid four-digit year: {year}"
        else:
            return False, f"Invalid year length: {year}"

        # Check day/month ranges: either (a day, b month) or (b day, a month)
        day1, month1 = a, b
        day2, month2 = b, a
        valid1 = (1 <= day1 <= 31) and (1 <= month1 <= 12)
        valid2 = (1 <= day2 <= 31) and (1 <= month2 <= 12)
        if not (valid1 or valid2):
            return False, f"Invalid day/month values: {a}/{b}. One must be month (1-12) and the other day (1-31)"
        return True, f"Valid date format: {text}"
    else:  # len(nums) == 2
        # Assume month/day (no year) - common for expiry like "03/24"
        # Accept either order where one is month (1-12) and other is day (1-31)
        a, b = nums
        # Option 1: a=month, b=day
        opt1 = (1 <= a <= 12) and (1 <= b <= 31)
        # Option 2: b=month, a=day
        opt2 = (1 <= b <= 12) and (1 <= a <= 31)
        if not (opt1 or opt2):
            return False, f"Invalid day/month values: {a}/{b}. One must be month (1-12) and the other day (1-31)"
        return True, f"Valid date format: {text}"

def validate_fields(fields: List[Dict[str, Union[str, float]]]) -> List[Dict]:
    """
    Validate a list of field dictionaries.

    Args:
        fields: List of dicts with keys: 'field' (str), 'text' (str), 'confidence' (float)

    Returns:
        List of validation result dicts with keys:
        - field: field name
        - status: 'PASS', 'FAIL', or 'UNCERTAIN'
        - details: validation message
        - confidence: OCR confidence (passed through)
    """
    results = []

    for field_dict in fields:
        field_name = field_dict.get('field', '').lower()
        text = field_dict.get('text', '')
        confidence = field_dict.get('confidence', 0.0)

        # Determine validation function based on field name
        if field_name in ['mrp']:
            is_valid, message = validate_mrp(text)
        elif field_name in ['quantity']:
            is_valid, message = validate_quantity(text)
        elif field_name in ['manufacturer', 'packer', 'importer']:
            is_valid, message = validate_manufacturer(text)
        elif field_name in ['date', 'mfg_date', 'exp_date']:
            is_valid, message = validate_date(text)
        else:
            # Unknown field: treat as pass but with warning
            is_valid = True
            message = f"No validation rule for field '{field_name}' - accepting as is"

        # Determine status
        if is_valid:
            status = "PASS"
        else:
            # If confidence is low, mark as UNCERTAIN instead of FAIL
            if confidence < 0.5:
                status = "UNCERTAIN"
            else:
                status = "FAIL"

        results.append({
            "field": field_dict.get('field', field_name),
            "status": status,
            "details": message,
            "confidence": confidence
        })

    return results

# Convenience function for direct validation of a single field
def validate_field(field_name: str, text: str, confidence: float = 1.0) -> Dict:
    """
    Validate a single field and return result dict.
    """
    field_dict = {
        "field": field_name,
        "text": text,
        "confidence": confidence
    }
    results = validate_fields([field_dict])
    return results[0] if results else {}

if __name__ == "__main__":
    # Simple test cases
    test_cases = [
        ("MRP", "₹199.00", 0.95),
        ("MRP", "₹ 199.00", 0.92),
        ("MRP", "Rs. 199", 0.90),
        ("MRP", "Rs 199.50", 0.88),
        ("MRP", "199.00", 0.9),  # missing currency symbol
        ("Quantity", "500 g", 0.93),
        ("Quantity", "500g", 0.90),
        ("Quantity", "2.5 kg", 0.95),
        ("Quantity", "100 ml", 0.92),
        ("Quantity", "1 L", 0.9),
        ("Quantity", "500", 0.9),  # missing unit
        ("Manufacturer", "ABC Foods Ltd", 0.97),
        ("Manufacturer", "", 0.8),  # empty
        ("Date", "03/24/23", 0.9),
        ("Date", "03/24/2023", 0.88),
        ("Date", "24/03/23", 0.9),  # day/month/year
        ("Date", "03-24-23", 0.9),
        ("Date", "32/24/23", 0.8),  # invalid day/month
        ("Date", "03/24", 0.85),    # month/day no year
        ("Date", "24/03", 0.85),    # day/month no year
    ]

    print("Running validation tests...")
    for field, text, conf in test_cases:
        result = validate_field(field, text, conf)
        print(f"{field}: '{text}' -> {result['status']} - {result['details']}")