"""
Test data loader utilities.
Supports CSV loading for parametrized test data.
"""
import csv
from pathlib import Path
from typing import Dict, List, Any


class TestDataLoader:
    """Load and query test data from CSV files."""

    def __init__(self, csv_path: Path):
        self.csv_path = Path(csv_path)
        self._data = []
        self._by_set = {}
        self._load()

    def _load(self):
        """Load CSV data into memory."""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Test data file not found: {self.csv_path}")

        with open(self.csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            self._data = list(reader)

        # Index by data_set
        for row in self._data:
            ds = row.get("data_set", "")
            if ds not in self._by_set:
                self._by_set[ds] = []
            self._by_set[ds].append(row)

    def get_all(self) -> List[Dict[str, str]]:
        """Return all test data rows."""
        return self._data

    def get_by_set(self, data_set: str) -> List[Dict[str, str]]:
        """Return all rows for a given data_set (e.g., 'D01')."""
        return self._by_set.get(data_set, [])

    def get_by_id(self, data_id: str) -> Dict[str, str]:
        """Return a single row by data_id."""
        for row in self._data:
            if row.get("data_id") == data_id:
                return row
        return {}

    def get_by_priority(self, priority: str) -> List[Dict[str, str]]:
        """Return all rows matching a priority (P0/P1/P2/P3)."""
        return [row for row in self._data if row.get("priority") == priority]

    def get_scenarios(self, data_set: str) -> List[str]:
        """Return scenario names for a data_set."""
        return [row.get("scenario", "") for row in self.get_by_set(data_set)]

    @property
    def data_sets(self) -> List[str]:
        """List all available data sets."""
        return list(self._by_set.keys())

    @property
    def count(self) -> int:
        """Total number of test data rows."""
        return len(self._data)


def load_csv_as_params(csv_path: Path, data_set: str) -> List[tuple]:
    """Load CSV data as pytest parametrize tuples."""
    loader = TestDataLoader(csv_path)
    rows = loader.get_by_set(data_set)
    result = []
    for row in rows:
        result.append((
            row.get("data_id", ""),
            row.get("scenario", ""),
            row,
        ))
    return result
