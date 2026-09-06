# Storage Module (TM5)

This module handles the storage of inspection records using SQLite.

## Table Structure

As per `Rules.md`, the `inspections` table has the following columns:
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `timestamp` (TEXT NOT NULL) - ISO format timestamp of inspection
- `image_name` (TEXT NOT NULL) - Name of the inspected image file
- `result_json` (TEXT NOT NULL) - JSON string of inspection results
- `passed` (BOOLEAN NOT NULL) - Whether the inspection passed

## Usage

```python
from storage.database import InspectionDB

# Initialize database (defaults to "inspections.db" in current directory)
db = InspectionDB()

# Store an inspection result
result_data = {
    "mrp": {"value": "₹199.00", "confidence": 0.95},
    "net_quantity": {"value": "500 g", "confidence": 0.92},
    "manufacturer": {"value": "ABC Foods Pvt Ltd", "confidence": 0.88},
    "violations": [],
    "passed": True
}

inspection_id = db.store_inspection("product_label.jpg", result_data, True)

# Retrieve an inspection by ID
inspection = db.get_inspection(inspection_id)

# Get all inspections (most recent first)
all_inspections = db.get_all_inspections(limit=50)

# Get total count
count = db.get_inspection_count()

# Delete an inspection
db.delete_inspection(inspection_id)
```

## Features

- Automatic table creation on initialization
- JSON serialization/deserialization of complex result data
- ISO timestamp storage for consistent time handling
- Proper resource management (connections closed after each operation)
- Error handling through SQLite exceptions

## Testing

Run the test suite:
```bash
python test_database.py
```