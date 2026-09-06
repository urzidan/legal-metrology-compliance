import sys
sys.path.insert(0, '.')

from validation.validator import validate_fields

# Sample data without rupee symbol to avoid encoding issues
sample_fields = [
    {"field": "MRP", "text": "Rs. 199.00", "confidence": 0.95},
    {"field": "MRP", "text": "Rs 199", "confidence": 0.90},
    {"field": "MRP", "text": "199.00", "confidence": 0.9},  # invalid
    {"field": "quantity", "text": "500 g", "confidence": 0.93},
    {"field": "quantity", "text": "500g", "confidence": 0.90},
    {"field": "quantity", "text": "2.5 kg", "confidence": 0.95},
    {"field": "quantity", "text": "100 ml", "confidence": 0.92},
    {"field": "quantity", "text": "1 L", "confidence": 0.9},
    {"field": "quantity", "text": "500", "confidence": 0.9},  # invalid
    {"field": "manufacturer", "text": "ABC Foods Ltd", "confidence": 0.97},
    {"field": "manufacturer", "text": "", "confidence": 0.8},  # invalid
    {"field": "date", "text": "03/24/23", "confidence": 0.9},
    {"field": "date", "text": "24/03/23", "confidence": 0.9},
    {"field": "date", "text": "03/24", "confidence": 0.85},
    {"field": "date", "text": "32/24/23", "confidence": 0.8},  # invalid
]

print("Testing validation engine...")
results = validate_fields(sample_fields)

for res in results:
    # Use repr to avoid encoding issues
    print(f"{res['field']:12} {res['status']:8} -> {repr(res['details'])}")
