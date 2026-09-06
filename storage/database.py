import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any


class InspectionDB:
    """
    SQLite database handler for storing inspection records.

    Table structure as per Rules.md:
    inspections (id, timestamp, image_name, result_json, passed)
    """

    def __init__(self, db_path: str = "inspections.db"):
        """
        Initialize the database connection and create table if it doesn't exist.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Create the inspections table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inspections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                image_name TEXT NOT NULL,
                result_json TEXT NOT NULL,
                passed BOOLEAN NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def store_inspection(self, image_name: str, result_data: Dict[str, Any], passed: bool) -> int:
        """
        Store an inspection record in the database.

        Args:
            image_name: Name of the inspected image file
            result_data: Dictionary containing inspection results
            passed: Boolean indicating if inspection passed

        Returns:
            The ID of the inserted record
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Convert result data to JSON string for storage
        result_json = json.dumps(result_data)
        timestamp = datetime.now().isoformat()

        cursor.execute('''
            INSERT INTO inspections (timestamp, image_name, result_json, passed)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, image_name, result_json, passed))

        inspection_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return inspection_id

    def get_inspection(self, inspection_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve an inspection record by ID.

        Args:
            inspection_id: ID of the inspection to retrieve

        Returns:
            Dictionary containing the inspection data or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, timestamp, image_name, result_json, passed
            FROM inspections
            WHERE id = ?
        ''', (inspection_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'id': row[0],
                'timestamp': row[1],
                'image_name': row[2],
                'result_data': json.loads(row[3]),
                'passed': bool(row[4])
            }
        return None

    def get_all_inspections(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve all inspection records, ordered by timestamp descending.

        Args:
            limit: Maximum number of records to return

        Returns:
            List of inspection dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, timestamp, image_name, result_json, passed
            FROM inspections
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))

        rows = cursor.fetchall()
        conn.close()

        inspections = []
        for row in rows:
            inspections.append({
                'id': row[0],
                'timestamp': row[1],
                'image_name': row[2],
                'result_data': json.loads(row[3]),
                'passed': bool(row[4])
            })

        return inspections

    def delete_inspection(self, inspection_id: int) -> bool:
        """
        Delete an inspection record by ID.

        Args:
            inspection_id: ID of the inspection to delete

        Returns:
            True if record was deleted, False if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM inspections WHERE id = ?', (inspection_id,))
        deleted = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return deleted

    def get_inspection_count(self) -> int:
        """
        Get the total number of inspection records.

        Returns:
            Count of inspections in the database
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM inspections')
        count = cursor.fetchone()[0]

        conn.close()

        return count


# Example usage
if __name__ == "__main__":
    # Initialize database
    db = InspectionDB("test_inspections.db")

    # Store a sample inspection
    sample_result = {
        "mrp": {"value": "₹199.00", "confidence": 0.95},
        "net_quantity": {"value": "500 g", "confidence": 0.92},
        "manufacturer": {"value": "ABC Foods Pvt Ltd", "confidence": 0.88},
        "violations": [],
        "passed": True
    }

    inspection_id = db.store_inspection("sample_product.jpg", sample_result, True)
    print(f"Stored inspection with ID: {inspection_id}")

    # Retrieve the inspection
    retrieved = db.get_inspection(inspection_id)
    print(f"Retrieved inspection: {retrieved}")

    # Get all inspections
    all_inspections = db.get_all_inspections()
    print(f"Total inspections: {len(all_inspections)}")

    # Clean up test database
    os.remove("test_inspections.db")