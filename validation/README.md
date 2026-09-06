# Validation Engine (TM3)

This package implements the rule‑validation step for the Legal Metrology Compliance system.

## Files

- `validator.py` – Core validation functions.
- `test_validator.py` – Unit tests (run with `python -m unittest validation/test_validator.py`).

## Public API

```python
from validation.validator import (
    validate_mrp,
    validate_quantity,
    validate_manufacturer,
    validate_date,
    validate_fields,
    validate_field
)
```

### Expected Input

`validate_fields` expects a list of dictionaries matching the output from the OCR pipeline:

```python
[
    {"field": "MRP", "text": "₹199.00", "confidence": 0.95},
    {"field": "quantity", "text": "500 g", "confidence": 0.93},
    ...
]
```

Each dict must contain:
- `field`: name of the field (case‑insensitive, e.g. "MRP", "quantity")
- `text`: extracted string from OCR
- `confidence`: float in [0, 1] representing OCR confidence

### Output

Returns a list of result dictionaries:

```python
[
    {
        "field": "MRP",
        "status": "PASS",   # or "FAIL" or "UNCERTAIN"
        "details": "Valid MRP format: ₹199.00",
        "confidence": 0.95
    },
    ...
]
```

- `status` **PASS** – validation succeeded.
- `status` **FAIL** – validation failed and OCR confidence ≥ 0.5.
- `status` **UNCERTAIN** – validation failed but OCR confidence < 0.5 (low‑confidence OCR).

### Validation Rules

| Field          | Rule (regex / logic)                                                                 |
|----------------|------------------------------------------------------------------------------------|
| MRP            | `^(?:₹|Rs\.?)\s*\d+(?:\.\d{1,2})?$` (₹ or Rs., optional space, up to 2 decimals) |
| Quantity       | `^\d+(?:\.\d+)?\s*(?:g|kg|mg|ml|l)\s*$` (number, optional space, unit)            |
| Manufacturer   | Non‑empty, ≤100 chars, only letters, spaces, . , , ' -                           |
| Date           | Accepts `DD/MM/YY`, `MM/DD/YY`, `DD/MM`, `MM/DD` with `/` or `-` separators; basic range checks (day 1‑31, month 1‑12). |

## Running Tests

```bash
# From the repository root
python -m unittest validation/test_validator.py
```

All tests should pass.

## Integration

The validation step fits between OCR extraction and result presentation/storage:

```
Image → Detection → OCR → Validation (TM3) → UI/Storage
```

Call `validate_fields()` on the list produced by `backend/main.py:process_and_format_for_validation()` to obtain validation results ready for display or logging.